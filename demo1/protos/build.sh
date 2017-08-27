#!/bin/bash

python -m grpc_tools.protoc \
    --proto_path=. \
    --python_out=../service \
    --grpc_python_out=../service \
    *.proto
