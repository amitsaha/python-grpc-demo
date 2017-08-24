from __future__ import print_function

import grpc

import service_pb2
import service_pb2_grpc


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = service_pb2_grpc.GreeterStub(channel)
  response = stub.SayHello(service_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()
