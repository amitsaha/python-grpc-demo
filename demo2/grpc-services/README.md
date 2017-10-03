```
$ docker build -t amitsaha/grpc-users -f Dockerfile.users .
$ docker run --add-host Demo:127.0.0.1 -ti amitsaha/grpc-users
```

```bash
docker-compose -f docker-compse.yml -f docker-compose-infra.yml up
```

```bash
docker exect -ti users bash
cd /client
$ ./run-client.sh 100
```
