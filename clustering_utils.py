import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

from geo_utils import hexagons_dataframe_to_geojson


def clustering_tab_plot(df_h3_geom, n_clusters, features):
    '''Plot clustering results against selected features and number of clusters.'''
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
            pie5 = px.pie(
                df_count,
                values='Number of hexagons',
                names='Cluster',
                color='Cluster',
                color_discrete_sequence=px.colors.sequential.Agsunset
            )
            pie5.update_layout(
                legend_font_size=9,
                legend=dict(
                            orientation="v",
                            itemwidth=50,
                            xanchor="right",
                            x=0.9
                ),
                title={
                    'text': 'Number of hexagons in each cluster',
                    'x': 0.5,
                    'xanchor': 'center',
                }
            )
            st.plotly_chart(pie5, use_container_width=True, theme='streamlit')

        with col2:
            # scatterplot
            if len(features) > 2:
                fig = px.scatter_3d(
                    df_h3_geom,
                    x=features[0],
                    y=features[1],
                    z=features[2],
                    color='cluster',
                    color_discrete_sequence=px.colors.sequential.Agsunset
                )
                fig.update_layout(height=700)
            else:
                fig = px.scatter(
                    df_h3_geom,
                    x=features[0],
                    y=features[1],
                    color='cluster',
                    color_discrete_sequence=px.colors.sequential.Agsunset
                )
                fig.update_layout(height=600)
            fig.update_traces(marker_size=9)
            st.plotly_chart(fig, use_container_width=True, theme='streamlit')

    st.markdown('#')
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            df_sum = df_h3_geom.groupby('cluster')[features].sum().reset_index()
            df_sum = pd.melt(
                df_sum,
                id_vars=['cluster'],
                value_vars=features
            )
            df_sum['cluster'] = df_sum['cluster'].astype(str)

            fig2 = px.bar(
                df_sum,
                color='cluster',
                y='value',
                x='variable',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                height=600,
            )
            fig2.update_layout(
                title={
                    'text': 'Total number of population <br> in each cluster by selected features',
                    'x': 0.5,
                    'xanchor': 'center',
                },
                xaxis_title=None
            )
            st.plotly_chart(fig2, use_container_width=True, theme='streamlit')

        with col2:
            df_mean = df_h3_geom.groupby('cluster')[features].mean().reset_index()
            df_mean = pd.melt(
                df_mean,
                id_vars=['cluster'],
                value_vars=features
            )
            df_mean['cluster'] = df_mean['cluster'].astype(str)

            fig2 = px.bar(
                df_mean,
                color='cluster',
                y='value',
                x='variable',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                height=600,
            )
            fig2.update_layout(
                title={
                    'text': 'Mean number of population <br> in each cluster by selected features',
                    'x': 0.5,
                    'xanchor': 'center',
                    },
                xaxis_title=None
            )
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
    hover.update(dict(zip(features, len(features) * [True])))

    df_h3_geom['cluster'] = df_h3_geom['cluster'].astype('str')

    fig = px.choropleth_mapbox(
        df_h3_geom,
        geojson=geojson_obj,
        locations="h3_index",
        color='cluster',
        mapbox_style="open-street-map",
        color_discrete_map={
            '0': 'pink',
            '1': 'hotpink',
            '2': 'royalblue',
            '3': 'purple',
            '4': 'mediumslateblue'
        },
        hover_data=hover,
        zoom=3.5,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.8
    )
    fig.update_coloraxes(
        colorbar_dtick=n_clusters,
        colorbar_tickvals=np.sort(df_h3_geom['cluster'].unique()),
    )
    fig.update_layout(height=900, coloraxis_colorbar=dict(title='Clusters'))
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
