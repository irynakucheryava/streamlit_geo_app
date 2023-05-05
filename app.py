
import streamlit as st
import pandas as pd

import h3_geomap
import analytics
import home
import clustering


PAGES = [
    '🏠 Home',
    '👨‍👩‍👧‍👦 Demographic Statistics',
    '🌎 H3 Geo Lens',
    '🎯 ML Geo Clustering'
]

def run_UI():
    st.set_page_config(page_title='US GEO CENSUS',
                       layout='wide')
    st.sidebar.title('🗺 US GEO CENSUS APP')
    if st.session_state.page:
        page=st.sidebar.radio('', PAGES, index=st.session_state.page)
    else:
        page=st.sidebar.radio('', PAGES, index=0)

    st.experimental_set_query_params(page=page)

    if page == '🏠 Home':
        st.sidebar.write("""
            ## About
           App description
        """)
        home.home_UI()

    elif page == '👨‍👩‍👧‍👦 Demographic Statistics':
        st.sidebar.write("""
            ## About
            Interactive demographic dashboard
        """)

        analytics.analytics_UI()

    elif page == '🌎 H3 Geo Lens':
        st.sidebar.write("""
            ## About
            Hexagon view of selected demographic data, year and state
        """)

        h3_geomap.h3_geomap_UI()

    else:
        st.sidebar.write("""
            ## About
            Cluster hexagons based on similarities
        """)
        clustering.clustering_UI()


if __name__ == '__main__':

    url_params = st.experimental_get_query_params()
    if 'loaded' not in st.session_state:
        if len(url_params.keys()) == 0:
            st.experimental_set_query_params(page='🏠 Home')
            url_params = st.experimental_get_query_params()

        st.session_state.page = PAGES.index(url_params['page'][0])
    run_UI()

