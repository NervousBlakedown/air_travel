import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt

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

def draw_flight_network(G):
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.4)
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'connecting_flight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_color='red')
    plt.axis('off')
    plt.title("Connecting Flight Locations")
    plt.show()

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
    df = pd.DataFrame(flights, columns=['flight_arrival', 'flight_destination', 'connecting_flight_airport'])
    G = create_flight_network(airports, flights)
    draw_flight_network(G)

if __name__ == "__main__":
    main()

