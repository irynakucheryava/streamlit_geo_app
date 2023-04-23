import streamlit as st
import querry
from utils import list_concat
import pandas as pd
import plotly.express as px
import numpy as np



from CONSTANTS import YEAR, STATES, TABLE_DATA

def analytics_UI():
    st.title('Static analytics for chosen year')
    st.write("Some random shit")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox(
                "Year",
                YEAR,
                1,
            )
        with col2:
            button = st.button(label='Show analytics',
                               help='Select year and click the button')
    if button:
        ### total population by state
        cbg_states = querry.read_static(year, name="states", use_where=False)

        fd = querry.read_static(year, "description")
        # queting sex by age - 'Male_age'
        # table name and columns for actual data
        df_table = TABLE_DATA.format(year=year, table_id='B01')
        cols = list(fd.loc[fd['TABLE_TITLE'] == 'Sex By Age', 'TABLE_ID'])
        # read data
        df = querry.read_dataset(df_table, cols)
        # merging tstaes by CBG
        df_full = df.merge(cbg_states, on = 'CENSUS_BLOCK_GROUP')

        ### plotting total count by state and gender
        male_female_total = fd.loc[(fd['TABLE_ID'].isin(cols)) & (fd['FIELD_LEVEL_6'].isnull()), ['TABLE_ID', 'FIELD_LEVEL_5']]
        df_male_female = df_full[list(male_female_total['TABLE_ID']) + ['STATE']].copy()
        df_male_female.columns =  list(male_female_total['FIELD_LEVEL_5']) + ['STATE']
        df_male_female = df_male_female.groupby(by='STATE').sum().reset_index()
        df_male_female_melted = pd.melt(df_male_female, id_vars = ['STATE'], value_vars=['Male', 'Female'])
        fig = px.bar(df_male_female_melted, x = 'STATE', y = 'value', color='variable', color_discrete_map={'Male': 'hotpink', 'Female': 'darkviolet'})
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

        #### age and gender and race
        with st.container():
            col3, col4 = st.columns(2)
            with col3:
                t_mal_fem = df_male_female_melted.groupby('variable').sum('value').reset_index()
                pie = px.pie(t_mal_fem , values='value', names='variable', color='variable', color_discrete_map={'Male': 'khaki', 'Female': 'gold'})
                st.plotly_chart(pie, use_container_width=True, theme='streamlit')
            with col4:
                # age
                age_t_cols = fd.loc[(fd['TABLE_ID'].isin(cols)) & (np.invert(fd['FIELD_LEVEL_6'].isnull())), ['TABLE_ID', 'FIELD_LEVEL_6']]
                age_df = df_full[age_t_cols['TABLE_ID']]
                age_df.columns = list(age_t_cols['FIELD_LEVEL_6'])
                age_df = pd.DataFrame(age_df.sum()).reset_index()
                age_df.columns = ['Age', 'Count']
                pie1 = px.pie(age_df, values='Count', names='Age', color='Age', color_discrete_sequence=px.colors.sequential.Plasma)
                st.plotly_chart(pie1, use_container_width=True, theme='streamlit')
        with st.container():
            col5, col6 = st.columns(2)
            with col5:
                race = fd.loc[(fd['TABLE_TITLE'] == 'Race'), ['TABLE_ID','FIELD_LEVEL_5',  'FIELD_LEVEL_6']]
                race = race.loc[race['FIELD_LEVEL_6'].isnull(), ['TABLE_ID','FIELD_LEVEL_5']]
                df_table_r = TABLE_DATA.format(year=year, table_id='B02')
                df_race = querry.read_dataset(df_table_r, list(race['TABLE_ID']))
                df_race= df_race[list(race['TABLE_ID'])]
                df_race.columns = list(race['FIELD_LEVEL_5'])
                df_race = pd.DataFrame(df_race.sum().reset_index())
                df_race.columns = ['Race', 'Count']
                pie2 = px.pie(df_race, values='Count', names='Race', color='Race', color_discrete_sequence=px.colors.sequential.Plasma)
                pie2.update_layout(legend_font_size=8)
                st.plotly_chart(pie2, use_container_width=True, theme='streamlit')
















