from node import ScientistNode
from network import generate_ring_lattice, generate_random_network, generate_watts_strogatz_network, generate_barabasi_albert_network

STEPS = 25

def sanity_check():
    s1 = ScientistNode(1)
    s2 = ScientistNode(2)
    s3 = ScientistNode(3)

    # Belief stays the same after 25 iterations
    # s1.set_belief(0.49360896462333026)
    # s2.set_belief(0.42888114975493140)
    # s3.set_belief(0.22176380692356368)

    # Belief does not converge in 25 iterations
    # s1.set_belief(0.001)
    # s2.set_belief(0.0002)
    # s3.set_belief(0.5)

    s1.define_neighbours([s2, s3])
    s2.define_neighbours([s1, s3])
    s3.define_neighbours([s1, s2])

    print(s1)
    print(s2)
    print(s3)

    for _ in range(25):
        for s in [s1, s2, s3]:
            s.act()

        for s in [s1, s2, s3]:
            s.update_belief()


    print(s1)
    print(s2)
    print(s3)

def run_simulation(nodes):
    print(nodes)
    for _ in range(STEPS):
        for n in nodes:
            n.act()

        for n in nodes:
            n.update_belief()
    print(nodes)
    

def main():
    # sanity_check()
    nodes = generate_ring_lattice(N=20)
    run_simulation(nodes)


    

if __name__ == '__main__':
    main()
