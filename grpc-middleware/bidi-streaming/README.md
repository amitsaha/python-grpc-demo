# Identity service

An example gRPC service with a bidi streaming method + intereceptors

## Running the demos

Install poetry based on the instructions on the project [website](https://python-poetry.org).

### Install all dependencies 

```
poetry install
```

### Compile protobufs

```
$ cd service
$ poetry run python -m grpc_tools.protoc \
  --proto_path . --python_out=. --grpc_python_out=. \
  identity.proto
```

### Run server

```
$ cd server
$ TLS_CERT_PATH=../tls_certs/user_sessions/tls/server.crt \
  TLS_KEY_PATH=../tls_certs/user_sessions/tls/server.key \
  PYTHONPATH=../service poetry run python server.py
```


### Run client

```
$ cd client
$ PYTHONPATH=../service poetry run python client_stream_example.py
$ PYTHONPATH=../service poetry run python client_unary_unary_example.py
```

## Resources

- [gRPC Python API](https://grpc.github.io/grpc/python/grpc.html#)
