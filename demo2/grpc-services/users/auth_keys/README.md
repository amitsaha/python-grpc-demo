## Create a self-signed certificate 

**Generate a private key**

```
$ openssl genrsa -out server.key 2048
Generating RSA private key, 2048 bit long modulus
.........+++
.......................................................................+++
e is 65537 (0x10001)


$ ls
server.key
```

**Use the above key to generate and sign a certificate**

```
$ openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650
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
Common Name (e.g. server FQDN or YOUR name) []:users
Email Address []:a@a.com
(
```

We will now have two files:

$ ls
server.key server.crt

```

## Server side configuration

We will then copy both these files to the `server` directory

## Client side configuration

We will copy the `.crt` file to the `client` directory.

## Learn more

- https://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl
- https://en.wikipedia.org/wiki/X.509
- https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04

