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

# def visualize_dictionary_on_map(country_data):
#     # Load the world shapefile using geopandas
#     world_shp = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#     # Convert the dictionary to a pandas DataFrame
#     df = pd.DataFrame.from_dict(country_data, orient='index', columns=['Value'])
#     df.reset_index(inplace=True)
#     df.columns = ['Country', 'Value']

#     # Merge the DataFrame with the world shapefile based on country names
#     world_data = world_shp.merge(df, left_on='name', right_on='Country', how='left')

#     # Set up the Streamlit app
#     st.title("World Map Visualization")
#     st.write("Visualizing dictionary values on a world map")

#     # Display the world map with choropleth
#     fig, ax = plt.subplots(figsize=(12, 8))
#     world_data.plot(column='Value', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
#     plt.title("Dictionary Values on World Map")
#     plt.axis('off')

#     # Show the map in Streamlit
#     st.pyplot(fig)

# def visualize_dictionary_on_map(country_data):
#     # Load the world shapefile using geopandas
#     world_shp = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#     # Compute centroids of country geometries
#     world_shp['centroid'] = world_shp['geometry'].centroid
#     world_shp['latitude'] = world_shp['centroid'].y
#     world_shp['longitude'] = world_shp['centroid'].x

#     # Convert the dictionary to a pandas DataFrame
#     df = pd.DataFrame.from_dict(country_data, orient='index', columns=['Value'])
#     df.reset_index(inplace=True)
#     df.columns = ['Country', 'Value']

#     # Merge the DataFrame with the world shapefile based on country names
#     world_data = world_shp.merge(df, left_on='name', right_on='Country', how='left')

#     # Set up the Streamlit app
#     st.title("World Map Visualization")
#     st.write("Visualizing dictionary values on a world map")

#     # Display the world map with choropleth using Streamlit's map feature
#     st.map(world_data)

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


# Example usage
# country_data = {
#     'Australia': 10,
#     'Canada': 20,
#     'China': 15,
#     'India': 25,
#     'United States': 30
# }

# visualize_dictionary_on_map(country_data)
    
with open('temp3.json', 'r') as file:
    temp_dic = json.load(file)

# visualize_country_counts(temp_dic)

visualize_dictionary_on_map(temp_dic)
