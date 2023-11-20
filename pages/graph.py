import streamlit as st
from utils import visualizer_func
import json
from utils import util_functions, visualizer_func
import pandas as pd

st.set_page_config(page_title="Graph Charts", page_icon=":bar_chart:", layout="wide")

df, twi_df = util_functions.get_processed_merged_data()

import streamlit as st

# Define options
options = ['Name (English)', 'Entity owner (English)', 'Parent entity (English)', 'Focus countries']

# Let the user select exactly two options using checkboxes
selected_options = st.multiselect('Select Options', options)

# Apply custom styles using HTML and CSS
style = """
    <style>
        .custom-option {
            display: flex;
            align-items: center;
        }
        .custom-checkbox {
            margin-right: 10px;
        }
    </style>
"""

# Render custom styles using the st.markdown function
st.markdown(style, unsafe_allow_html=True)

# Check the number of selected options
if len(selected_options) == 2:
    nodes, edges, node_colors = util_functions.generate_graph(selected_options, df)
    color_code = {
        'Name (English)': '#04c0b1',
        'Entity owner (English)': '#274d4a',
        'Parent entity (English)': '#088fbc',
        'focus countries': '#e87551'
    }
    for option in selected_options:
        color = color_code.get(option, '#888888')  # Default to gray if color not specified
        st.markdown(f'<div class="custom-option" style="color: {color};"><input type="checkbox" class="custom-checkbox" checked disabled>{option}</div>', unsafe_allow_html=True)

    visualizer_func.visualize_graph(nodes, edges, node_colors)
else:
    st.warning('Please select exactly two options.')