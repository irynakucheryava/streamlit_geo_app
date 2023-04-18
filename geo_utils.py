import h3pandas
import pandas as pd
import numpy as np
from CONSTANTS import TABLE_INDEX

from geojson import Feature, FeatureCollection

import plotly.express as px


def add_geography(raw_data, raw_geography):
    raw_data_coord = pd.merge(raw_data, raw_geography, on=TABLE_INDEX)
    raw_data_coord.index = raw_geography["h3_index"]
    return raw_data_coord

def add_h3_index(raw_data : pd.DataFrame, resolution : int):
    raw_data_h3 = raw_data.h3.geo_to_h3(
        resolution=resolution,
        lat_col="LATITUDE", lng_col="LONGITUDE",
        set_index=True,
    ).copy()
    raw_data_h3["h3_index"] = raw_data_h3.index
    raw_data_h3 = raw_data_h3.h3.h3_to_geo_boundary()
    return raw_data_h3


def h3_resolution_change(raw_coord_h3 : pd.DataFrame, new_resolution : int):
    old_resolution = raw_coord_h3.h3.h3_get_resolution().h3_resolution.unique()[0]
    if old_resolution > new_resolution:
        raw_data_h3_new = raw_coord_h3.h3.h3_to_parent_aggregate(new_resolution)
        raw_data_h3_new["h3_index"] = raw_data_h3_new.index
        return raw_data_h3_new
    elif old_resolution == new_resolution:
        return raw_coord_h3
    else:
        raw_coord_h3.reset_index(inplace=True)
        raw_data_h3_new = add_h3_index(raw_coord_h3, new_resolution)
        return raw_data_h3_new


def hexagons_dataframe_to_geojson(
    df_hex, hex_id_field, geometry_field, value_field
    ):
    list_features = []
    for _, row in df_hex.iterrows():
        feature = Feature(geometry = row[geometry_field],
                          id = row[hex_id_field],
                          properties = {"value": row[value_field]})
        list_features.append(feature)
    feat_collection = FeatureCollection(list_features)
    return feat_collection


def plotly_h3(df):
    geojson_obj = hexagons_dataframe_to_geojson(
        df,
        hex_id_field="h3_index",
        value_field="log2_value_count",
        geometry_field="geometry"
    )

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_obj,
        locations="h3_index",
        color="log2_value_count",
        color_continuous_scale="thermal", # "Viridis"
        range_color=(0,  df["log2_value_count"].max()),
        #range_color=(0,  19),
        hover_data={'h3_index': True, 'value_count':True, 'log2_value_count':False},
        #mapbox_style="carto-positron",
        mapbox_style="open-street-map",
        zoom=3.5,
        center = {"lat": 37.0902, "lon": -95.7129},
        opacity=0.9,
        #labels={"count":"# of fire ignitions"}
    )
    #fig.update_coloraxes(colorbar_dtick=5)
    log_ticks = np.arange(0,  df["log2_value_count"].max(), 5).tolist()
    true_ticks = [2**i if i != 0 else i for i in log_ticks]
    fig.update_coloraxes(colorbar_dtick=5, colorbar_tickvals=log_ticks,
                         colorbar_ticktext=true_ticks)
    fig.update_layout(height=900)

    return fig

def plotly_hist_all(df, h3_level):
    fig = px.histogram(df,
                       x="value_count",
                       color_discrete_sequence=['firebrick'],
                       labels={
                           "value_count": "Number of people in a hexagon"
                           },
                       title="Distribution of all hexagons count at H" + h3_level + ' level')
    return fig

def plotly_hist_out(df, h3_level):
    # removing all zeros and
    fig = px.histogram(df,
                       x="value_count",
                       color_discrete_sequence=['firebrick'],
                       labels={
                           "value_count": "Number of people in a hexagon"
                           },
                       title="Distribution of all hexagons couns above 0 and below 95th percentile at H" + h3_level + ' level')
    return fig









