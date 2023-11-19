import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import visualizer_func
import json
import pandas as pd

with open('assets/country_focus_count.json', 'r') as file:
    temp_dic = json.load(file)
    
# visualizer_func.visualize_dictionary_on_map(temp_dic)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
# loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

language_usage_series = df['Language'].value_counts()
# visualizer_func.plot_language_focus_bar(language_usage_series.index, language_usage_series.values, 
                    # title='Language Focus', x_name='Languages', y_name='Number of Accounts')


# visualizer_func.plot_filtered_language_follower_bar(df)


# visualizer_func.plot_followers(df)

with open('findings/account_owner_parent.json', 'r') as file:
    temp_dic = json.load(file)
nodes = temp_dic['nodes']
edges = temp_dic['edges']
node_colors = temp_dic['node_colors']

# visualizer_func.visualize_graph(nodes, edges, node_colors)


import pandas as pd
import streamlit as st
import plotly.express as px

twitter_dir_path = 'dataset/twitter_accounts_info.csv'
twi_df = pd.read_csv(twitter_dir_path, index_col='user_id')

# twi_df = twi_df.sort_values('followers_count', ascending=False)
twi_df['followers_following_ratio'] = twi_df['followers_count'] / (twi_df['following_count'] + 1e-8)
####################################################################################

# Convert 'created_at' to datetime format
twi_df['created_at'] = pd.to_datetime(twi_df['created_at'])

# Sort the DataFrame based on 'created_at'
twi_df.sort_values(by='created_at', inplace=True)

# Streamlit app
st.title('Twitter Data Visualization')

# Allow user to select y-axis column
selected_y_column = st.selectbox('Select a Column for Y-axis', ['followers_count', 'following_count', 'tweet_num', 'followers_following_ratio'])

# Allow user to choose the top n rows
top_n = st.slider('Select Top N Rows', min_value=1, max_value=len(twi_df), value=100)

# Display the bar plot with adjusted text size and orientation for the top n rows
top_n_df = twi_df.nlargest(top_n, selected_y_column)
fig = px.bar(top_n_df, x='created_at', y=selected_y_column, labels={'created_at': 'Year of Creation', selected_y_column: 'Y-axis Column'}, text=top_n_df.index)
fig.update_traces(textposition='outside', textfont_size=12, textangle=-90)

st.plotly_chart(fig)