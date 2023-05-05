import streamlit as st
import querry
import geo_utils
import pandas as pd
import numpy as np

from utils import list_concat

from CONSTANTS import (
    YEAR, STATES,
    TABLE_DATA, TABLE_INDEX,
    FIELD_PREFIXES,
)

H3_RESOLUTION = 6


def h3_geomap_UI():
    st.title('🌎 H3 Geo Lens')
    st.header('''Explore US Census data via H3 Geo lens by navigating through demographic filters''')
    st.markdown('#')
    st.write(
        """
        This part of the app generates a map with a count of selected population within each hexagon at desired a H3 level.
        Use filters to see a geo representation of a different subset of the data.
        Please note that options for the second filter will be shown only if available.
        Select 'All' if you want all options for a given filter to be used.
        If you select 'All' in conjunction with another option(s), then all options will be used.
        Make sure to unselect 'All' if you want only a certain state(s) to show.
        Once ready, click the "Show results" button to display H3 geo map.
        """)
    with st.container():
        sel1, sel2, sel3 = st.columns(3)
        # year
        with sel1:
            year = st.selectbox(
                "Year",
                YEAR,
                1,
            )
            # field description
            fd = querry.read_static(year, "description")
        # states
        with sel2:
            states = st.multiselect(
                label="State",
                options=['All'] + list(STATES.values()),
                default='All',
            )
        # split
        with sel3:
            splits = fd.loc[
                fd.TABLE_NUMBER.isin(FIELD_PREFIXES),
                "TABLE_TITLE"
            ].unique().tolist()
            selected_var = st.selectbox(
                "Select variable",
                splits,
                0,
            )
    with st.container():
        sel4, sel5, sel6 = st.columns(3)
        # first level filter
        with sel4:
            # select description for chosen split
            fd_split = fd.loc[fd.TABLE_TITLE == selected_var]
            # options for filter 1
            filter_1_choices = list(filter(None, fd_split.FIELD_LEVEL_5.unique()))
            filter_1 = st.multiselect(
                label="Select the first filter",
                options=['All'] + filter_1_choices,
                default='All',
            )
        # second level filter
        with sel5:
            if 'All' in filter_1:
                filter_2_choices = list(
                    filter(
                        None,
                        fd_split.loc[
                            fd_split.FIELD_LEVEL_5.isin(filter_1_choices),
                            "FIELD_LEVEL_6"
                        ].unique()
                    )
                )
            else:
                filter_2_choices = list(
                    filter(
                        None,
                        fd_split.loc[
                            fd_split.FIELD_LEVEL_5.isin(filter_1),
                            "FIELD_LEVEL_6"
                        ].unique()
                    )
                )
            filter_2 = st.multiselect(
                label="Select the second filter",
                options=['All'] + filter_2_choices,
                default='All',
            )
        # h3 index resolution
        with sel6:
            h3_res = st.selectbox(
                "Choose H3 resolution",
                [4, 5, 6],
                0
            )
        st.markdown('#')
        button = st.button(
            label='Show results',
            help='Select filters and click the button'
        )
        if button:
            # filtering census block group codes for selected states
            if 'All' in states:
                cbg_states = querry.read_static(year, name="states", use_where=False)
            else:
                states_list = list_concat(states)
                cbg_states = querry.read_static(year, name="states", use_where=True, states_list=states_list)
            # creating the final field description dataframe - if no choices available for filter 2,
            # then just use filter 1
            # filtering fd based on the first filter
            if 'All' in filter_1 or len(filter_1) == 0:
                fd_final = fd_split.loc[fd_split.FIELD_LEVEL_5.isin(filter_1_choices)]
            else:
                fd_final = fd_split.loc[fd_split.FIELD_LEVEL_5.isin(filter_1)]

            # filterding fd based on filter 2 if exists
            if len(filter_2_choices) > 0:
                if 'All' in filter_2 or len(filter_2) == 0:
                    fd_final = fd_final.loc[fd_split.FIELD_LEVEL_6.isin(filter_2_choices)]
                else:
                    fd_final = fd_final.loc[fd_split.FIELD_LEVEL_6.isin(filter_2)]
            #### querring the data
            # selecting unique variablr indicators
            table_id = fd_final.TABLE_NUMBER.str[:3].unique()[0]
            # table name and columns for actual data
            df_table = TABLE_DATA.format(year=year, table_id=table_id)
            cols = list(fd_final.TABLE_ID.unique())
            # read data
            df = querry.read_dataset(df_table, cols)
            # slecting cbg for selected states
            df = df.loc[df[TABLE_INDEX].isin(cbg_states[TABLE_INDEX])]
            # freading lat and log and filtering by selected states cbg
            cbg_coord = querry.read_static(year, name="geographic", use_where=False)
            cbg_coord_f = cbg_coord.loc[cbg_coord[TABLE_INDEX].isin(cbg_states[TABLE_INDEX])]
            # add h3 index to coordinates at H6 level
            cbg_coord_h3 = geo_utils.add_h3_index(cbg_coord_f, resolution=H3_RESOLUTION)
            # merging df and cbg_coord_h3 by cbg
            df_h3_geom = geo_utils.add_geography(df, cbg_coord_h3)
            # change H3 level to  user selected level
            if h3_res != H3_RESOLUTION:
                df_h3_geom = geo_utils.h3_resolution_change(df_h3_geom, h3_res)
            #### calculating count, indices and logs
            df_h3_geom["count"] = df_h3_geom[cols].sum(axis=1)
            df_h3_geom['log2_value_count'] = np.log2(df_h3_geom['count']) # this can be a function
            # finding an index - compared to hexagon national average at given H3 resolution
            df_h3_geom['index_mean'] = df_h3_geom['count'].apply(
                lambda x: x / df_h3_geom['count'].mean()
            ).round(2)
            df_h3_geom['index_log'] = np.log2(df_h3_geom['index_mean'])

            # calculating index based on median
            median_divider = df_h3_geom['count'].median() if df_h3_geom['count'].median() > 0 else 0.01
            df_h3_geom['index_median'] = df_h3_geom['count'].apply(
                lambda x: x / median_divider # here median can be 0. Mb median + 1?
            ).round(2)
            df_h3_geom['index_med_log'] = np.log2(df_h3_geom['index_median'])

            # replacing Inf with 0
            df_h3_geom.replace([np.inf, -np.inf], 0, inplace=True)

            tab1, tab2, tab3 = st.tabs(['Raw', 'Mean Index', 'Median Index'])
            with tab1:
                st.write(
                    '''
                    This map shows the count of people within every H3 hexagon
                    who meet the criteria selected in the filter section.
                    '''
                )
                geo_utils.h3_tab_plot(
                    df_h3_geom=df_h3_geom, col='count', col_log='log2_value_count',
                    distribution_title='Explore hexagon size distribution for selected population at H' + str(h3_res) + ' level.',
                    hist_param_df={
                        'x_label': "Number of people within a hexagon",
                        'title': 'Distribution of all hexagon counts'
                    },
                    hist_param_df_95={
                        'x_label': "Number of people within a hexagon",
                        'title': 'Distribution of hexagon counts <br> above 0 and below 95th percentile'
                    }
                )
            with tab2:
                st.write(
                    '''This map shows an index - a count within each hexagon compared to the MEAN value across all hexagons for filtered population.
                    For example, a value of 200 means that compared to an average count, a given hexagon contains twice as many people,
                    while a value of 50 means half as many.
                    Note that index is calculated taken all selected states into account.
                    '''
                )
                geo_utils.h3_tab_plot(
                    df_h3_geom=df_h3_geom, col='index_mean', col_log='index_log',
                    distribution_title='Explore hexagon index against mean distribution for selected population at H' + str(h3_res) + ' level.',
                    hist_param_df={
                        'x_label': "Index against mean",
                        'title': 'Distribution of all hexagon <br> indices against mean'
                    },
                    hist_param_df_95={
                        'x_label': "Index against mean",
                        'title': 'Distribution of hexagon indices <br> against mean above 0 and below 95th percentile'
                    }
                )
            with tab3:
                st.write(
                    '''
                    This map shows an index - a count within each hexagon compared to the MEDIAN value across all hexagons for filtered population.
                    Median helps account for skewness in the data and a non-representative mean. Same rules as in the "Mean Index" tab apply:
                    a value of 200 means that compared to a median count, a given hexagon contains twice as many people,
                    while a value of 50 means half as many.
                    Note that index is calculated taken all selected states into account.
                    '''
                )
                geo_utils.h3_tab_plot(
                    df_h3_geom=df_h3_geom, col='index_median', col_log='index_med_log',
                    distribution_title='Explore hexagon index against median distribution for selected population at H' + str(h3_res) + ' level.',
                    hist_param_df={
                        'x_label': "Index against median",
                        'title': 'Distribution of all hexagon <br> indices against median'
                    },
                    hist_param_df_95={
                        'x_label': "Index against median",
                        'title': 'Distribution of hexagon indices <br> against median above 0 and below 95th percentile'
                    }
                )
