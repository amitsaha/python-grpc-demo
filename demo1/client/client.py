from __future__ import print_function

import grpc

import users_pb2_grpc as users_service
import users_types_pb2 as users_messages


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = users_service.UsersStub(channel)
  metadata = [('ip', '127.0.0.1')]
  response = stub.CreateUser(
      users_messages.CreateUserRequest(username='tom'),
      metadata=metadata,
  )
  print("User created:", response.user.username)

if __name__ == '__main__':
  run()
