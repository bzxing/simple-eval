#!/bin/bash

for i in {1..10}
do
        echo "run $i"
        CONDUCTOR_IP="$1" python3.14 -m simple-evals.simple_evals --model emberglow-large_low --eval mmlu --n-repeats 8 --n-threads 8
done
