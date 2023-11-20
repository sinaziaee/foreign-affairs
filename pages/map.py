from utils import util_functions, visualizer_func
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="Chinese Social Media", page_icon=":bar_chart:", layout="wide")

account_country_dict = util_functions.load_file('findings/platform_accounts_per_country.json')
followers_country_dict = util_functions.load_file('findings/follower_country.json')

import streamlit as st
import plotly.graph_objects as go
import pandas as pd



df_left = pd.DataFrame(account_country_dict).T.reset_index()
df_right = pd.DataFrame(followers_country_dict).T.reset_index()
st.title('Stacked Bar Chart by Platform and Country')
selected_country = st.selectbox('Select a country:', df_left['index'])
selected_data_left = df_left[df_left['index'] == selected_country]

selected_data_right = df_right[df_right['index'] == selected_country]

left, right = st.columns((1, 1))
with left:
    # Create a stacked bar chart
    fig = go.Figure()

    for platform in ['twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'threads']:
        fig.add_trace(go.Bar(
            x=[selected_country],
            y=selected_data_left[platform],
            name=platform.capitalize()
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Country',
        yaxis_title='Number of Channels',
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

with right:
    # Create a stacked bar chart
    fig = go.Figure()

    for platform in ['twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'threads']:
        fig.add_trace(go.Bar(
            x=[selected_country],
            y=selected_data_right[platform],
            name=platform.capitalize()
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Country',
        yaxis_title='Number of Followers',
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

