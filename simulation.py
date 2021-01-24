from node import ScientistNode

def main():
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
        
        # s1.update_belief()
    
    print(s1)
    print(s2)
    print(s3)
        

if __name__ == '__main__':
    main()
