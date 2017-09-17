## Demo 1

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


