import streamlit as st
from PIL import Image
import pandas as pd


def home_UI():

    st.title(
    'USA GEO ANALYTICS :earth_americas:')

    st.subheader('''
             This app helps you visually explore various demographics in the USA by adopting Uber H3 Hexagonal Hierarchical Spatial Index framework.

             ''')

    st.header('Data')
    with st.container():
        text, screen = st.columns(2)
        with text:
            st.markdown('#')
            st.markdown('#')
            st.markdown('#')
            st.write('''
                     USA GEO ANALYTICS app uses free source Snowflake dataset "US Open Census Data & Neighborhood Insights".
                     The data presents a rich selection of various demographics to explore, however, in our app we have decided to concentrate
                     only on a couple of features for dempnstration purposes:''')

            st.markdown('- Sex By Age')
            st.markdown('- Race')
            st.markdown('- Travel Time To Work')
            st.markdown('- Households By Type')
            st.markdown('- Total Fields Of Bachelors Degrees Reported')
            st.markdown('- Occupancy Status')
            st.markdown('- Value (Housing Value and Purchase Price')
            st.write('''
                     We also allow a user to filter the features further by filtering on 2 sub-dimentions. For example in Households By Type we allow to filter out not only by type
                     but also by living engagement such as Living alone. Not all features have second a second level filter.
                     ''')
        with screen:
            image1 = Image.open('images/data_imagei.png')
            st.image(image1)
            st.markdown('#')
            st.markdown('#')
            image2 = Image.open('images/data_image.png')
            st.image(image2)

    # st.markdown('#')
    # st.header('Snowflake connect')
    # with st.container():
    #     text1, screen1 = st.columns(2)
    #     with text1:
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.markdown('#')
    #         st.write('''
    #                  In order to use this this app you need to connect to the dataset in Snowflake.
    #                  To to this, make sure you have an account in Snowflake or a free trial.
    #                  Once the acount has been created, navigate to Marketplace and look for
    #                  "US Open Census Data & Neighborhood Insights", then clock 'Get'.
    #                  Credential info here.
    #                  ''')
    #     with screen1:
    #         image3 = Image.open('images/image3.png')
    #         st.image(image3)

    st.header('Uber H3 Spatial Index')
    image = Image.open('images/Twitter-H3.png.webp')
    st.image(image)
    st.write('''Uber H3 spacial index uses hexagons as the grid system. One of it's major benefits is that it allows to scale up and down different levels.
             In this application, for demonstration purposes we offer three H3 levels - 4,5 and 6.
             You can read more about it [here](https://www.uber.com/en-PL/blog/h3/)
             ''')
    st.markdown('#')
    st.write('''
             In the table below you can see how much area in km2 each hexagon covers split by three resolutions we allow in this app.
             ''')
    h3_res_table = pd.read_csv('tables/h3_resolution.csv', sep= ';')
    h3_res_table.set_index('H3 resolution',inplace=True)
    st.dataframe(h3_res_table, width=2000)
    st.markdown('#')
    st.write('''
             We use [H3](https://h3geo.org) open source library to project hexagons onto the map using latitude and longitude information available in the dataset.
             ''')

    st.header('Contributors')





