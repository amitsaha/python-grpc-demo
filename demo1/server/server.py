from concurrent import futures
import time

import grpc

import service_pb2
import service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(service_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return service_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
