import streamlit as st
import querry
import pandas as pd
import plotly.express as px
from analytics_utils import data_count
from CONSTANTS import YEAR, STATES, TABLE_DATA


def analytics_UI():
    st.title(' 👨‍👩‍👧‍👦 Demographic Statistics')
    st.header('''Create an interactive dashboard visualising US demographics''')
    st.markdown('#')
    st.write(
        """
        The dashboard contains a selection of plots showcasing default variables.
        You can interact with plots by unselecting categories or by selecting areas of interest.
        """)
    # parameter selection
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.selectbox(
                label="Year",
                options=YEAR,
                index=1,
            )
        with col2:
            state = st.selectbox(
                label="State",
                options=['All'] + list(STATES.values()),
                index=0,
            )
        with col3:
            st.markdown('#')
            button = st.button(
                label='Show analytics',
                help='Select year and click the button',
                use_container_width=True
            )
    if button:
        st.markdown('#')
        st.markdown("""---""")
        st.markdown('#')
        st.header('''Basic population demographics''')
        st.markdown('#')

        # importing data and field description
        data = querry.read_analytics(year)
        # gender plot
        if state == 'All':
            # plotting population by state and gender
            gender_state = data[['STATE', 'sex_males', 'sex_females']].groupby(
                by='STATE').sum().reset_index().copy()
            gender_state = pd.melt(
                gender_state,
                id_vars = ['STATE'],
                value_vars=['sex_males', 'sex_females']
            )
            gender_state['variable'] = gender_state['variable'].str.replace('sex_', '')
            fig = px.bar(
                gender_state,
                x='STATE', y='value',
                color='variable',
                # color_discrete_map={'FEMALES': 'mediumpurple',
                #                     'MALES': 'indigo'})
                color_discrete_sequence=px.colors.sequential.Agsunset,
                height=600
            )
            fig.update_layout(
                title={
                    'text': 'Population by state and gender',
                    #'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    #'yanchor': 'top'
                }
            )
            st.plotly_chart(fig, use_container_width=True, theme='streamlit')
        else:
            data = data.loc[data['STATE'] == state, :]

        with st.container():
            st.markdown('#')
            st.markdown('#')
            col3, col4, col5 = st.columns(3)
            with col3:
                # gender
                gender_df = data_count(
                    data=data,
                    col='sex',
                    col_name='Gender'
                )
                pie = px.pie(
                    gender_df,
                    values='Count',
                    names='Gender',
                    color='Gender',
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                pie.update_layout(
                    legend_font_size=9,
                    legend=dict(
                        orientation="v",
                        itemwidth=50,
                        xanchor="right",
                        x=0.9,
                    ),
                    title={
                        'text': 'Population by Gender',
                        'x': 0.5,
                        'xanchor': 'center',
                    }
                )
                st.plotly_chart(pie, use_container_width=True, theme='streamlit')
            with col4:
                # age
                age_df = data_count(
                    data=data,
                    col='age',
                    col_name='Age'
                )
                pie1 = px.pie(
                    age_df,
                    values='Count',
                    names='Age',
                    color='Age',
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                pie1.update_layout(
                    legend_font_size=9,
                    legend=dict(
                        orientation="v",
                        itemwidth=50,
                        xanchor="right",
                        x=1
                    ),
                    title={
                        'text': 'Population by Age',
                        'x': 0.5,
                        'xanchor': 'center',
                    }
                )
                st.plotly_chart(pie1, use_container_width=True, theme='streamlit')

            with col5:
                # race
                race_df = data_count(
                    data=data,
                    col='race',
                    col_name='Race'
                )

                pie2 = px.pie(
                    race_df,
                    values='Count',
                    names='Race',
                    color='Race',
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                pie2.update_layout(
                    legend_font_size=9,
                    legend=dict(
                        orientation="v",
                        itemwidth=50,
                        xanchor="right",
                        x=1.1
                    ),
                    title={
                        'text': 'Population by Race',
                        'x': 0.5,
                        'xanchor': 'center',
                    }
                )
                st.plotly_chart(pie2, use_container_width=True, theme='streamlit')
        st.markdown('#')
        st.markdown('#')
        st.markdown("""---""")
        st.markdown('#')
        st.header('''Living conditions''')
        st.markdown('#')
        with st.container():
            col6, col7 = st.columns(2)
            with col6:
                house_df = data_count(
                    data=data,
                    col='household',
                    col_name='Type'
                )

                fig1 = px.bar(
                    house_df,
                        y='Type',
                        x='Count',
                        color='Type',
                        color_discrete_map={
                            'female householder': 'mediumpurple',
                            'male householder': 'mediumslateblue',
                            'married couple': 'indigo',
                            'cohabiting couple': 'mediumorchid'
                        },
                    )
                fig1.update_layout(
                    legend_font_size=9,
                    legend=dict(
                        orientation="v",
                        itemwidth=50,
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1.1
                    ),
                    title={
                        'text': 'Type of Household',
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                    }
                    )
                fig1.update_yaxes(showticklabels=False)
                st.plotly_chart(fig1, use_container_width=True, theme='streamlit')

            with col7:
                occupancy_df = data_count(
                    data=data,
                    col='occupancy',
                    col_name='Type'
                )

                pie3 = px.pie(
                    occupancy_df,
                    values='Count',
                    names='Type',
                    color='Type',
                    color_discrete_sequence=px.colors.sequential.Agsunset
                )
                pie3.update_layout(
                    legend_font_size=9,
                    legend=dict(
                        orientation="v",
                        itemwidth=50,
                        xanchor="right",
                        x=0.8
                    ),
                    title={
                        'text': 'Occupancy Status of Housing Unit',
                        'x': 0.5,
                        'xanchor': 'center',
                    }
                )
                st.plotly_chart(pie3, use_container_width=True, theme='streamlit')

            st.markdown('#')
            value_df = data_count(
                data=data,
                col='value',
                col_name='Type'
            )
            fig2 = px.bar(
                value_df,
                x='Type',
                y='Count',
                color='Type',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                height=600,
            )
            fig2.update_layout(
                title={
                    'text': 'Housing Value',
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
        st.header('''Education and Income''')
        st.markdown('#')
        with st.container():
            col9, col10, col11  = st.columns(3)
            with col9:
                education_df = data_count(
                    data=data,
                    col='education',
                    col_name='Type'
                )

                fig3 = px.bar(
                    education_df,
                    x='Type',
                    y='Count',
                    color='Type',
                    color_discrete_sequence=px.colors.sequential.Agsunset
                )
                fig3.update_layout(
                    title={
                        'text': 'Type of Education',
                        'x': 0.5,
                        'xanchor': 'center',
                        },
                    legend_font_size=9,
                    xaxis_title=None
                )
                fig3.update_xaxes(showticklabels=False)
                st.plotly_chart(fig3, use_container_width=True, theme='streamlit')

                with col10:
                    income_df = data_count(
                        data=data,
                        col='income',
                        col_name='Type'
                    )

                    pie4 = px.pie(
                        income_df,
                        values='Count',
                        names='Type',
                        color='Type',
                        color_discrete_sequence=px.colors.sequential.Agsunset
                    )
                    pie4.update_layout(
                        legend_font_size=9,
                        legend=dict(
                            orientation="v",
                            itemwidth=50,
                            xanchor="right",
                            x=1
                        ),
                        title={
                            'text': 'Household Income',
                            'x': 0.5,
                            'xanchor': 'center',
                        }
                    )
                    st.plotly_chart(pie4, use_container_width=True, theme='streamlit')
                with col11:
                    travel_df = data_count(
                        data=data,
                        col='time_to_work',
                        col_name='Time'
                    )
                    pie5 = px.pie(
                        travel_df,
                        values='Count',
                        names='Time',
                        color='Time',
                        color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    pie5.update_layout(
                        legend_font_size=9,
                        legend=dict(
                            orientation="v",
                            itemwidth=50,
                            xanchor="right",
                            x=1.1
                        ),
                        title={
                            'text': 'Travel Time to Work',
                            'x': 0.5,
                            'xanchor': 'center',
                        }
                    )
                    st.plotly_chart(pie5, use_container_width=True, theme='streamlit')

