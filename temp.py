import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import visualizer_func
import json
import pandas as pd

with open('assets/country_focus_count.json', 'r') as file:
    temp_dic = json.load(file)
    
visualizer_func.visualize_dictionary_on_map(temp_dic)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
# loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

language_usage_series = df['Language'].value_counts()
visualizer_func.plot_language_focus_bar(language_usage_series.index, language_usage_series.values, 
                    title='Language Focus', x_name='Languages', y_name='Number of Accounts')


visualizer_func.plot_filtered_language_follower_bar(df)


visualizer_func.plot_followers(df)

with open('findings/account_owner_parent.json', 'r') as file:
    temp_dic = json.load(file)
nodes = temp_dic['nodes']
edges = temp_dic['edges']
node_colors = temp_dic['node_colors']

visualizer_func.visualize_graph(nodes, edges, node_colors)