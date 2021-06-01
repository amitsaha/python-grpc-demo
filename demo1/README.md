## Demo 1

```
Package      Version
------------ -------
grpcio       1.38.0
grpcio-tools 1.38.0
pip          21.1.2
protobuf     3.17.1
setuptools   57.0.0
six          1.16.0
wheel        0.36.2
```

Contents:

```
$ tree -L 2 demo1
demo1
├── grpc-services
│   ├── client_wrapper.py
│   ├── protos
│   └── users
├── requirements.txt
└── webapp
    ├── app.py
    └── run-server.sh
```

- `grpc-services/protos`: `protobuf` definitions for a service `users`
- `grpc-services/users`: Sample client and server for the `users` service
- `grpc-services/client_wrapper.py`: A generic gRPC client wrapper
- `webapp`: A simple Flask application which interfaces with the `users` service


