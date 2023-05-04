import streamlit as st
import querry
import geo_utils
import pandas as pd
import numpy as np

from utils import list_concat

from CONSTANTS import (
    YEAR, STATES,
    TABLE_DATA, TABLE_INDEX, # is TABLE_INDEX needed to be imported? it is only used a few times? same for TABLE_DATA
    FIELD_PREFIXES,
)

H3_RESOLUTION = 6


def h3_geomap_UI():
    st.title('🌎 H3 geomap')
    st.header('''Explore US Census data though H3 Geo lens by navigating through demographic filters.''')
    st.markdown('#')
    st.write(
        """
        By default we show a count of the whole population within each hexagon at H3 level 4 in 2020.
        Use filters to see a geo representation of a different subset of the data.
        Please note that Filter 2 will be shown only if available.
        Select 'All' if you want all option for a given filter to be used.
        If you select 'All' in conjunction with another option(s), then all options will be used.
        Once ready, click the "Show results" button to display H3 geo map.
        """)
    #st.markdown('#')
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
                options=['All'] + list(STATES.keys()),
                default='All',
            )
        # split
        with sel3:
            splits = fd.loc[
                fd.TABLE_NUMBER.isin(FIELD_PREFIXES),
                "TABLE_TITLE"
            ].unique().tolist()
            selected_var = st.selectbox(
                "What variable would you like to look at?",
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
                states_codes = [code for _, code in STATES.items() if _ in states]
                states_list = list_concat(states_codes)
                cbg_states = querry.read_static(year, name="states", use_where=True, states_list=states_list)

            # creating the final field description dataframe - if no choices available for filter 2, then just use filter 1
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
            df_h3_geom['index_median'] = df_h3_geom['count'].apply(
                lambda x: x / df_h3_geom['count'].median() # here median can be 0. Mb median + 1?
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
                fig1 = geo_utils.plotly_h3(
                    df=df_h3_geom,
                    col='count',
                    col_log='log2_value_count'
                )
                st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

                count_filtered = geo_utils.quantile_filter(df_h3_geom, 'count')
                # count_filtered = df_h3_geom.loc[
                #     (df_h3_geom['count'] <= df_h3_geom[["count"]].quantile(0.95)[0]) &
                #     (df_h3_geom['count'] > 0),
                #     ['count']
                # ]

                with st.container():
                    st.write(
                        'Explore hexagon size distribution for selected population at H' + str(h3_res) + ' level.'
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        #st.write('The histogram shows the raw distribution of all hexagon couns at H' + str( h3_res) + ' level.')
                        hist1 = geo_utils.plotly_hist_all(
                            df=df_h3_geom,
                            col='count',
                            cumulative=False,
                            x_label="Number of people within a hexagon",
                            color='gold',
                            title='Distribution of all hexagon counts'
                        )
                        st.plotly_chart(hist1, use_container_width=True, theme='streamlit')
                    with col2:
                        # st.write('''The histogram shows the processed distribution of all hexagon couns at H' + str(h3_res) + ' level.
                        #          Processed means that all hexagons with the count of 0 were removed as well as all hexagons with a count of above 95th% quantile.
                        #          ''')
                        hist2 = geo_utils.plotly_hist_all(
                            df=count_filtered,
                            col='count',
                            cumulative=False,
                            x_label="Number of people within a hexagon",
                            color='gold',
                            title='Distribution of hexagon counts above 0 and below 95th percentile'
                        )
                        st.plotly_chart(hist2, use_container_width=True, theme='streamlit')


                hist_df_1 = pd.concat(
                    [
                        pd.DataFrame(df_h3_geom['count']).describe().transpose(),
                        pd.DataFrame(count_filtered.describe()).transpose()
                    ]
                )
                hist_df_1.index = ['raw count', 'filtered count']
                st.dataframe(hist_df_1, use_container_width=True)

            with tab2:
                st.write(
                    '''This map shows an index - a count within each hexagon compared to the MEAN value across all hexagons for filtered population.
                    For example, a value of 200 means that compared to an average count, a given hexagon contains twice as many people,
                    while a value of 50 means twice as less.
                    Note that index is calculated taken all selected states into account.
                    '''
                )
                fig2 = geo_utils.plotly_h3(df_h3_geom, col='index_mean', col_log='index_log')
                st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

                ind_mean_filtered = geo_utils.quantile_filter(df_h3_geom, 'index_mean')
                # ind_mean_filtered = df_h3_geom.loc[
                #     (df_h3_geom['index_mean'] <= df_h3_geom[['index_mean']].quantile(0.95)[0]) &
                #     (df_h3_geom['index_mean'] > 0),
                #     ['index_mean']
                # ]

                with st.container():
                    st.write(
                        'Explore hexagon index against mean distribution for selected population at H' + str(h3_res) + ' level.'
                    )
                    col3, col4 = st.columns(2)
                    with col3:
                        #st.write('The histogram shows the raw distribution of all hexagon couns at H' + str( h3_res) + ' level.')
                        hist3 = geo_utils.plotly_hist_all(
                            df=df_h3_geom,
                            col='index_mean',
                            cumulative=False,
                            x_label="Index against mean",
                            color='darkviolet',
                            title='Distribution of all hexagon indeces against mean'
                        )
                        st.plotly_chart(hist3, use_container_width=True, theme='streamlit')
                    with col4:
                        # st.write('''The histogram shows the processed distribution of all hexagon couns at H' + str(h3_res) + ' level.
                        #          Processed means that all hexagons with the count of 0 were removed as well as all hexagons with a count of above 95th% quantile.
                        #          ''')
                        hist4 = geo_utils.plotly_hist_all(
                            df=ind_mean_filtered,
                            col='index_mean',
                            cumulative=False,
                            x_label="Index against mean",
                            color='darkviolet',
                            title='Distribution of hexagon indices against mean above 0 and below 95th percentile'
                        )
                        st.plotly_chart(hist4, use_container_width=True, theme='streamlit')

                hist_df_2 = pd.concat(
                    [
                        pd.DataFrame(df_h3_geom['index_mean']).describe().transpose(),
                        pd.DataFrame(ind_mean_filtered.describe()).transpose()
                    ]
                )
                hist_df_2.index = ['raw count', 'filtered count']
                st.dataframe(hist_df_2, use_container_width=True)
            with tab3:
                st.write('''This map shows an index - a count within each hexagon compared to the MEDIAN val across all hexagons for filtered population.
                         Median helps account for skewness in the data and a non-representative mean. Same rules as in the "Mean Index" tab apply:
                             a value of 200 means that compared to a median count, a given hexagon contains twice as many people,
                             while a value of 50 means twice as less.
                             Note that index is calculated taken all selected states into account.
                         ''')
                fig3 = geo_utils.plotly_h3(df_h3_geom, col='index_median', col_log='index_med_log')
                st.plotly_chart(fig3, use_container_width=True, theme="streamlit")

                ind_med_filtered = geo_utils.quantile_filter(df_h3_geom, 'index_median')
                # ind_med_filtered = df_h3_geom.loc[
                #     (df_h3_geom['index_median'] <= df_h3_geom[['index_median']].quantile(0.95)[0]) &
                #     (df_h3_geom['index_median'] > 0),
                #     ['index_median']
                # ]

                with st.container():
                    st.write('Explore hexagon index against median distribution for selected population at H' + str(h3_res) + ' level.')
                    col5, col6 = st.columns(2)
                    with col5:
                        #st.write('The histogram shows the raw distribution of all hexagon couns at H' + str( h3_res) + ' level.')
                        hist5 = geo_utils.plotly_hist_all(
                            df=df_h3_geom,
                            col='index_median',
                            cumulative=False,
                            x_label="Index against median",
                            color='hotpink',
                            title='Distribution of all hexagon indeces against median'
                        )
                        st.plotly_chart(hist5, use_container_width=True, theme='streamlit')
                    with col6:
                        # st.write('''The histogram shows the processed distribution of all hexagon couns at H' + str(h3_res) + ' level.
                        #          Processed means that all hexagons with the count of 0 were removed as well as all hexagons with a count of above 95th% quantile.
                        #          ''')
                        hist6 = geo_utils.plotly_hist_all(
                            df=ind_med_filtered,
                            col='index_median',
                            cumulative=False,
                            x_label="Index against median",
                            color='hotpink',
                            title='Distribution of hexagon indices against median above 0 and below 95th percentile'
                        )
                        st.plotly_chart(hist6, use_container_width=True, theme='streamlit')

                hist_df_3 = pd.concat(
                    [
                        pd.DataFrame(df_h3_geom['index_median']).describe().transpose(),
                        pd.DataFrame(ind_med_filtered.describe()).transpose()
                    ])
                hist_df_3.index = ['raw count', 'filtered count']
                st.dataframe(hist_df_3, use_container_width=True)
