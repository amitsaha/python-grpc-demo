#!/bin/bash

# Add  grpc-interecptors to the PYTHONPATH
# Add ../prots/gen-py to the PYTHONPATH
PYTHONPATH=../protos/gen-py:../ python server/server.py
