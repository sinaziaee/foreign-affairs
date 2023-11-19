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

bottom_left_column, bottom_mid, bottom_right_column = st.columns((20, 2, 20))

with bottom_left_column:
    st.header("Type of Twitter Accounts")
    temp_series = df['type'].value_counts(dropna=False)
    temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
    # find total and nan values
    temp_series, text = util_functions.find_account_category(temp_df, df)
    temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
    st.text(text)
    visualizer_func.create_pie_chart(temp_df, 'Value', 'Name', "")
    
with bottom_right_column:
    st.header("Twitter Verified Accounts")
    temp_series = df['is_blue_verified'].value_counts(dropna=False)
    temp_df = pd.DataFrame({'Name': ["Is Verified", "Is Not Verified", "N/A"], 'Value': list(temp_series.values)})
    visualizer_func.create_pie_chart(temp_df, 'Value', 'Name', "", text='Verified Accounts are the ones that are Blue Verified')



# top_left_column, top_mid, top_right_column = st.columns((15, 1, 10))

# with top_left_column:
# st.header("Social Media Platform Focus")
# st.write("Ratio of No. accounts in each platform per total accounts")
# col_1, col_2, col_3, col_4, col_5 = st.columns(5)
# # col_1, col_2 = st.columns(2)
# with col_1:
#     visualizer_func.plot_gauge(indicator_number=corp_dict['twitter']/corp_dict['total']*100, 
#                             indicator_color="#00f7ff", indicator_suffix="%", indicator_title=f"{corp_dict['twitter']} on Twitter", 
#                             max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['twitter_fol']))
# with col_2:
#     visualizer_func.plot_gauge(indicator_number=corp_dict['youtube']/corp_dict['total']*100,
#                             indicator_color="#ff0000", indicator_suffix="%", indicator_title=f"{corp_dict['youtube']} on Youtube", 
#                             max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['youtube_fol']))
# with col_3:
#     visualizer_func.plot_gauge(indicator_number=corp_dict['facebook']/corp_dict['total']*100,
#                             indicator_color="#0048ff", indicator_suffix="%", indicator_title=f"{corp_dict['facebook']} on Facebook", 
#                             max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['facebook_fol']))        
# with col_4:
#     visualizer_func.plot_gauge(indicator_number=corp_dict['instagram']/corp_dict['total']*100, 
#                             indicator_color="#e00bd2", indicator_suffix="%", indicator_title=f"{corp_dict['instagram']} on Instagram", 
#                             max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['instagram_fol']))        
# with col_5:
#     visualizer_func.plot_gauge(indicator_number=corp_dict['tiktok']/corp_dict['total']*100, 
#                             indicator_color="#0f0f0f", indicator_suffix="%", indicator_title=f"{corp_dict['tiktok']} on Tiktok", 
#                             max_bound=3, value=util_functions.generate_visual_numbers(corp_dict['tiktok_fol']))
        
import pandas as pd
import plotly.express as px

# with top_right_column:
#     st.header("The ratio of Followers per Accounts in each platform")
#     temp_dic = util_functions.load_file('findings\\follower_per_account_ratio.json')
#     # temp_df = pd.DataFrame({"value": list(temp_dic.values()), "title": list(temp_dic.keys())})
#     temp_df = pd.DataFrame(list(temp_dic.items()), columns=['Platform', 'Percentage'])
#     fig = px.pie(temp_df, values='Percentage', names='Platform')
#     st.plotly_chart(fig)

# with bottom_left_column:
#     st.header("Media Focus on Countries")
#     with open('assets/country_focus_count.json', 'r') as file:
#         temp_dic = json.load(file)

#     visualizer_func.visualize_dictionary_on_map(temp_dic)
    


