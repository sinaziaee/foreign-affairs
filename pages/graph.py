import streamlit as st
from utils import visualizer_func
import json
from utils import util_functions, visualizer_func

st.set_page_config(page_title="Graph Charts", page_icon=":bar_chart:", layout="wide")

df, twi_df = util_functions.get_processed_merged_data()

options = ['Name (English)', 'Entity owner (English)', 'Parent entity (English)', 'focus countries']

# Let the user select exactly two options using checkboxes
selected_options = st.multiselect('Select Options', options)

# Check the number of selected options
if len(selected_options) == 2:
    nodes, edges, node_colors = util_functions.generate_graph(selected_options, df)
    visualizer_func.visualize_graph(nodes, edges, node_colors)
    
else:
    st.warning('Please select exactly two options.')