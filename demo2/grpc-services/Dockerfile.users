FROM python:3.6-jessie
RUN set -e; \
	apt-get update ; \
    apt-get install \
		gcc \
        g++ \
	; \
    pip install --upgrade pip; \
    pip install grpcio==1.6.3 grpcio-tools==1.6.3 
ADD protos/gen-py /protos/gen-py
ADD grpc_interceptors /grpc_interceptors
ADD users/server /server

# Add the client code strictly for development
# purposes
ADD users/client /client
WORKDIR /server
RUN pip install -r requirements.txt
EXPOSE 50051
VOLUME /server
CMD PYTHONPATH=/:/protos/gen-py python3 server.py
