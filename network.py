import itertools
import numpy as np
import numpy.random as rand
import networkx as nx
from netwulf import visualize

from node import ScientistNode

def generate_ring_lattice(N=10, ret=False):
    G = nx.Graph()
    node_list = [ScientistNode(i) for i in range(1, N+1)]
    node_ids = [node.id for node in node_list]

    for i in range(len(node_ids)):
        for t in [(i-2) % N, (i-1) % N, (i+1) % N, (i+2) % N]:
            G.add_edge(node_ids[i], node_ids[t])
            node_list[i].add_neighbour(node_list[t])
            node_list[t].add_neighbour(node_list[i])

    if ret:
        return G, node_list, node_ids
    
    styled_network, config = visualize_network(G=G)
    return node_list, G, config


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
            node_list[j-1].add_neighbour(node_list[i-1])
    
    styled_network, config = visualize_network(G=G)
    return node_list, G, config



def generate_watts_strogatz_network(N=10, p=0.11):
    """
        N = number of nodes in the initial ring network
        p = probability of a link between 2 nodes to be rewired

    """
    G, node_list, node_ids = generate_ring_lattice(N=N, ret=True)
    # I could probably do this faster...
    for node in node_list:
        idx = node_list.index(node)
        idx_neighbours = [node_list.index(n) for n in node.neighbours]
        for idx_n in idx_neighbours:
            if rand.uniform(0, 1) < p:
                # remove existing edge
                G.remove_edge(node_ids[idx], node_ids[idx_n])
                node.remove_neighbour(node_list[idx_n])
                node_list[idx_n].remove_neighbour(node)
                # rewire
                end_id = rand.choice(node_ids)
                # does not rewire to itself
                while end_id == idx:
                    end_id = rand.choice(node_ids)
                
                G.add_edge(node_ids[idx], node_ids[end_id])
                node.add_neighbour(node_list[end_id])
                node_list[end_id].add_neighbour(node)
                
    styled_network, config = visualize_network(G=G)
    return node_list, G, config


# also called scale-free model
def generate_barabasi_albert_network(N=10, m0=2, m=2):
    """
        N = number of ndoes in the final network
        m0 = starting number of randomly connected nodes with at least one link
        m = number of links created for each node inserted using prferential attachement
        
        Restriction: m <= m0
    """
    G = nx.Graph()
    node_list = [ScientistNode(i) for i in range(1, N+1)]
    node_ids = [node.id for node in node_list]

    G.add_nodes_from(node_ids)
    
    # initial network
    initial_node_list = node_list[:m0]
    initial_node_ids = node_ids[:m0]

    for i in range(len(initial_node_ids) - 1):
        G.add_edge(initial_node_ids[i], initial_node_ids[i+1])
        node_list[i].add_neighbour(node_list[i+1])
        node_list[i+1].add_neighbour(node_list[i])
    
    # preferential attachement
    for node in node_list[m0:]:
        idx = node_list.index(node)
        node_degrees = [len(n.neighbours) for n in node_list if n != node]
        probs = np.array(node_degrees) / sum(node_degrees)
        end_nodes = rand.choice([n for n in node_list if n != node], m, replace=False, p=probs)
        
        for end in end_nodes:
            node.add_neighbour(end)
            end.add_neighbour(node)
            end_idx = node_list.index(end)
            G.add_edge(idx, end_idx)

    styled_network, config = visualize_network(G=G)
    return node_list, G, config


def visualize_network(G=None):
    if G is None:
        # purely for exemplification purposes
        G = nx.Graph()
        G.add_node(1)
        G.add_nodes_from([2, 3])
        G.add_edge(2, 4)
        G.add_edges_from([(1, 2), (1, 3), (1, 4), (3, 4)])
        G.remove_edge(1, 3)
        print(list(G.nodes))
        print(list(G.edges))
    return visualize(G)

