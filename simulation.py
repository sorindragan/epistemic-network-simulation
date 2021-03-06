import numpy as np
import numpy.random as rand
import networkx as nx
import matplotlib.pyplot as plt
from optparse import OptionParser
from netwulf import visualize, draw_netwulf

from node import JournalistNode, PolicymakerNode, ScientistNode
from network import generate_ring_lattice, generate_random_network, generate_watts_strogatz_network, generate_barabasi_albert_network

VERBOSE = True
MAX_STEPS = 25
EXPERIMENT = "policymakers_journalists"

def sanity_check():
    G = nx.Graph()
    s1 = ScientistNode(1)
    s2 = ScientistNode(2)
    s3 = ScientistNode(3)
    s4 = ScientistNode(4)

    p1 = PolicymakerNode(5)
    j1 = JournalistNode(6)

    # Belief stays the same after 25 iterations
    # s1.set_belief(0.49360896462333026)
    # s2.set_belief(0.42888114975493140)
    # s3.set_belief(0.22176380692356368)

    # Belief does not converge in 25 iterations
    # s1.set_belief(0.001)
    # s2.set_belief(0.0002)
    # s3.set_belief(0.5)

    # Interesting test -> The policy maker still converges
    s1.set_belief(0.55)
    s2.set_belief(0.6)
    s3.set_belief(0.1)
    s4.set_belief(0.1)

    s1.define_neighbours([s4, s2])
    s2.define_neighbours([s1, s3])
    s3.define_neighbours([s2, s4])
    s4.define_neighbours([s3, s1])
    G.add_edge(1, 2)
    G.add_edge(1, 4)
    G.add_edge(2, 3)
    G.add_edge(3, 4)

    p1.define_neighbours([s3, j1])
    j1.define_neighbours([s3, s4])
    G.add_edge(5, 3)
    G.add_edge(5, 1)
    G.add_edge(6, 3)
    G.add_edge(6, 4)
    
    # group colors
    for k, v in list(G.nodes(data=True))[:-2]:
        v['group'] = "blue"
    
    list(G.nodes(data=True))[-2][1]['group'] = "green"
    list(G.nodes(data=True))[-1][1]['group'] = "red"
    visualize(G)

    for n_ in [s1, s2, s3, s4, p1, j1]: 
        print(n_)

    average_beliefs = []
    average_beliefs.append({
        "label": "Aggregated Avg Belief",
        "values": [np.mean([s.belief for s in [s1, s2, s3, s4, p1, j1]])]
    })
    average_beliefs.append({
        "label": "Scientists Avg Belief",
        "values": [np.mean([s.belief for s in [s1, s2, s3, s4]])]
    })
    average_beliefs.append({
        "label": "Policymakers Avg Belief",
        "values": [p1.belief]
    })
    average_beliefs.append({
        "label": "Journalist Avg Belief",
        "values": [j1.belief]
    })

    timesteps = [0]
    for t_ in range(25):
        for s in [s1, s2, s3, s4, j1]:
            # print(s)
            s.act()

        for s in [s1, s2, s3, s4, j1, p1]:
            # print(s)
            s.update_belief()
        
        average_beliefs[0]["values"].append(
            np.mean([s.belief for s in [s1, s2, s3, s4, p1, j1]]))
        average_beliefs[1]["values"].append(
            np.mean([s.belief for s in [s1, s2, s3, s4]]))
        average_beliefs[2]["values"].append(p1.belief)
        average_beliefs[3]["values"].append(j1.belief)
        timesteps.append(t_+1)

    for n_ in [s1, s2, s3, s4, p1, j1]: 
        print(n_)
    
    generate_belief_graph('Convergence of average belief', timesteps, *average_beliefs)

def generate_belief_graph(filename,
                          title,
                          timesteps,
                          *args
                          ):
    """
        args must be a list with elements in the following format:
            type: dict
            argument["label"] = "Label Name"
            argument["values"] = list of len(timesteps)
    """
    # print(args)
    fig, ax = plt.subplots(1, figsize=(8, 6))
    fig.suptitle(title, fontsize=15)
    colors = ["black", "blue", "green", "red", "yellow", "pink"]
    for idx, avg_belief in enumerate(args):
        ax.plot(timesteps, avg_belief["values"], color=colors[idx], label=avg_belief["label"])

    plt.legend(loc="lower right", title="Lines Legend", frameon=False)
    plt.xlabel('Timesteps')
    plt.ylabel('Average Belief')    

    # plt.show()
    plt.savefig(f"results/{filename}.png")


def run_simulation(filename, nodes, advanced=False):
    timesteps = [0]
    average_beliefs = []
    if not advanced:
        average_beliefs.append({
            "label": "Scientists Average Belief",
            "values": [np.mean([s.belief for s in nodes])]
        })
    if advanced:
        average_beliefs.append({
            "label": "Aggregated Average Belief",
            "values": [np.mean([s.belief for s in nodes])]
        })
        average_beliefs.append({
             "label": "Scientists Average Belief",
             "values": [np.mean([s.belief for s in nodes[:-2]])]
         })
        average_beliefs.append({
            "label": "Policymaker Average Belief",
            "values": [nodes[-2].belief]
        })
        average_beliefs.append({
            "label": "Journalist Average Belief",
            "values": [nodes[-1].belief]
        })

    for t_ in range(MAX_STEPS):
        for n in nodes:
            if advanced and n == nodes[-2]:
                continue
            n.act()

        for n in nodes:
            n.update_belief()
        
        if not advanced:
            average_beliefs[0]["values"].append(
                np.mean([s.belief for s in nodes]))
        if advanced:
            average_beliefs[0]["values"].append(
                np.mean([s.belief for s in nodes]))
            average_beliefs[1]["values"].append(
                np.mean([s.belief for s in nodes[:-2]]))
            average_beliefs[2]["values"].append(nodes[-2].belief)
            average_beliefs[3]["values"].append(nodes[-1].belief)

        timesteps.append(t_+1)

    generate_belief_graph(filename, 'Convergence of average belief',
                          timesteps, *average_beliefs)


def add_policymaker_journalist(nodes, G, s):
    if s > 0.5:
        s = 0.5
    nodes_no = len(nodes)
    pmaker_neighbours_no = int(nodes_no * s) - 1
    journalist_neighbours_no = int(nodes_no * 2 * s) - 1

    if pmaker_neighbours_no == 0:
        pmaker_neighbours_no = 1
        journalist_neighbours_no = 2

    policymaker = PolicymakerNode(nodes_no + 1)
    journalist = JournalistNode(nodes_no + 2)
   
    # get the most connected percentage of scientists
    sorted_nodes = sorted(nodes, key=lambda n: len(n.neighbours), reverse=True)
    policymaker.define_neighbours(sorted_nodes[:pmaker_neighbours_no] + [journalist])
    for node in sorted_nodes[:pmaker_neighbours_no]:
        G.add_edge(nodes_no + 1, node.id)
    
    probs = [i for i in range(len(sorted_nodes))]
    journalist_neighbours = rand.choice(sorted_nodes, journalist_neighbours_no, 
                                        replace=False,
                                        p=np.array(probs)/sum(probs)
                                        )
    journalist.define_neighbours(journalist_neighbours)
    
    for node in journalist_neighbours:
        G.add_edge(nodes_no + 2, node.id)
     
    G.add_edge(nodes_no + 1, nodes_no + 2)
    nodes.append(policymaker)
    nodes.append(journalist)

    # add colors
    for k, v in list(G.nodes(data=True))[:-2]:
        v['group'] = "blue"

    list(G.nodes(data=True))[-2][1]['group'] = "green"
    list(G.nodes(data=True))[-1][1]['group'] = "red"

    return nodes, G

def main():
    parser = OptionParser()

    parser.add_option("-m", "--model", type="string", dest="ntype",
                    help="Possible network types: 'ring', 'random', 'ws', 'ba'.")
    parser.add_option("-n", "--nodes", type="int", dest="N",
                    help="Number of nodes in the network.")
    parser.add_option("-p", "--prob", type="float", dest="p",
                    help="Probability used in generating models.")
    parser.add_option("--m0", type="int", dest="m0",
                      help="Starting connected nodes for BA model.")
    parser.add_option("-a", "--advanced", action="store_true", dest="a", default=False,
                      help="Add policymakers and journalists to the model.")
    parser.add_option("-s", "--scilinks", type="float", dest="s",
                      help="Percentage of the scientists connected with the other nodes.")

    (options, args) = parser.parse_args()

    default_config = {
        # Input/output
        'zoom': 2,
        # Physics
        'node_charge': -45,
        'node_gravity': 0.1,
        'link_distance': 15,
        'link_distance_variation': 0,
        'node_collision': True,
        'wiggle_nodes': True,
        'freeze_nodes': False,
        # Nodes
        'node_fill_color': '#4e4fd4',
        'node_stroke_color': '#555555',
        'node_label_color': '#000000',
        'display_node_labels': True,
        'scale_node_size_by_strength': True,
        'node_size': 8,
        'node_stroke_width': 1.5,
        'node_size_variation': 0.8,
        # Links
        'link_color': '#7c7c7c',
        'link_width': 2,
        'link_alpha': 0.5,
        'link_width_variation': 0.5,
        # Thresholding
        'display_singleton_nodes': True,
        'min_link_weight_percentile': 0,
        'max_link_weight_percentile': 1
    }
    
    if VERBOSE: print(options)

    # Sanity check working fine
    # sanity_check()

    # Default values
    p   = 0.11
    N   = 20
    m0  = 2
    s   = 0.25

    if options.p:
        p = options.p
    
    if options.N:
        N = options.N
    
    if options.m0:
        m0 = options.m0
    
    if options.s:
        s = options.s
    
    # Scientists only simulation 
    if options.ntype and not options.a:
        if options.ntype == 'ring':
            # Ring Lattice
            nodes, G, config = generate_ring_lattice(N=N)
            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_graph"
            run_simulation(filename, nodes)

        if options.ntype == 'random':
            # Random Network
            nodes, G, config = generate_random_network(N=N, p=p)
            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_graph"
            run_simulation(filename, nodes)

        if options.ntype == 'ws':
            # Watts-Strogatz Network
            nodes, G, config = generate_watts_strogatz_network(N=N, p=p)
            _network, _ = visualize(G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_graph"
            run_simulation(filename, nodes)

        if options.ntype == 'ba':
            # Barabasi-Albert Network
            nodes, G, config = generate_barabasi_albert_network(N=N, m0=m0, m=m0)
            # visualize(G, config=default_config)
            _network, _ = visualize(G, config=default_config, plot_in_cell_below=False)
            # fig, ax = draw_netwulf(_network, figsize=(10, 10))
            fig, ax = draw_netwulf(_network)
            # plt.show()

            plt.savefig(f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_graph"
            run_simulation(filename, nodes)  

    ###################################################

    # Advanced simulation: Policymakers and Journalists
    if options.ntype and options.a:
        if options.ntype == 'ring':
            # Ring Lattice
            nodes, G, config = generate_ring_lattice(N=N)
            nodes, G = add_policymaker_journalist(nodes, G, s)

            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}_graph"
            run_simulation(filename, nodes, advanced=True)

        if options.ntype == 'random':
            # Random Network
            nodes, G, config = generate_random_network(N=N, p=p)
            nodes, G = add_policymaker_journalist(nodes, G, s)

            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}_graph"
            run_simulation(filename, nodes, advanced=True)

        if options.ntype == 'ws':
            # Watts-Strogatz Network
            nodes, G, config = generate_watts_strogatz_network(N=N, p=p)
            nodes, G = add_policymaker_journalist(nodes, G, s)

            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}_graph"
            run_simulation(filename, nodes, advanced=True)

        if options.ntype == 'ba':
            # Barabasi-Albert Network
            nodes, G, config = generate_barabasi_albert_network(
                N=N, m0=m0, m=m0)
            nodes, G = add_policymaker_journalist(nodes, G, s)

            _network, _ = visualize(
                G, config=default_config, plot_in_cell_below=False)
            fig, ax = draw_netwulf(_network)
            
            plt.savefig(
                f"results/{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}.png")
            filename = f"{EXPERIMENT}_{options.ntype}_{N}_{p}_{m0}_{s}_graph"
            run_simulation(filename, nodes, advanced=True)


if __name__ == '__main__':
    main()
