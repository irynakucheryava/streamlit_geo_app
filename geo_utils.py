import h3pandas
import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px

from CONSTANTS import TABLE_INDEX
from geojson import Feature, FeatureCollection


def add_geography(raw_data, raw_geography):
    """
    Siple merge of actual data and geographic data.
    """
    raw_data_coord = pd.merge(raw_data, raw_geography, on=TABLE_INDEX)
    raw_data_coord.index = raw_geography["h3_index"]
    return raw_data_coord


def add_h3_index(raw_data : pd.DataFrame, resolution : int):
    """
    Adding H3 Uber index based on latitude and longitude.
    """
    raw_data_h3 = raw_data.h3.geo_to_h3(
        resolution=resolution,
        lat_col="LATITUDE", lng_col="LONGITUDE",
        set_index=True,
    ).copy()
    raw_data_h3["h3_index"] = raw_data_h3.index
    raw_data_h3 = raw_data_h3.h3.h3_to_geo_boundary()
    return raw_data_h3


def h3_resolution_change(raw_coord_h3 : pd.DataFrame, new_resolution : int):
    """
    Resizing of H3 hexagons.
    """
    # get old resolution
    old_resolution = raw_coord_h3.h3.h3_get_resolution().h3_resolution.unique()[0]
    if old_resolution > new_resolution:
        # if new resolution is parent to old
        raw_data_h3_new = raw_coord_h3.h3.h3_to_parent_aggregate(new_resolution)
        raw_data_h3_new["h3_index"] = raw_data_h3_new.index
        return raw_data_h3_new
    elif old_resolution == new_resolution:
        # nothing to do
        return raw_coord_h3
    else:
        # drop old and create new
        raw_coord_h3.reset_index(inplace=True)
        raw_data_h3_new = add_h3_index(raw_coord_h3, new_resolution)
        return raw_data_h3_new


def hexagons_dataframe_to_geojson(
    df_hex, hex_id_field, geometry_field, value_field
    ):
    """
    Create geojson coordintes out of H3 index for plotly.
    """
    list_features = []
    for _, row in df_hex.iterrows():
        feature = Feature(geometry = row[geometry_field],
                          id = row[hex_id_field],
                          properties = {"value": row[value_field]})
        list_features.append(feature)
    feat_collection = FeatureCollection(list_features)
    return feat_collection


def plotly_h3(df, col, col_log):
    """
    Plotly map based on H3 index.
    """
    geojson_obj = hexagons_dataframe_to_geojson(
        df,
        hex_id_field="h3_index",
        value_field=col_log,
        geometry_field="geometry"
    )

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_obj,
        locations="h3_index",
        color=col_log,
        color_continuous_scale="thermal", # "Viridis"
        range_color=(0,  df[col_log].max()),
        #range_color=(0,  19),
        hover_data={'h3_index': True, col:True, col_log:False},
        #mapbox_style="carto-positron",
        mapbox_style="open-street-map",
        zoom=3.5,
        #center = {"lat": df["LATITUDE"].mean(), "lon": df["LONGITUDE"].mean()},
        center = {"lat": 37.0902, "lon": -95.7129},
        opacity=0.8,
        #labels={"count":"# of fire ignitions"}
    )
    #fig.update_coloraxes(colorbar_dtick=5)
    # here np.round(df[col_log].max() / 5) can be 0 which cause for Hawaii
    log_ticks = np.arange(0, df[col_log].max(), np.round(df[col_log].max() / 5)).tolist()
    true_ticks = [2**i if i != 0 else i for i in log_ticks]
    fig.update_coloraxes(colorbar_dtick=5, colorbar_tickvals=log_ticks,
                         colorbar_ticktext=true_ticks)
    fig.update_layout(height=900, coloraxis_colorbar=dict(title=col))

    return fig


def plotly_hist_all(df, col, x_label, color, title, cumulative=False):
    fig = px.histogram(
        df,
        x=col,
        color_discrete_sequence=[color],
        marginal="violin",
        nbins=150,
        cumulative=cumulative,
        opacity=0.7,
        labels={
            col: x_label
            },
    )
    fig.update_traces(marker_line_width=1, marker_line_color="white")
    fig.update_layout(
        height=600,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
        }
    )
    return fig


def quantile_filter(df : pd.DataFrame, col : str, q=0.95):
    df_filtered = df.loc[
        (df[col] <= df[[col]].quantile(q)[0]) &
        (df[col] > 0),
        [col]
    ]
    return df_filtered


def h3_tab_plot(
        df_h3_geom : pd.DataFrame, col : str, col_log : str,
        distribution_title : str, hist_param_df : dict, hist_param_df_95 : dict
    ):
    fig1 = plotly_h3(
        df=df_h3_geom,
        col=col,
        col_log=col_log
    )
    st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

    count_filtered = quantile_filter(df_h3_geom, col)

    with st.container():
        st.write(
            distribution_title
        )
        col1, col2 = st.columns(2)
        with col1:
            hist1 = plotly_hist_all(
                df=df_h3_geom,
                col=col,
                cumulative=False,
                x_label=hist_param_df["x_label"],
                color='gold',
                title=hist_param_df["title"],
            )
            st.plotly_chart(hist1, use_container_width=True, theme='streamlit')
        with col2:
            hist2 = plotly_hist_all(
                df=count_filtered,
                col=col,
                cumulative=False,
                x_label=hist_param_df_95["x_label"],
                color='gold',
                title=hist_param_df_95["title"],
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
