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
from folium.plugins import HeatMap


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


with open('assets/country_focus_count.json', 'r') as file:
    temp_dic = json.load(file)
    
visualize_dictionary_on_map(temp_dic)

################################################################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'
# loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

language_usage_series = df['Language'].value_counts()
# Generate and display the bar plot
plot_bar(language_usage_series.index, language_usage_series.values, 
                    title='Language Focus', x_name='Languages', y_name='Number of Accounts')

twitter_follower_series = df['X (Twitter) Follower #']
twitter_follower_series = twitter_follower_series.dropna()
twitter_follower_series.sort_values(ascending=False, inplace=True)
twitter_follower_series

plot_bar(twitter_follower_series.index, twitter_follower_series.values, 
                    title='Accounts Followers', x_name='Accounts', y_name='Number of Followers')


def filtered_plot(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'

# Loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

# Filter bar
selected_language = st.selectbox('Select a Language', df['Language'].unique())

# Update DataFrame based on selected language
filtered_df = df[df['Language'] == selected_language]

twitter_follower_series = filtered_df['X (Twitter) Follower #']
twitter_follower_series = twitter_follower_series.dropna()
twitter_follower_series.sort_values(ascending=False, inplace=True)

# Generate and display the bar plot
filtered_plot(twitter_follower_series.index, twitter_follower_series.values, 
            title='Accounts Followers Based on Language', x_name='Accounts', y_name='Number of Followers')


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'

# Loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

# Column selection filter bar
column_options = ['X (Twitter) Follower #', 'Facebook Follower #', 'YouTube Subscriber #',
                    'Instagram Follower #', 'Threads Follower #', 'TikTok Subscriber #']

selected_column = st.selectbox('Select a Column', column_options)

# Update DataFrame column based on selected column
df_column_name = 'X (Twitter) Follower #'
df_column_name = selected_column

twitter_follower_series = df[df_column_name]
twitter_follower_series = twitter_follower_series.dropna()
twitter_follower_series.sort_values(ascending=False, inplace=True)

# Generate and display the bar plot
plot_bar(twitter_follower_series.index, twitter_follower_series.values, 
            title=f'{str(selected_column).replace(" #", "")} Counter', x_name='Accounts', y_name='Number of Followers')


import streamlit as st
import pandas as pd
import plotly.express as px

def plot_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig)

df_path = 'dataset/state_media_on_social_media_platforms.xlsx'

# Loading the dataset
df = pd.read_excel(df_path, index_col='Name (English)')

# Column selection filter bar
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
    plot_bar(series.index, series.values,
            title=f'{column_name} Followers/Subscribers', x_name='Accounts', y_name='Number of Followers')

import streamlit as st
from pyvis.network import Network
import pandas as pd
import json

def visualize_graph(nodes, edges, node_colors):
    # Define the graph structure
    # nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    # edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'), ('D', 'H'), ('D', 'I')]

    # Create a Network instance
    nt = Network(notebook=True, height='500px', width='100%')

    # Add nodes to the graph with assigned colors
    for node in nodes:
        color = node_colors.get(node, 'lightblue')  # Default color if not found in mapping
        nt.add_node(node, color=color)

    # Add edges to the graph
    for edge in edges:
        nt.add_edge(edge[0], edge[1])

    # Display the graph using Streamlit
    nt.show('graph.html')
    st.components.v1.html(open('graph.html', 'r').read(), height=600)

with open('findings/account_owner_parent.json', 'r') as file:
    temp_dic = json.load(file)
nodes = temp_dic['nodes']
edges = temp_dic['edges']
node_colors = temp_dic['node_colors']
# Run the Streamlit app
visualize_graph(nodes, edges, node_colors)