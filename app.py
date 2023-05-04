
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
    # st.set_page_config(
    #     page_title="US CENSUS Data Neighborhood Insights",
    #     page_icon="🏠",
    #     initial_sidebar_state="expanded",
        # menu_items={
        #     'Report a bug': "https://github.com/arup-group/social-data/issues/new/choose",
        #     'About': """
        #  If you're seeing this, we would love your contribution! If you find bugs, please reach out or create an issue on our
        #  [GitHub](https://github.com/arup-group/social-data) repository. If you find that this interface doesn't do what you need it to, you can create an feature request
        #  at our repository or better yet, contribute a pull request of your own. You can reach out to the team on LinkedIn or
        #  Twitter if you have questions or feedback.

        # More documentation and contribution details are at our [GitHub Repository](https://github.com/arup-group/social-data).

        #  This app is the result of hard work by our team:
        # - [Jared Stock 🐦](https://twitter.com/jaredstock)
        # - [Angela Wilson 🐦](https://twitter.com/AngelaWilson925) (alum)
        # - Sam Lustado
        # - Lingyi Chen
        # - Kevin McGee (alum)
        # - Jen Combs
        # - Zoe Temco
        # - Prashuk Jain (alum)
        # - Sanket Shah (alum)
        # Special thanks to Julieta Moradei and Kamini Ayer from New Story, Kristin Maun from the city of Tulsa,
        # Emily Walport, Irene Gleeson, and Elizabeth Joyce with Arup's Community Engagment team, and everyone else who has given feedback
        # and helped support this work. Also thanks to the team at Streamlit for their support of this work.
        # The analysis and underlying data are provided as-is as an open source project under an [MIT license](https://github.com/arup-group/social-data/blob/master/LICENSE).
        # Made by [Arup](https://www.arup.com/).
        # """
        # }
    #)
    st.set_page_config(page_title='USA GEO',
                       layout='wide')
    st.sidebar.title('Navigate through tabs')
    if st.session_state.page:
        page=st.sidebar.radio('', PAGES, index=st.session_state.page)
    else:
        page=st.sidebar.radio('', PAGES, index=0)

    st.experimental_set_query_params(page=page)

    if page == '🏠 Home':
        st.sidebar.write("""
            ## About
            Brief information about the project
        """)
        home.home_UI()

    elif page == '👨‍👩‍👧‍👦 Demographic Statistics':
        st.sidebar.write("""
            ## About
            Explore demographic descriptive statistics across years and states
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
            Cluster H3 Geo data based on selected demographics, resolution, state and year
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





