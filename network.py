import itertools
import numpy.random as rand
import networkx as nx
from netwulf import visualize

from node import ScientistNode



def generate_random_network(N=10, p=0.11):
    """
        N = number of nodes in the network
        p = probability of a link between 2 nodes

        For p > 1/N, the network is in the supercritical regime
    """
    G = nx.Graph()
    node_list = [ScientistNode(i) for i in range(1, N+1)]
    node_ids = [node.id for node in node_list]

    G.add_nodes_from(node_ids)
    for i, j in itertools.product(node_ids, node_ids):
        if i == j:
            continue

        # add edge
        if rand.uniform(0, 1) < p:
            G.add_edge(i, j)
            node_list[i-1].add_neighbour(node_list[j-1])
    
    visualize_network(G=G)

def visualize_network(G=None):
    if G is None:
        # purely for exemplification purposes
        G = nx.Graph()
        G.add_node(1)
        G.add_nodes_from([2, 3])
        G.add_edge(1, 4)
        G.add_edges_from([(1, 2), (1, 3), (1, 4), (3, 4)])
    visualize(G)

