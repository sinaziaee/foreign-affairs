import streamlit as st
from utils import visualizer_func
import json


with open('findings/account_owner_parent.json', 'r') as file:
    temp_dic = json.load(file)
nodes = temp_dic['nodes']
edges = temp_dic['edges']
node_colors = temp_dic['node_colors']

st.set_page_config(page_title="Chinese Media Hierarchy of Corporation", page_icon=":bar_chart:", layout="wide")

visualizer_func.visualize_graph(nodes, edges, node_colors)