import streamlit as st
import querry
import geo_utils
import pandas as pd
import numpy as np


from utils import list_concat
from CONSTANTS import YEAR, STATES, TABLE_DATA, TABLE_INDEX


SPLITS = [
    'Sex By Age',
    'Race',
    'Travel Time To Work',
    'Households By Type',
    "Total Fields Of Bachelor's Degrees Reported",
    'Occupancy Status',
    'Value'
]

H3_RESOLUTION = 6


def h3_geomap_UI():
    st.title('H3 geomap')
    st.header('''Explore geo spatial data in the US by navigating through demographic filters''')
    st.markdown('#')
    st.write("""
            By default we show a count of males of all age groups.
            If you want to explore the count of the whle populaition then simply choose both Male and Female.
            Please note that Filter 2 will be shown only if available.""")

    st.markdown('#')
    # select year
    year = st.selectbox(
        "What year do you want to explore?",
        YEAR ,
        1,
    )
    # get coordinates
    cbg_coord = querry.read_static(year, name="geographic", use_where=False)
    # field description
    fd = querry.read_static(year, "description")
    st.markdown('#')
    # select state
    states = st.multiselect(
        label="Choose state or ALL",
        options=['All'] + list(STATES.keys()),
        default=None,
    )
    # select cbg from selected states
    if len(states) > 0:
        if 'All' in states:
            cbg_states = querry.read_static(year, name="states", use_where=False)
        else:
            states_codes = [code for _, code in STATES.items() if _ in states]
            states_list = list_concat(states_codes)
            cbg_states = querry.read_static(year, name="states", use_where=True, states_list=states_list)
        # choose split
        st.markdown('#')
        split = st.selectbox(
            "Chooose split to show",
            SPLITS,
            0
        )
        # select description for chosen split
        fd_split = fd.loc[fd.TABLE_TITLE == split]
        # lvl 5 filter
        filter_lvl5 = list(
            filter(
                None,
                fd_split.FIELD_LEVEL_5.unique()
            )
        )
        st.markdown('#')
        filter_1 = st.multiselect(
            label="Choose filter 1",
            options=['All'] + filter_lvl5,
            default=None,
        )
        if len(filter_1) > 0:
            # filtered by lvl 6
            if 'All' in filter_1:
                filter_1 = filter_lvl5
            filter_lvl6 = list(
                filter(
                    None,
                    fd_split.loc[
                        fd_split.FIELD_LEVEL_5.isin(filter_1),
                        "FIELD_LEVEL_6"
                    ].unique()
                )
            )
            if len(filter_lvl6) > 0:
                st.markdown('#')
                filter_2 = st.multiselect(
                    "Choose filter 2",
                    options=['All'] + filter_lvl6,
                    default=None,
                )
                if len(filter_2) > 0:
                    if 'All' in filter_2:
                        filter_2 = filter_lvl6
                    fd_final = fd_split.loc[
                            fd_split.FIELD_LEVEL_5.isin(filter_1) &
                            fd_split.FIELD_LEVEL_6.isin(filter_2)
                        ]
                else:
                    fd_final = fd_split.loc[
                            fd_split.FIELD_LEVEL_5.isin(filter_1) 
                        ]
            else:
                fd_final = fd_split.loc[
                        fd_split.FIELD_LEVEL_5.isin(filter_1) 
                    ]
            # select H3 resolution
            h3_res = st.selectbox(
                "Choose resolution of H3",
                [4, 5, 6],
                2
            )
            # data table postfix
            table_id = fd_final.TABLE_NUMBER.str[:3].unique()[0]
            # table name and columns for actual data
            df_table = TABLE_DATA.format(year=year, table_id=table_id)
            cols = list(fd_final.TABLE_ID.unique())
            # read data
            df = querry.read_dataset(df_table, cols)
            df = df.loc[
                df[TABLE_INDEX].isin(cbg_states[TABLE_INDEX])
            ]
            # filter coord
            cbg_coord_f = cbg_coord.loc[
                cbg_coord[TABLE_INDEX].isin(cbg_states[TABLE_INDEX])
            ]
            # add h3 index to coordinates
            cbg_coord_h3 = geo_utils.add_h3_index(cbg_coord_f, resolution=H3_RESOLUTION)
            # add geometry
            df_h3_geom = geo_utils.add_geography(df, cbg_coord_h3)
            # check selected resolution
            df_h3_geom = geo_utils.h3_resolution_change(df_h3_geom, h3_res)
            df_h3_geom["value_count"] = df_h3_geom[cols].sum(axis=1)
            # add log value
            df_h3_geom['log2_value_count'] = np.log2(df_h3_geom['value_count'])
            df_h3_geom.loc[np.isinf(df_h3_geom['log2_value_count']), 'log2_value_count'] = 0 # replacing inf with 0 (still 0 peopl in hexagon)
            # plot h3 map
            fig = geo_utils.plotly_h3(df_h3_geom)
            st.markdown('#')
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")

            st.markdown('#')
            st.subheader('Explore descriptive statistics of hexagons')
            with st.container():
                hist1, hist2 = st.columns(2)
                with hist1:
                    fig1 = geo_utils.plotly_hist_all(df=df_h3_geom, h3_level=str(h3_res))
                    st.plotly_chart(fig1)
                with hist2: # the safest option should be to just exclude outliers
                    df1 = df_h3_geom.loc[
                        (df_h3_geom['value_count'] <= df_h3_geom[["value_count"]].quantile(0.95)[0]) &
                        (df_h3_geom['value_count'] > 0),
                        ['value_count']
                    ].copy()
                    fig2 = geo_utils.plotly_hist_out(df1, h3_level=str(h3_res))
                    st.plotly_chart(fig2)

            st.markdown('#')
            with st.container():
                tab1, tab2 = st.columns(2)
                with tab1:
                    st.dataframe(
                        pd.DataFrame(
                            df_h3_geom['value_count'].describe()
                        ).transpose(),
                        use_container_width=True
                    )
                with tab2:
                    st.dataframe(
                        pd.DataFrame(
                            df1['value_count'].describe()
                        ).transpose(),
                        use_container_width=True
                    )