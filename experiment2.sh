#!/bin/bash
e=0.01
n=100
for s in 0.01 0.05 0.1 0.2 0.5
do
echo "$s links to scientists"
r=$(python -c "print(1/$n)")
p=`echo $r + $e | bc`
python simulation.py --model random -n $n -p $p -s $s -a
done
exit 0