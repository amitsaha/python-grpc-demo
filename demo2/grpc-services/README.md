Build the docker image for the gRPC server:

```
$ docker build -t amitsaha/grpc-users -f Dockerfile.users .
$ docker run -ti amitsaha/grpc-users
```

Start the server along with statsd exporter, prometheus and grafana:

```bash
docker-compose -f docker-compse.yml -f docker-compose-infra.yml up
```

Run the client:

```bash
$ docker exect -ti users bash
cd /client
$ ./run-client.sh 100
```
