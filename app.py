
import streamlit as st
import pandas as pd

import h3_geomap
import comparison
import analytics
import home
import clustering


PAGES = [
    'HOME',
    'H3 GEO LENS',
    'DEMOGRAPHIC ANALYTICS',
    'CLUSTERING'
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
    st.set_page_config(page_title='blah blah', page_icon=':bar_chart:', layout='wide')
    st.sidebar.title('Explore USA GEO Analytics')
    if st.session_state.page:
        page=st.sidebar.radio('', PAGES, index=st.session_state.page)
    else:
        page=st.sidebar.radio('', PAGES, index=0)

    st.experimental_set_query_params(page=page)

    if page == 'HOME':
        st.sidebar.write("""
            ## About

            Brief information about the project
        """)
        home.home_UI()

    elif page == 'H3 GEO LENS':
        st.sidebar.write("""
            ## About

            Hexagon view of demographic data
        """)
        h3_geomap.h3_geomap_UI()
    elif page == 'CLUSTERING':
        st.sidebar.write(
            """
            ## About

            KMeans model for selected demographic features
            """
        )
        clustering.clustering_UI()
    else:
        analytics.analytics_UI()

    # elif page == 'Equity Explorer':
    #     st.sidebar.write("""
    #         ## About
    #         The Equity Explorer is a set of Arup-designed analyses to identify vulnerable and historically under-served geographies at the census tract level. The tool provides a transparent, Arup-approved framework for approaching equity and allows users to compare indicators and explore the data for census tracts across the US. Users can also customize a transportation vulnerability index for their specific planning purposes to best understand which areas have the biggest gaps in accessibility and demand. Keep in mind that much of the data comes from the 2019 US Census which has limitations with response rates.

    #         Please note that this tool is a work in progress. Contact us [here](mailto:shannon.nakamura@arup.com) or consider contributing to our [GitHub](https://github.com/arup-group/social-data) repository with any suggestions or questions.
    #     """)
    #     try:
    #         equity_explorer.census_equity_explorer()
    #     except:
    #         st.error('Equity Explorer is currently under construction. Come back soon!')
    #         st.stop()

    # else:
    #     st.sidebar.write("""
    #         ## About
    #         The Data Explorer is an interface to allow you to explore the data available in our database and do some initial analysis. In total we have over 2 million rows and over 400 unique features with coverage across the 50 US states and expanding to the District of Columbia and Puerto Rico. You can use this interface to combine multiple datasets and export raw data as an Excel file.

    #         Datasets vary between county and census tract resolution and data may not exist for all counties or tracts. Some features may not work for all states/territories.
    #     """)
    #     st.title("Data Explorer")
    #     subcol_1, subcol_2 = st.columns(2)
    #     with subcol_1:
    #         st.session_state.data_type = st.radio("Data resolution:", ('County Level', 'Census Tracts'), index=0)
    #     with subcol_2:
    #         # Todo: implement for census level too
    #         if st.session_state.data_type =='County Level':
    #             st.session_state.data_format = st.radio('Data format', ['Raw Values', 'Per Capita', 'Per Square Mile'], 0)

    #     if st.session_state.data_type == 'County Level':
    #         data_explorer.county_data_explorer()
    #     else:
    #         data_explorer.census_data_explorer()


if __name__ == '__main__':

    url_params = st.experimental_get_query_params()
    if 'loaded' not in st.session_state:
        if len(url_params.keys()) == 0:
            st.experimental_set_query_params(page='HOME')
            url_params = st.experimental_get_query_params()

        st.session_state.page = PAGES.index(url_params['page'][0])
    run_UI()





