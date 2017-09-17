#!/bin/bash

declare -a services=("users")

# Python
# $ python -m pip install grcpio
# $ python -m pip install grpcio-tools

for SERVICE in "${services[@]}"; do
    DESTDIR='gen-py'
    mkdir -p $DESTDIR
    python -m grpc_tools.protoc \
        --proto_path=$SERVICE/ \
        --python_out=$DESTDIR \
        --grpc_python_out=$DESTDIR \
        $SERVICE/*.proto
done

# Golang
# Install protoc (https://github.com/google/protobuf/releases/tag/v3.4.0)
# Install go get -a github.com/golang/protobuf/protoc-gen-go

#for SERVICE in "${services[@]}"; do
#    DESTDIR='gen-go'
#    mkdir -p $DESTDIR
#    protoc \
#        --proto_path=$SERVICE/ \
#        --go_out=plugins=grpc:$DESTDIR \
#        $SERVICE/*.proto
#done
