import streamlit as st
from pyvis.network import Network
import pandas as pd
import json

def visualize_graph(nodes, edges, node_colors):
    # Create a Network instance with directed graph
    nt = Network(notebook=True, height='500px', width='100%', directed=True)

    # Add nodes to the graph with assigned colors
    for node in nodes:
        color = node_colors.get(node, 'lightblue')  # Default color if not found in mapping
        nt.add_node(node, color=color)

    # Add edges to the graph
    for edge in edges:
        nt.add_edge(edge[0], edge[1])
        # nt.add_edge(edge[1], edge[0])

    # Display the graph using Streamlit
    nt.show('graph.html')
    st.components.v1.html(open('graph.html', 'r').read(), height=600)


import streamlit as st
import pandas as pd
import plotly.express as px
from utils import util_functions

def plot_follower_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)


def plot_followers(df):
    column_options = ['X (Twitter) Follower #', 'Facebook Follower #', 'YouTube Subscriber #',
                        'Instagram Follower #', 'Threads Follower #', 'TikTok Subscriber #']
    selected_columns = st.multiselect('Select Columns', column_options)

    # Update DataFrame column based on selected columns
    df_columns = ['X (Twitter) Follower #']  # Default column(s)
    df_columns = selected_columns if selected_columns else df_columns

    # Filter and process data for selected columns
    filtered_data = df[df_columns]
    filtered_data = filtered_data.dropna()
    filtered_data.sort_values(by=df_columns, ascending=False, inplace=True)

    # Generate and display the bar plot for each selected column
    for column in df_columns:
        column_name = column.replace(' #', '')
        series = filtered_data[column]
        plot_follower_bar(series.index, series.values,
                title=f'{column_name} Followers/Subscribers', x_name='Accounts', y_name='Number of Followers')