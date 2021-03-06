#!/bin/bash
cd ..
e=0.01
for n in 20 50 100 150 250 500
do
echo "$n nodes"
r=$(python -c "print(1/$n)")
p=`echo $r + $e | bc`
python simulation.py --model ba -n $n -p $p
done
exit 0