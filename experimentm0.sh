#!/bin/bash
e=0.01
n=100
for links in 1 2 5 10
do
echo "m0: $links"
r=$(python -c "print(1/$n)")
p=`echo $r + $e | bc`
python simulation.py --model ba -n $n -p $p --m0 $links
done
exit 0