
import numpy as np
import seaborn as sns
import streamlit as st

from matplotlib import pyplot as plt
from querry import read_analytics
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

from CONSTANTS import (
    YEAR, STATES,
    TABLE_INDEX
)


def clustering_UI():
    st.title("Clustering page")
    st.header("Build clusters out of census block groups based on selected features")
    with st.container():
        sel1, sel2 = st.columns(2)
        with sel1:
            year = st.selectbox(
                "Year",
                YEAR,
                1,
            )
            df = read_analytics(year=year)
            df.set_index(TABLE_INDEX, inplace=True, drop=True)
        with sel2:
            states = st.multiselect(
                label="State",
                options=['All'] + list(STATES.keys()),
                default='All',
            )
    with st.container():
        sel3, sel4 = st.columns(2)
        with sel3:
            features = st.multiselect(
                "Choose features for clustering (maximum 5)",
                options=df.columns[df.columns != "STATE"],
                default=None,
                max_selections=5,
            )
        with sel4:
            n_clusters = st.selectbox(
                "Select number of clusters from (2 - 5)",
                options=list(range(2, 6))
            )
        button = st.button(
            label='Show results',
            help='Select features and number of clusters and click the button'
        )
        if button:
            if 'All' in states:
                df_features = df[features]
            else:
                states_codes = [code for _, code in STATES.items() if _ in states]
                df_features = df.loc[df.STATE.isin(states_codes), features]
            df_features = df_features.astype('float')
            # remove outliers
            df_features_out = df_features[(np.abs(stats.zscore(df_features)) < 3).all(axis=1)].copy()
            # normalize
            scaler = MinMaxScaler()
            df_features_out[features] = scaler.fit_transform(df_features_out)
            # kmeans
            kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
            labels = kmeans.fit_predict(df_features_out)
            df_features_out['cluster'] = labels
            fig = sns.pairplot(data=df_features_out, hue='cluster')
            st.pyplot(fig)
    
