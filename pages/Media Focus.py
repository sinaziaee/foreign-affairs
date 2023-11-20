import plotly.graph_objects as go
import streamlit as st
from utils import util_functions, visualizer_func
import json

st.set_page_config(page_title="Chinese Social Media", page_icon=":bar_chart:", layout="wide")
# st.title("Chinese Social Media Impact")
# with st.sidebar:
#     st.header("Configuration")
#     uploaded_file = st.file_uploader("Choose a file")

# if uploaded_file is None:
#     st.info(" Upload a file through config", icon="ℹ️")
#     st.stop()
top_left_column, top_mid, top_right_column = st.columns((1, 1, 2))
bottom_left_column, bottom_right_column = st.columns(2)
df, twi_df = util_functions.get_processed_merged_data()
corp_dict = util_functions.load_file('findings/corp_data.json')

with top_left_column:
    st.header("Media Focus on Countries")
    with open('assets/country_focus_count.json', 'r') as file:
        temp_dic = json.load(file)
    visualizer_func.visualize_dictionary_on_map(temp_dic)
    
with top_right_column:
    st.header("Media Focus on Language")
    language_usage_series = df['Language'].value_counts()
    visualizer_func.plot_language_focus_bar(language_usage_series.index, language_usage_series.values, 
                    title='Language Focus', x_name='Languages', y_name='Number of Accounts')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import pandas as pd
import plotly.express as px 


account_country_dict = util_functions.load_file('findings/platform_accounts_per_country.json')
followers_country_dict = util_functions.load_file('findings/follower_country.json')
corps_data = util_functions.load_file('findings/corp_data.json')

import streamlit as st
import plotly.graph_objects as go
import pandas as pd



df_left = pd.DataFrame(account_country_dict).T.reset_index()
df_right = pd.DataFrame(followers_country_dict).T.reset_index()
st.title('Chinese media Impact on each platform with focus on Each Country')
selected_country = st.selectbox('Select a country:', df_left['index'])
selected_data_left = df_left[df_left['index'] == selected_country]

selected_data_right = df_right[df_right['index'] == selected_country]

left, right = st.columns((1, 1))
with left:
    st.header("Social Media Accounts")
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
    st.header("Number of Followers")
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
    
    
bot_left, bot_right = st.columns((1, 1))

with bot_left:
    st.header("Ratio of Media Accounts")
    # Create a stacked bar chart
    fig = go.Figure()

    for platform in ['twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'threads']:
        fig.add_trace(go.Bar(
            x=[selected_country],
            y=100*(selected_data_left[platform]/corps_data[platform]),
            name=platform.capitalize()
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Country',
        yaxis_title='Ratio of Channels',
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

with bot_right:
    st.header("Number of Followers")
    # Create a stacked bar chart
    fig = go.Figure()

    for platform in ['twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'threads']:
        fig.add_trace(go.Bar(
            x=[selected_country],
            y=100*(selected_data_right[platform]/corps_data[f'{platform}_fol']),
            name=platform.capitalize()
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Country',
        yaxis_title='Number of Followers',
    )

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)