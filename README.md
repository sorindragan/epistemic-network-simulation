# Epistemic Network Simulation

This code assists the paper present in the repository. The aim is to uncover insights into learning in epistemic networks comprised of scientists, policymakers, and journalists.

### Usage

Install the dependencies from requirements.txt.
```
pip install -r requirements.txt
```

```
Usage: python simulation.py [options]

Options:
  -h, --help            show this help message and exit
  -m NTYPE, --model=NTYPE
                        Possible network types: 'ring', 'random', 'ws', 'ba'.
  -n N, --nodes=N       Number of nodes in the network.
  -p P, --prob=P        Probability used in generating models.
  --m0=M0               Starting connected nodes for BA model.
  -a, --advanced        Add policymakers and journalists to the model.
  -s S, --scilinks=S    Percentage of the scientists connected with the other
                        nodes.
```

Example single run:
```
python simulation.py --model ba -n 100 -p 0.11 -s 0.1 -a
```

Experiment scripts are also available in the experiments/ directory. 
Each experiment script can be freely modified before each run.

Example experiment run:
```
bash experiment_*.sh
```
