import dash
import dash_cytoscape as cyto
from dash import html
import networkx as nx
import random
from utils import util_functions
import math

# Create the Dash app
app = dash.Dash(__name__)
def visualize_graph(nodes, edges, node_colors):
    # Create a directed graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Find the central nodes using eigenvector centrality
    centrality = nx.eigenvector_centrality(G)
    central_nodes = sorted(centrality, key=centrality.get, reverse=True)[:10]  # Get top 10 central nodes

    # Calculate positions in a circle
    num_central_nodes = len(central_nodes)
    angle_increment = 2 * math.pi / num_central_nodes

    positions = {}
    for i, node in enumerate(central_nodes):
        angle = i * angle_increment
        x = 0.5 + 0.4 * math.cos(angle)  # Adjust radius as needed
        y = 0.5 + 0.4 * math.sin(angle) + 0.05 * random.uniform(-1, 1)  # Add a slight random offset
        positions[node] = {'x': x, 'y': y}

    # Create the Dash app
    app = dash.Dash(__name__)

    # Create the layout
    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'preset', 'positions': positions},
            style={'width': '100%', 'height': '100vh'},  # Set height to 100% of the viewport height
            elements=[
                {'data': {'id': node, 'label': node}, 'style': {'background-color': node_colors.get(node, 'lightblue')}}
                for node in nodes
            ] + [
                {'data': {'source': edge[0], 'target': edge[1]}}
                for edge in edges
            ]
        ),
    ])
    
    # Run the Dash app
    app.run_server(debug=True)
    
    
selected_options = ['Parent entity (English)', 'Entity owner (English)']

df, twi_df = util_functions.get_processed_merged_data()
# Example usage
nodes, edges, node_colors = util_functions.generate_graph(selected_options, df)


# Call the function to visualize the graph
visualize_graph(nodes, edges, node_colors)
