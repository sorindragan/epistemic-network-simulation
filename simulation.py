import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
from netwulf import visualize

from node import JournalistNode, PolicymakerNode, ScientistNode
from network import generate_ring_lattice, generate_random_network, generate_watts_strogatz_network, generate_barabasi_albert_network

STEPS = 25

def sanity_check():
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
    p1.define_neighbours([s3, j1])
    j1.define_neighbours([s3, s4])

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

def generate_belief_graph(title,
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

    plt.legend(loc="upper left", title="Lines Legend", frameon=False)
    plt.show()

def run_simulation(nodes):
    timesteps = [0]
    average_beliefs = []
    average_beliefs.append({
        "label": "Scientists Average Belief",
        "values": [np.mean([s.belief for s in nodes])]
    })

    for t_ in range(STEPS):
        for n in nodes:
            n.act()

        for n in nodes:
            n.update_belief()
        
        average_beliefs[0]["values"].append(
            np.mean([s.belief for s in nodes]))
        timesteps.append(t_+1)

    generate_belief_graph('Convergence of average belief',
                          timesteps, *average_beliefs)


def main():

    # parser = OptionParser()

    # parser.add_option("-f", "--file", dest="filename",
    #                 help="write report to FILE", metavar="FILE")
    # parser.add_option("-q", "--quiet",
    #                 action="store_false", dest="verbose", default=True,
    #                 help="don't print status messages to stdout")

    # (options, args) = parser.parse_args()


    # sanity_check()

    # Ring Lattice
    # nodes, G, config = generate_ring_lattice(N=20)
    # visualize(G, config=config)
    # run_simulation(nodes)

    # Random Network
    nodes, G, config = generate_random_network(N=50)
    visualize(G, config=config)
    run_simulation(nodes)
    

if __name__ == '__main__':
    main()
