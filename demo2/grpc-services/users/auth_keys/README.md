```
07:27 $ openssl genrsa -out server.key 2048
Generating RSA private key, 2048 bit long modulus
.........+++
.......................................................................+++
e is 65537 (0x10001)
(grpc-demo) ✔ ~/work/github.com/amitsaha/python-grpc-demo/demo2/grpc-services/users/auth_keys [part2 L|…15]
07:27 $ ls
server.key
```


```
07:28 $ openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:AU
State or Province Name (full name) [Some-State]:NSW
Locality Name (eg, city) []:Sydney
Organization Name (eg, company) [Internet Widgits Pty Ltd]:gRPC Demo
Organizational Unit Name (eg, section) []:gRPC
Common Name (e.g. server FQDN or YOUR name) []:Demo
Email Address []:a@a.com
(
07:27 $ ls
server.key server.crt

```
