import streamlit as st
from PIL import Image
import pandas as pd


def home_UI():

    with st.container():
        text, vis = st.columns(2)
        with text:
            st.markdown('#')
            st.markdown('#')
            st.markdown('#')
            st.markdown('#')
            st.markdown('#')
            st.title('        🗺  US GEO CENSUS APP')
        with vis:
            image1 = Image.open('images/01 Header.PNG')
            image1 = image1.resize((600, 400))
            st.image(image1)
    st.markdown('#')
    st.markdown('#')

    st.subheader('''
             🕵🏻‍♀️ Explore US Census Data though geo lens'''
             )
    st.write('''
             With the power of Uber H3 Hexagonal Hierarchical Spatial Index framework you now can explore various demographic variables mapped onto county’s landscape.
             On top of it, with US GEO CENSUS app you can study demographics statistics through a dynamic dashboard as well use Machine Learning Clustering
             to group and visualise hexagons based on pre-selected parameters.
             ''')

    st.markdown('#')
    st.markdown("""---""")
    st.subheader('📊 Data')
    st.markdown('#')
    with st.container():
        text, vis = st.columns(2)
        with text:
            #st.markdown('#')
            st.markdown('#')
            st.write('''
                     US GEO CENSUS app uses free source Snowflake dataset
                     [US Open Census Data & Neighborhood Insights](https://app.snowflake.com/marketplace/listing/GZSNZ2UNN0/safegraph-us-open-census-data-neighborhood-insights-free-dataset).
                     The data presents a rich selection of various demographics to explore, however,
                     in our app we have decided to concentrate only on a couple of
                     features for demonstration purposes:
                             ''')
            st.markdown('- Sex By Age')
            st.markdown('- Race')
            st.markdown('- Total Fields Of Bachelors Degrees Reported')
            st.markdown('- Value (Housing Value and Purchase Price)')
            st.markdown('- Travel Time To Work')
            st.markdown('- Households By Type')
            st.markdown('- Occupancy Status')
            st.markdown('- Income (Household Income In The Past 12 Months in Inflation-Adjusted Dollars)')
        with vis:
            #st.markdown('#')
            image1 = Image.open('images/data.png')
            image1 = image1.resize((430, 500))
            st.image(image1)

    st.markdown('#')
    st.markdown("""---""")
    st.subheader('🔖 App Tabs')
    st.markdown('#')
    tab1, tab2, tab3 = st.tabs(['👨‍👩‍👧‍👦  Demographic Statistics', '🌎  H3 Geo Lens', '🎯  ML Geo Clustering'])
    with tab1:
        st.markdown('#')
        st.write('''
                 Generate an interactive dahsboard showcasing demographic statistics for
                 a given a year and state. Customize plots views by unselecting categories you do not want to show and by zooming in
                 to get a desired view.  "Population by state and gender" histogram will only be generated if all states are selected.
                 ''')
        image1 = Image.open('images/dem.png')
        st.image(image1)
    with tab2:
        st.markdown('#')
        st.write('''
                 Visualise US Census data using H3 Geo lens. In this tab you can look at various
                 demographics across the whole country or pre-selected states mapped with hexagons at a desired H3 resolution.
                 Each haxagon displays a count of people for a selected variable. Use available filters to filter down a variable of interest.
                 ''')
        st.markdown('#')
        col1, col2, col3 = st.columns(3)
        with col1:
            image1 = Image.open('images/map1.png')
            st.image(image1, width=550)
        with col2:
            image2 = Image.open('images/map2.png')
            st.image(image2, width=550)
        with col3:
            image3 = Image.open('images/map3.png')
            st.image(image3, width=550)

    with tab3:
        st.markdown('#')
        st.write('''
                 Cluster H3 hexagons at a desired resolution by selected features of interest.
                 You can create as many as 5 clusters with up to 5 features across the whole country
                 or pre-selected states.
                 ''')
        st.markdown('#')
        col1, col2 = st.columns(2)
        with col1:
            image1 = Image.open('images/cluster1.png')
            st.image(image1, width=700)
        with col2:
            image2 = Image.open('images/cluster2.png')
            st.image(image2, width=800)

    st.markdown('#')
    st.markdown("""---""")
    st.subheader('🧰 Frameworks')
    st.markdown('#')
    st.write('''
             US GEO CENSUS APP was created with the following freamworks
             ''')
    st.markdown('#')
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        image1 = Image.open('images/streamlit.png')
        st.image(image1, width=200)
    with col2:
        st.markdown('#')
        image2 = Image.open('images/snowflake.png')
        st.image(image2, width=200)
    with col3:
        image1 = Image.open('images/h3.png')
        st.image(image1, width=150)
    with col4:
        image1 = Image.open('images/plotly.png')
        st.image(image1, width=200)
    with col5:
        image1 = Image.open('images/sklearn.png')
        st.image(image1, width=200)
    with col6:
        st.markdown('#')
        image1 = Image.open('images/pandas.png')
        st.image(image1, width=200)
    with col7:
        st.markdown('#')
        image1 = Image.open('images/numpy.png')
        st.image(image1, width=200)

    st.markdown('#')
    st.markdown("""---""")
    st.subheader('🌍 Uber H3 Spatial Index')
    st.markdown('#')
    col1, col2 = st.columns(2)
    with col1:
        image1 = Image.open('images/hexagons.png')
        st.image(image1, width=800)
    with col2:
        st.markdown('#')
        st.write('''Uber H3 spacial index uses hexagons as the grid system. One of its major benefits is
                 that it allows to scale up and down different levels.
                 In this application, for demonstration purposes we offer three H3 levels - 4,5 and 6.
                 You can read more about the framework [here](https://www.uber.com/en-PL/blog/h3/).
               ''')
        st.markdown('#')
        h3_res_table = pd.read_csv('tables/h3_resolution.csv', sep= ';')
        h3_res_table.set_index('H3 resolution',inplace=True)
        st.dataframe(h3_res_table, width=2000)

