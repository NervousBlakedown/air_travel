# Imports
import networkx as nx
import pandas as pd
import random
import plotly.graph_objects as go
import numpy as np

def generate_airports(num_airports=10):
    return ['AIRPORT{}'.format(i) for i in range(num_airports)]

def generate_flights(airports, num_flights=5000):
    flights = []
    for _ in range(num_flights):
        arrival, destination = random.sample(airports, 2)
        connecting_flight = random.choice(airports)
        flights.append((arrival, destination, connecting_flight))
    return flights

def create_flight_network(airports, flights):
    G = nx.Graph()
    G.add_nodes_from(airports)
    for flight in flights:
        G.add_edge(*flight[:2], connecting_flight=flight[2])
    return G

def draw_3d_network(G, pos, flights_df):
    # Extract the node and edge positions and information
    edge_x = []
    edge_y = []
    edge_z = []
    edge_info = []  # Stores the text for edge hover information
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
        # Count the number of flights for this connection
        flights_count = flights_df[(flights_df['flight_arrival'] == edge[0]) & 
                                   (flights_df['flight_destination'] == edge[1])].shape[0]
        edge_info.append(f"{edge[0]} to {edge[1]}: {flights_count} flights")
    
    # Create a trace for the edges
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        text=edge_info,
        mode='lines')

    # Create a trace for the nodes
    node_x = []
    node_y = []
    node_z = []
    node_info = []  # Stores the text for node hover information
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        # Prepare the hover text with airport name and number of connections
        connections_count = len(list(G.neighbors(node)))
        node_info.append(f"{node}: {connections_count} connections")

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(size=10, line_width=2),
        hoverinfo='text',
        text=node_info)

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Network graph of flights',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://github.com/your-repo'>GitHub Repo</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    fig.show()

def generate_3d_positions(G, scale=1):
    # Use a 2D layout as basis
    base_pos = nx.spring_layout(G, dim=2, seed=42)
    
    # Initialize a dictionary for 3D positions
    pos_3d = {}
    
    # Add z-coordinate
    for node in G.nodes():
        pos_3d[node] = np.array([*base_pos[node], np.random.uniform(-scale, scale)])
    
    return pos_3d

# Init script
def main():
    try:
        num_airports = int(input("Enter number of airports and press enter: "))
        num_flights = int(input("Enter number of flights and press enter: "))
    except ValueError:
        print("Please enter a valid integer for both airports and flights.")
        return  # Exit the function if there was an input error

    airports = generate_airports(num_airports)
    flights = generate_flights(airports, num_flights)
    df = pd.DataFrame(flights, columns=['flight_arrival', 'flight_destination', 'connecting_flight_airport'])  # Correct variable name
    G = create_flight_network(airports, flights)
    pos_3d = generate_3d_positions(G)  # Generate 3D positions for the nodes
    draw_3d_network(G, pos_3d, df)  # Draw the 3D network

# Run script
if __name__ == "__main__":
    main()
