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
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import util_functions


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
    # st.title("World Map Visualization")
    st.write("Visualizing the number of social Media Platforms on each country")

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
    
def display_country_info(selected_country_name, country_info_dict, df=None):
    # Function to display country information in a table
    st.write("Selected Country Information:")
    
    if selected_country_name in country_info_dict:
        country_info = country_info_dict[selected_country_name]
        
        temp_df = pd.DataFrame({'name': country_info['name'], 'owner': country_info['owner'], 'parent': country_info['parent']})
        temp_df
        st.dataframe(temp_df)
    else:
        st.write(f"No information available for {selected_country_name}")

def visualize_graph(nodes, edges, node_colors):
    nt = Network(notebook=True, height='500px', width='100%', directed=True)
    for node in nodes:
        color = node_colors.get(node, 'lightblue') 
        nt.add_node(node, color=color)

    for edge in edges:
        nt.add_edge(edge[0], edge[1])

    nt.show('graph.html')
    st.components.v1.html(open('graph.html', 'r').read(), height=1000)

def plot_follower_bar(x, y, title='Title', x_name='X', y_name='Y'):
    st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x=x_name, y=y_name)
    st.plotly_chart(fig, use_container_width=True)


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
    filtered_data = filtered_data.sort_values(by=df_columns, ascending=False)

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
    
    fig = px.bar(df, x=x_name, y=y_name, color_discrete_sequence=['#04c0b1'])
    st.plotly_chart(fig, use_container_width=True)
    
def plot_filtered_language_follower_bar(df):
    # Filter bar
    selected_language = st.selectbox('Select a Language', list(df['Language'].unique()))

    # Column selector
    selected_column = st.selectbox('Select a Column', ['X (Twitter) Follower #', 'Facebook Follower #', 'YouTube Subscriber #',
                            'Instagram Follower #', 'Threads Follower #', 'TikTok Subscriber #'])

    # Update DataFrame based on selected language
    filtered_df = df[df['Language'] == selected_language]

    # Filtered data series
    filtered_df = df[df['Language'] == selected_language]
    filtered_df = filtered_df[filtered_df[selected_column].notna()]
    filtered_df = filtered_df.set_index('Account Name')
    filtered_df = filtered_df.sort_values(selected_column, ascending=False)
    
    plot_filtered_language_bar_based_on_followers_of_each_platform(filtered_df.index, filtered_df[selected_column], 
            title='', x_name='Accounts', y_name='Number of Followers')

    # return selected_column_series
    
def plot_language_focus_bar(x, y, title='Title', x_name='X', y_name='Y'):
    # st.title(title)
    data = {x_name: x, y_name: y}
    df = pd.DataFrame(data)
    
    st.text('\n \n')
    st.text('\n \n')
    
    fig = px.bar(df, x=x_name, y=y_name)
    fig.update_layout(height=620)
    st.plotly_chart(fig, use_container_width=True)
    
def visualize_top_n_rows(df, selected_y_column, top_n):
    # Convert 'created_at' to datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Sort the DataFrame based on 'created_at'
    df.sort_values(by='created_at', inplace=True)

    # Display the bar plot with adjusted text size and orientation for the top n rows
    top_n_df = df.nlargest(top_n, selected_y_column)
    fig = px.bar(top_n_df, x='created_at', y=selected_y_column, labels={'created_at': 'Year of Creation', selected_y_column: 'Y-axis Column'}, text=top_n_df.index)
    fig.update_traces(textposition='outside', textfont_size=12, textangle=-90)

    st.plotly_chart(fig, use_container_width=True, height=800)
    
    
def create_pie_chart(data, column_value_name, column_title_name, title='Pie Chart', text=None):
    # Function to create a pie chart from data
    st.write(title)
    if text is not None:
        st.text(text)
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=[column_title_name, column_value_name])
    
    # Plot a pie chart using plotly
    fig = px.pie(df, names=column_title_name, values=column_value_name, title='')
    
    # Display the chart using st.plotly_chart
    st.plotly_chart(fig, use_container_width=True)
    
def create_donut_chart(data, column_value_name, column_title_name, title='Donut Chart', text=None):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Function to create a donut chart from data
    st.write(title)
    if text is not None:
        st.text(text)
    
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=[column_value_name, column_title_name])
    
    # Plot a donut chart
    plt.figure(figsize=(4, 4))
    plt.pie(df[column_value_name], labels=df[column_title_name], autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(width=0.3, edgecolor='w'))  # Set the width and edge color to create a donut
    plt.axis('equal')  # Equal aspect ratio ensures that donut is drawn as a circle.
    
    # Display the chart using st.pyplot
    st.pyplot(use_container_width=True)

def plot_metric(
    label,
    value,
    prefix="",
    suffix="",
):
    fig = go.Figure()
    
    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis":{"visible":False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            }
        )
    )
    chart_height=100
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True, use_container_height = True)
    
def plot_gauge(
    indicator_number,
    indicator_color,
    indicator_suffix,
    indicator_title,
    max_bound,
    value = 2000,
):
    max_bound = 80
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x":[0, 1], 
                    "y":[0,1]
            },
            number={"suffix": indicator_suffix,
                    "font.size": 22
            },
            gauge={"axis":{"range":[0, max_bound], "tickwidth": 1},
                    "bar": {"color": indicator_color},
            },
            title={"text": indicator_title,
                    "font": {"size": 18},
            },
        )
    )
    
    fig.add_annotation(
        x=0.5,
        y=0.2,
        text=f'{value} Followers',
        showarrow=False,
        font=dict(size=16),
    )
    
    fig.update_layout()
    st.plotly_chart(fig, use_container_width=True)