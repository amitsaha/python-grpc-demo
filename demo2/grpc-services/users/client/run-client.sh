#!/bin/bash

for i in $(seq 1 $1); do
    PYTHONPATH=../../protos/gen-py/ python sample_client_demo.py &
done

