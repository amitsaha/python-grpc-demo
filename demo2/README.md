## Demo 2

Contents:

```
13:51 $ tree -L 1 grpc-services/
grpc-services/
├── Dockerfile.users
├── client_wrapper.py
├── config
├── docker-compose-infra.yml
├── docker-compose.yml
├── grpc_interceptors
├── protos
└── users

```

### Running the gRPC server

Build the docker image for the gRPC server:

```
$ cd grpc-services
$ docker build -t amitsaha/grpc-users -f Dockerfile.users .
$ docker run -ti amitsaha/grpc-users
```

Start the server along with statsd exporter, prometheus and grafana:

```bash
$ docker-compose -f docker-compse.yml -f docker-compose-infra.yml up
```

### Running the client


```bash
$ docker exec -ti users bash
# cd /client
# # run the sample_client_demo.py file 10 times
#  ./run-client.sh 10
```

