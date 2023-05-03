
import numpy as np
import streamlit as st
import geo_utils

import plotly.express as px
import pandas as pd
from querry import read_analytics, read_static
#from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from geo_utils import hexagons_dataframe_to_geojson

from CONSTANTS import YEAR, STATES, TABLE_INDEX, COLUMNS


def clustering_UI():
    st.title("Clustering page")
    st.header("Build clusters out of census block groups based on selected features")
    st.markdown('#')
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
                "Choose features for clustering",
                options=COLUMNS,
                default=None,
                max_selections=5,
            )
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
    button = st.button(label='  Create clusters  ',
                       help='Select all parameters and click the button',
                       use_container_width=True)
    st.markdown('#')

    if button:

        # getting the data
        df = read_analytics(year=year) # KIRA: here would be nice to already send states and columns as opposed to loadind all the data all the time
        df.set_index(TABLE_INDEX, inplace=True, drop=True)

        # filtering based on states
        if 'All' not in states:
            df = df.loc[df['STATE'].isin(states), :]

        # filtering based on columns
        df = df[features]
        # making sure all features are floats
        df = df.astype('float')
        # replacing outliers  - either remove, or replace with ecdf or leave for now

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

        # scaling values
        scaler = MinMaxScaler()
        norm_features = ['norm_' + i for i in features]
        df_h3_geom[norm_features] = scaler.fit_transform(df_h3_geom[features])

        # fitting kmeans
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
        labels = kmeans.fit_predict(df_h3_geom[norm_features])
        df_h3_geom['cluster'] = labels
        df_h3_geom['cluster'] = df_h3_geom['cluster'].astype('str')
        df_h3_geom = df_h3_geom.sort_values('cluster')

        #st.markdown('#')
        st.markdown("""---""")
        st.markdown('#')
        st.header('''Basic cluster statistics''')
        st.markdown('#')

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                df_count = df_h3_geom['cluster'].value_counts().reset_index()
                df_count.columns = ['Cluster', 'Number of hexagons']
                df_count['Cluster'] = df_count['Cluster'].astype(object)
                df_count = df_count.sort_values('Cluster')
                st.markdown('#')
                st.markdown('#')
                st.markdown('#')
                st.markdown('#')
                pie5 = px.pie(df_count,
                              values='Number of hexagons',
                              names='Cluster',
                              color='Cluster',
                              color_discrete_sequence=px.colors.sequential.Agsunset)
                pie5.update_layout(legend_font_size=9,
                                   legend=dict(
                                       orientation="v",
                                       itemwidth=50,
                                       #yanchor="bottom",
                                       #y=1.02,
                                       xanchor="right",
                                       x=0.9),
                                   title={
                                       'text': 'Number of hexagons in each cluster',
                                       #'y':0.9,
                                       'x':0.5,
                                       'xanchor': 'center',
                                       #'yanchor': 'top'
                                       })
                st.plotly_chart(pie5, use_container_width=True, theme='streamlit')

            with col2: # scatterplot
                #df_h3_geom['cluster'] = df_h3_geom['cluster'].astype('str')
                if len(features) > 2:
                    fig = px.scatter_3d(df_h3_geom,
                                        x=features[0],
                                        y=features[1],
                                        z=features[2],
                                        color='cluster',
                                        color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(height=700)
                else:
                    fig = px.scatter(df_h3_geom,
                                     x=features[0],
                                     y=features[1],
                                     color='cluster',
                                     color_discrete_sequence=px.colors.sequential.Agsunset)
                    fig.update_layout(height=600)

                fig.update_traces(marker_size = 9)


                st.plotly_chart(fig, use_container_width=True, theme='streamlit')

        st.markdown('#')
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                df_sum = df_h3_geom.groupby('cluster')[features].sum().reset_index()
                df_sum = pd.melt(df_sum,
                                 id_vars=['cluster'],
                                 value_vars=features)
                df_sum['cluster'] = df_sum['cluster'].astype(str)

                fig2 = px.bar(df_sum,
                              color='cluster',
                              y='value',
                              x='variable',
                              color_discrete_sequence=px.colors.sequential.Agsunset,
                              height=600,
                              )
                fig2.update_layout(
                    title={
                        'text': 'Total number of population <br> in each cluster by selected features',
                        #'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        #'yanchor': 'top'
                        },
                    xaxis_title=None)
                st.plotly_chart(fig2, use_container_width=True, theme='streamlit')

            with col2:
                df_mean = df_h3_geom.groupby('cluster')[features].mean().reset_index()
                df_mean = pd.melt(df_mean,
                                  id_vars=['cluster'],
                                  value_vars=features)
                df_mean['cluster'] = df_mean['cluster'].astype(str)

                fig2 = px.bar(df_mean,
                              color='cluster',
                              y='value',
                              x='variable',
                              color_discrete_sequence=px.colors.sequential.Agsunset,
                              height=600,
                              )
                fig2.update_layout(
                    title={
                        'text': 'Mean number of population <br> in each cluster by selected features',
                        #'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        #'yanchor': 'top'
                        },
                    xaxis_title=None)
                st.plotly_chart(fig2, use_container_width=True, theme='streamlit')

        st.markdown('#')
        st.markdown('#')
        st.markdown("""---""")
        st.markdown('#')
        st.header('''Plotting H3 clustered hexagons''')
        st.markdown('#')

        #creating geo map with clusters
        geojson_obj = hexagons_dataframe_to_geojson(
            df_h3_geom,
            hex_id_field="h3_index",
            value_field='cluster',
            geometry_field="geometry"
        )

        hover = {'h3_index': True, 'cluster': True}
        hover.update(dict(zip(features, len(features)*[True])))

        df_h3_geom['cluster'] = df_h3_geom['cluster'].astype('str')

        fig = px.choropleth_mapbox(
            df_h3_geom,
            geojson=geojson_obj,
            locations="h3_index",
            color='cluster',
            mapbox_style="open-street-map",
            #color_discrete_sequence=px.colors.sequential.Agsunset,
            color_discrete_map = {'0': 'pink', '1': 'hotpink', '2':'royalblue', '3':'purple', '4':'mediumslateblue'},
            hover_data=hover,
            zoom=3.5,
            center = {"lat": 37.0902, "lon": -95.7129},
            opacity=0.8
        )
        fig.update_coloraxes(colorbar_dtick=n_clusters,
                              colorbar_tickvals=np.sort(df_h3_geom['cluster'].unique())),
                              #colorbar_ticktext=np.sort(df_h3_geom['cluster'].unique()))
        fig.update_layout(height=900, coloraxis_colorbar=dict(title='Clusters'))

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")









