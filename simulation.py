import numpy as np
import matplotlib.pyplot as plt

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



    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(p1)
    print(j1)

    average_belief_all = [np.mean([s.belief for s in [s1, s2, s3, s4, p1, j1]])]
    average_belief_scientists = [np.mean([s.belief for s in [s1, s2, s3, s4]])]
    average_belief_policymakers = [p1.belief]
    average_belief_journalist = [j1.belief]
    timesteps = [0]

    for t_ in range(25):
        for s in [s1, s2, s3, s4, j1]:
            # print(s)
            s.act()

        for s in [s1, s2, s3, s4, j1, p1]:
            # print(s)
            s.update_belief()
        
        average_belief_all.append(
            np.mean([s.belief for s in [s1, s2, s3, s4, p1, j1]]))
        average_belief_scientists.append(
            np.mean([s.belief for s in [s1, s2, s3, s4]]))
        average_belief_policymakers.append(p1.belief)
        average_belief_journalist.append(j1.belief)
        timesteps.append(t_+1)

    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(p1)
    print(j1)

    fig, ax = plt.subplots(1, figsize=(8, 6))
    fig.suptitle('Convergence of average belief', fontsize=15)
    ax.plot(timesteps, average_belief_all, color="black", label="Aggregated Avg Belief")
    ax.plot(timesteps, average_belief_scientists, color="blue", label="Scientists Avg Belief")
    ax.plot(timesteps, average_belief_policymakers, color="green", label="Policymakers Avg Belief")
    ax.plot(timesteps, average_belief_journalist, color="red", label="Journalist Avg Belief")
    plt.legend(loc="upper left", title="Lines Legend", frameon=False)
    plt.show()


def run_simulation(nodes):
    print(nodes)
    for _ in range(STEPS):
        for n in nodes:
            n.act()

        for n in nodes:
            n.update_belief()
    print(nodes)
    

def main():
    sanity_check()
    # nodes = generate_ring_lattice(N=20)
    # run_simulation(nodes)


    

if __name__ == '__main__':
    main()
