#!/bin/bash

for i in {1..10}
do
        echo "run $i"
        CONDUCTOR_IP="$1" /opt/homebrew/bin/python3.13 -m simple-evals.simple_evals --model emberglow-large_low --eval gpqa --n-repeats 8 --n-threads 8
done
