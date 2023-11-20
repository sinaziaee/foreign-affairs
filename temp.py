import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import visualizer_func
from utils import util_functions 
import json
import pandas as pd

with open('assets/country_focus_count.json', 'r') as file:
    temp_dic = json.load(file)

# visualizer_func.visualize_dictionary_on_map(temp_dic)
    
with open('findings/country_corps.json', 'r') as file:
    country_info_dict = json.load(file)

# selected_country_name = st.selectbox('Select a Country', list(country_info_dict.keys()))

# Display country information in a table based on the selected country
# visualizer_func.display_country_info(selected_country_name, country_info_dict)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
# loading the dataset
df, twi_df = util_functions.get_processed_merged_data()

language_usage_series = df['Language'].value_counts()
# visualizer_func.plot_language_focus_bar(language_usage_series.index, language_usage_series.values, 
                    # title='Language Focus', x_name='Languages', y_name='Number of Accounts')


visualizer_func.plot_filtered_language_follower_bar(df)


visualizer_func.plot_followers(df)

with open('findings/account_owner_parent.json', 'r') as file:
    temp_dic = json.load(file)
nodes = temp_dic['nodes']
edges = temp_dic['edges']
node_colors = temp_dic['node_colors']

# visualizer_func.visualize_graph(nodes, edges, node_colors)


import pandas as pd
import streamlit as st
import plotly.express as px

df, twi_df = util_functions.get_processed_merged_data()

# twitter_dir_path = 'dataset/twitter_accounts_info.csv'
# twi_df = pd.read_csv(twitter_dir_path, index_col='user_id')
# twi_df['followers_following_ratio'] = twi_df['followers_count'] / (twi_df['following_count'] + 1e-8)
####################################################################################
# Allow user to select y-axis column
# selected_y_column = st.selectbox('Select a Column for Y-axis', ['followers_count', 'following_count', 'tweet_num', 'followers_following_ratio'])
# # Allow user to choose the top n rows
# top_n = st.slider('Select Top N Rows', min_value=1, max_value=len(twi_df), value=100)
# # Call the function to visualize the top n rows
# visualizer_func.visualize_top_n_rows(twi_df, selected_y_column, top_n)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np


# temp_series = df['is_blue_verified'].value_counts(dropna=False)
# temp_df = pd.DataFrame({'Name': ["Is Verified", "Is Not Verified", "N/A"], 'Value': list(temp_series.values)})
# # Convert the DataFrame to a list of dictionaries for animation frames
# # Store the animation in a variable

# visualizer_func.create_pie_chart(temp_df, 'Value', 'Name', "Verified Accounts")


# temp_series = df['type'].value_counts(dropna=False)
# temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
# # find total and nan values
# temp_series, text = util_functions.find_account_category(temp_df, df)
# temp_df = pd.DataFrame({'Name': list(temp_series.index), 'Value': list(temp_series.values)})
# st.text(text)
# visualizer_func.create_pie_chart(temp_df, 'Value', 'Name', "Type of Business accounts")


