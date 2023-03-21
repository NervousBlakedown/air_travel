import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt

# Create a list of airport names
airports = ['JFK', 'LAX', 'ORD', 'DFW', 'SFO', 'MCO', 'SEA', 'DEN', 'ATL', 'BOS']

# Create a random dataset of flight connections
flights = []
for i in range(5000):
    arrival = random.choice(airports)
    destination = random.choice(airports)
    while arrival == destination:
        destination = random.choice(airports)
    connecting_flight = random.choice(airports)
    flights.append((arrival, destination, connecting_flight))

# Create a Pandas DataFrame from the flight data
df = pd.DataFrame(flights, columns=['flight_arrival', 'flight_destination', 'connecting_flight_airport'])

# Create a new network graph object
G = nx.Graph()

# Add nodes to the graph for each airport
for airport in airports:
    G.add_node(airport)

# Add edges to the graph for each flight connection
for index, row in df.iterrows():
    G.add_edge(row['flight_arrival'], row['flight_destination'], connecting_flight=row['connecting_flight_airport'])

# Define the positions of the nodes
pos = nx.spring_layout(G, seed=42)

# Draw the nodes and edges of the graph
nx.draw_networkx_nodes(G, pos, node_size=200, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.4)

# Label the nodes with their names
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')

# Label the edges with the connecting flight airports
edge_labels = nx.get_edge_attributes(G, 'connecting_flight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='red')

# Display the graph
plt.axis('off')
plt.title("Connecting Flight Locations")
plt.show()

