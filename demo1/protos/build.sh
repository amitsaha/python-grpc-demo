#!/bin/bash

declare -a services=("users")

# Python
# $ pip install grpcio-tools

for SERVICE in "${services[@]}"; do
    DESTDIR='gen-py'
    mkdir -p $DESTDIR/$SERVICE
    touch $DESTDIR/$SERVICE/__init__.py
    python -m grpc_tools.protoc \
        --proto_path=$SERVICE/ \
        --python_out=$DESTDIR/$SERVICE \
        --grpc_python_out=$DESTDIR/$SERVICE \
        $SERVICE/*.proto
done

# Golang
# Install protoc
# Install go get -a github.com/golang/protobuf/protoc-gen-go

for SERVICE in "${services[@]}"; do
    DESTDIR='gen-go'
    mkdir -p $DESTDIR/$SERVICE
    protoc \
        --proto_path=$SERVICE/ \
        --go_out=plugins=grpc:$DESTDIR/$SERVICE \
        $SERVICE/*.proto
done
