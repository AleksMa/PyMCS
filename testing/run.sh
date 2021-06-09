#!/bin/bash
for ((i=10; i < 1000; i+=10))
do
python3 test.py $i
../run.py test1.txt test1.txt 0.8 10 0
done