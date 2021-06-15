## Demo 1

### Running the HTTP and gRPC server

Build the docker images:

```
$ docker-compose build
```

Start the server along with statsd exporter, prometheus and grafana:

```bash
$ docker-compose -f docker-compse.yml -f docker-compose-infra.yml up
```

### Making a request

```
$ curl localhost:5000/users/
{
  "user": {
    "username": "alexa",
    "userId": 1
  }
}{
  "user": {
    "username": "christie",
    "userId": 1
  }

```
