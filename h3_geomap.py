import streamlit as st
import querry
import geo_utils
import pandas as pd
import numpy as np

YEAR = [
    2019,
    2020
]

SPLITS = [
    'Sex By Age',
    'Race',
    'Travel Time To Work',
    'Households By Type',
    "Total Fields Of Bachelor's Degrees Reported",
    'Occupancy Status',
    'Value'
]

H3_RESOLUTION = 7

coord_h3 = querry.cbg_coordinates(add_h3=True, h3_res=H3_RESOLUTION)



def h3_geomap_UI():
    st.title('H3 geomap')
    st.header('''Explore geo spatial data in the US by navigating through demographic filters''')
    st.markdown('#')
    st.write("""
            By default we show a count of males of all age groups.
            If you want to explore the count of the whle populaition then simply choose both Male and Female.
            Please note that Filter 2 will be shown only if available.""")

    st.markdown('#')

    year = st.selectbox(
        'Select year',
        YEAR ,
        1,
    )
    st.markdown('#')
    # choose split
    split = st.selectbox(
        'Select a feature you would like to explore',
        SPLITS,
        0
    )
    # description map
    fd = querry.field_description(split)
    # lvl 5 filter
    f1 = list(filter(None, fd.FIELD_LEVEL_5.unique()))

    st.markdown('#')
    filter_1 = st.multiselect(
        label="Choose filter 1",
        options=fd.FIELD_LEVEL_5.unique(),
        default=f1[0],
    )
    # filtered by lvl 5
    fd = querry.field_description(split, filter_1)
    # lvl 6 filter
    f2 = list(filter(None, fd.FIELD_LEVEL_6.unique()))
    st.markdown('#')
    if len(f2) > 0:
        filter_2 = st.multiselect(
            "Choose filter 2",
            f2,
            default=f2,
        )
    else:
        filter_2 = None
    st.markdown('#')
    h3_res = st.selectbox(
        "Choose the resolution of H3",
        [4, 5, 6],
    )
    fd_filtered = querry.field_description(split, filter_1, filter_2)
    # table name and columns for actual data
    table = "2020_CBG_" + fd_filtered.TABLE_NUMBER.str[:3].unique()[0]
    cols = list(fd_filtered.TABLE_ID.unique())
    df = querry.read_dataset(table, cols)
    #df["value_count"] = df.sum(axis=1)
    #df['log_value_count'] = np.log2(df["value_count"])
    # check selected resolution
    df_h3_geom = geo_utils.add_geography(df, coord_h3)
    df_h3_geom = geo_utils.h3_resolution_change(df_h3_geom, h3_res)
    df_h3_geom['value_count'] = df_h3_geom[cols].sum(axis=1)
    df_h3_geom['log2_value_count'] = np.log2(df_h3_geom['value_count'])
    df_h3_geom.loc[np.isinf(df_h3_geom['log2_value_count']), 'log2_value_count'] = 0 # replacing inf with 0 (still 0 peopl in hexagon)

    fig = geo_utils.plotly_h3(df_h3_geom)
    # fd_filtered = querry.field_description(split, filter_1, filter_2)
    # if st.checkbox('Show raw data'):
    #     st.subheader('Raw Data')
    #     st.dataframe(fd_filtered)
    st.markdown('#')
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    st.markdown('#')
    st.subheader('Explore descriptive statistics of hexagons')
    with st.container():
        hist1, hist2 = st.columns(2)
        with hist1:
            fig1 = geo_utils.plotly_hist_all(df=df_h3_geom, h3_level=str(h3_res))
            st.plotly_chart(fig1)
        with hist2: # the safest option should be to just exclude outliers
            df1 = df_h3_geom.loc[(df_h3_geom['value_count'] <= df_h3_geom[["value_count"]].quantile(0.95)[0]) & (df_h3_geom['value_count'] > 0),
                                 ['value_count']].copy()
            fig2 = geo_utils.plotly_hist_out(df1, h3_level=str(h3_res))
            st.plotly_chart(fig2)

    st.markdown('#')
    with st.container():
        tab1, tab2 = st.columns(2)
        with tab1:
            st.dataframe(pd.DataFrame(df_h3_geom['value_count'].describe()).transpose(), use_container_width=True)
        with tab2:
            st.dataframe(pd.DataFrame(df1['value_count'].describe()).transpose(), use_container_width=True)






####



# geojson_obj = hexagons_dataframe_to_geojson(
#     df_h3_geom,
#     hex_id_field="h3_index",
#     value_field="log2_value_count",
#     geometry_field="geometry"
# )

# fig = px.choropleth_mapbox(
#     df_h3_geom,
#     geojson=geojson_obj,
#     locations="h3_index",
#     color="value_count",
#     color_continuous_scale="thermal", # "Viridis"
#     range_color=(0, df_h3_geom["value_count"].max()),
#     #color_continuous_midpoint = df_h3_geom["value_count"].median(),
#     color_continuous_midpoint = np.quantile(df_h3_geom["value_count"], 0.05),
#     hover_data=['value_count'],
#     #mapbox_style="carto-positron",
#     mapbox_style="open-street-map",
#     zoom=3.5,
#     center = {"lat": 37.0902, "lon": -95.7129},
#     opacity=0.9,
#     labels={"count":"# of fire ignitions"}
# )
# fig.update_layout(height=900)
# fig.show()


# geojson_obj = hexagons_dataframe_to_geojson(
#     df_h3_geom,
#     hex_id_field="h3_index",
#     value_field="log2_value_count",
#     geometry_field="geometry"
# )

# fig = px.choropleth_mapbox(
#     df_h3_geom,
#     geojson=geojson_obj,
#     locations="h3_index",
#     color="log2_value_count",
#     color_continuous_scale="thermal", # "Viridis"
#     range_color=(0,  df_h3_geom["log2_value_count"].max()),
#     #range_color=(0,  19),
#     hover_data={'h3_index': True, 'value_count':True, 'log2_value_count':False},
#     #mapbox_style="carto-positron",
#     mapbox_style="open-street-map",
#     zoom=3.5,
#     center = {"lat": 37.0902, "lon": -95.7129},
#     opacity=0.9,
#     #labels={"count":"# of fire ignitions"}
# )
# #fig.update_coloraxes(colorbar_dtick=5)
# log_ticks = np.arange(0,  df_h3_geom["log2_value_count"].max(), 5).tolist()
# true_ticks = [2**i if i != 0 else i for i in log_ticks]
# fig.update_coloraxes(colorbar_dtick=5, colorbar_tickvals=log_ticks, colorbar_ticktext=true_ticks)
# #fig.update_coloraxes(showscale=False)
# #fig.update_layout(coloraxis=list(dict(zip(df_h3_geom.log2_value_count, df_h3_geom.value_count))))
# #fig.update_layout(coloraxis=dict(cmax=df_h3_geom["value_count"].max(), cmin=df_h3_geom["value_count"].min()))
# #fig.update_coloraxes(colorbar_labelalias=dict(zip(df_h3_geom.log2_value_count, df_h3_geom.value_count)))
# #fig.show()





# # aaa = px.data.gapminder()

# # fig = px.bar(aaa, x="continent", y="pop", color="continent",
# #   animation_frame="year", animation_group="country", range_y=[0,4000000000])
# # fig.show()

