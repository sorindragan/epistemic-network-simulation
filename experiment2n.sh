#!/bin/bash
e=0.01
s=0.1
for n in 20 50 100 150 250 500
do
echo "$n nodes"
r=$(python -c "print(1/$n)")
p=`echo $r + $e | bc`
python simulation.py --model ba -n $n -p $p -s $s -a
done
exit 0