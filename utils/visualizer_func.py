import streamlit as st
from pyvis.network import Network
import pandas as pd
import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import json
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st

def visualize_dictionary_on_map(country_data):
    # Load the world shapefile using geopandas
    world_shp = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame.from_dict(country_data, orient='index', columns=['Value'])
    df.reset_index(inplace=True)
    df.columns = ['Country', 'Value']

    # Merge the DataFrame with the world shapefile based on country names
    world_data = world_shp.merge(df, left_on='name', right_on='Country', how='left')

    # Set up the Streamlit app
    st.title("World Map Visualization")
    st.write("Visualizing dictionary values on a world map")

    # Calculate the bounds based on the geometry of the mapped countries
    bounds = world_data.total_bounds.tolist()

    # Create a map centered on the average latitude and longitude
    map_center = [world_data['geometry'].centroid.y.mean(), world_data['geometry'].centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=2, min_zoom=2, max_bounds=True, max_bounds_viscosity=1.0,
                    control_scale=True, prefer_canvas=True)

    # Create a choropleth map using the dictionary values
    folium.Choropleth(
        geo_data=world_data,
        name='choropleth',
        data=world_data,
        columns=['Country', 'Value'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Value',
        nan_fill_color='white'  # Set the color for countries not listed in the dictionary to white
    ).add_to(m)

    # Set the map boundaries based on the calculated bounds
    m.fit_bounds(bounds)

    # Display the map in Streamlit
    folium_static(m)

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
                        'Instagram Follower #', 'Threads Follower #', 'TikTok Subscriber #',
                        'followers_count', 'following_count', 'tweet_num', 'followers_following_ratio']
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
        
        
def plot_filtered_language_bar_based_on_followers_of_each_platform(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)
    
def plot_filtered_language_follower_bar(df):
    # Filter bar
    all_languages_option = 'All Languages'
    selected_language = st.selectbox('Select a Language', [all_languages_option] + list(df['Language'].unique()))

    # Column selector
    selected_column = st.selectbox('Select a Column', ['X (Twitter) Follower #', 'Facebook Follower #', 'YouTube Subscriber #',
                            'Instagram Follower #', 'Threads Follower #', 'TikTok Subscriber #'])

    # Update DataFrame based on selected language
    if selected_language == all_languages_option:
        filtered_df = df
    else:
        filtered_df = df[df['Language'] == selected_language]

    # Filtered data series
    selected_column_series = filtered_df[selected_column]
    selected_column_series = selected_column_series.dropna()
    selected_column_series.sort_values(ascending=False, inplace=True)
    
    plot_filtered_language_bar_based_on_followers_of_each_platform(selected_column_series.index, selected_column_series.values, 
            title='Accounts Followers Based on Language', x_name='Accounts', y_name='Number of Followers')
    
def plot_language_focus_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)
    
    
def visualize_top_n_rows(df, selected_y_column, top_n):
    # Convert 'created_at' to datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Sort the DataFrame based on 'created_at'
    df.sort_values(by='created_at', inplace=True)

    # Display the bar plot with adjusted text size and orientation for the top n rows
    top_n_df = df.nlargest(top_n, selected_y_column)
    fig = px.bar(top_n_df, x='created_at', y=selected_y_column, labels={'created_at': 'Year of Creation', selected_y_column: 'Y-axis Column'}, text=top_n_df.index)
    fig.update_traces(textposition='outside', textfont_size=12, textangle=-90)

    st.plotly_chart(fig)