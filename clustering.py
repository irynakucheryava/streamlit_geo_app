
import numpy as np
import streamlit as st

import geo_utils

from clustering_utils import clustering_tab_plot
from querry import read_analytics, read_static

from CONSTANTS import (
    YEAR, STATES, TABLE_INDEX, COLUMNS
)


def clustering_UI():
    st.title("🎯 ML Geo Clustering")
    st.header("Group hexagons based on demographic similarities")
    st.markdown('#')
    st.write(
        '''
        Select location, features of interest, number of clusters, desired H3 resolution and click "Create clusters" button.
        Make sure to select at least 2 variables. Unselect "All" if you want to cluster hexagons from certain state(s) only.
        '''
    )
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.selectbox(
                label="Year",
                options=YEAR,
                index=1,
            )
        with col2:
            states = st.multiselect(
                label="State",
                options=['All'] + list(STATES.values()),
                default='All',
            )
        with col3:
            features = st.multiselect(
                "Choose up to 5 features",
                options=COLUMNS,
                default=None,
                max_selections=5,
            )
            number_of_features = len(features)
    st.markdown('#')
    st.markdown('#')
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            n_clusters = st.slider(
                label="Select number of desired clusters",
                min_value=2,
                max_value=5,
                value=2,
            )
        with col2:
            h3_res = st.slider(
                label="Choose H3 resolution",
                min_value=4,
                max_value=6,
                value=4
            )

    st.markdown('#')
    button = st.button(
        label='  Create clusters  ',
        help='Select all parameters and click the button',
        use_container_width=False,
        disabled=False,
    )
    st.markdown('#')

    if button:
        if number_of_features < 2:
            st.error(
                "You must select at least 2 features for clustering. {} was selected.".format(
                len(features)
            ),
        )
        # getting the data
        df = read_analytics(year=year)
        df.set_index(TABLE_INDEX, inplace=True, drop=True)

        # filtering based on states
        if 'All' not in states:
            df = df.loc[df['STATE'].isin(states), :]
        # filtering based on columns
        df = df[features]
        # making sure all features are floats
        df = df.astype('float')
        # mapping to H3 resolution
        cbg_coord = read_static(year, name="geographic", use_where=False)
        # filtering by states
        cbg_coord = cbg_coord.loc[cbg_coord[TABLE_INDEX].isin(df.index)]
        #add h3 index to coordinates at H6 level
        cbg_coord_h3 = geo_utils.add_h3_index(cbg_coord, resolution=6)
        # adding h3 index to data
        df_h3_geom = geo_utils.add_geography(df, cbg_coord_h3)
        # maapping h3 index to parent if needed
        if h3_res != 6:
            df_h3_geom = geo_utils.h3_resolution_change(df_h3_geom, h3_res)
        # deleting hexagons withs 0 across selected features
        df_h3_geom = df_h3_geom[np.invert(df_h3_geom[features].sum(axis=1) == 0)]
        # leaving only hexagons where valies are not above 95th percentile
        keep = np.invert(
            (
                (
                    df_h3_geom[features] > df_h3_geom[features].quantile(0.95)
                ).sum(axis=1)
            ) == len(features)
        )
        df_h3_geom_95 = df_h3_geom[keep].copy()
        st.markdown("""---""")
        st.markdown('#')
        st.header('''Basic cluster statistics''')
        st.markdown('#')
        # create tabs
        tab1, tab2, = st.tabs(['All non empty hexagons', 'Hexagons below 95th percentile'])
        with tab1:
            st.write(
                '''
                Explore clusters created based on non empty hexagons. This means that,
                depending on selected H3 resolution, all hexagons with 0 count across
                all selected features are removed.
                '''
            )
            clustering_tab_plot(
                df_h3_geom=df_h3_geom,
                n_clusters=n_clusters,
                features=features
            )
        with tab2:
            st.write(
                '''
                Explore clusters created with hexagons below 95th percentile.
                All hexagons where the count of all selected features is above
                their respective 95th percentile are removed. This is done to offer
                a cleaner view of clusters, thus avoiding big locations (e.g. cities).
                '''
            )
            clustering_tab_plot(
                df_h3_geom=df_h3_geom_95,
                n_clusters=n_clusters,
                features=features
            )
