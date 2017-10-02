```
20:30 $ docker build -t amitsaha/grpc-users -f Dockerfile.users .
```

```bash
docker-compose -f docker-compse.yml -f docker-compose-infra.yml up
```

```bash
docker exect -ti users bash
cd /client
$ ./run-client.sh 100
```
