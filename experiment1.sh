#!/bin/bash
e=0.01
for n in 20 50 100 150 200
do
echo "$n nodes"
r=$(python -c "print(1/$n)")
p=`echo $r + $e | bc`
python simulation.py --model ba -n $n -p $p
done
exit 0