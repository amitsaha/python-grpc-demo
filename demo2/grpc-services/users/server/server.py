from concurrent import futures
import time
import os

import grpc

import users_pb2_grpc as users_service
import users_types_pb2 as users_messages

from metric_interceptor import MetricInterceptor
from logging_interceptor import LoggingInterceptor

import random

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersService(users_service.UsersServicer):

    def CreateUser(self, request, context):
        user = users_messages.User(username=request.username, user_id=1)
        if random.random() > 0.5:
            1/0
        return users_messages.CreateUserResult(user=user)

    def GetUsers(self, request, context):
        for user in request.user:
            user = users_messages.User(
                username=user.username, user_id=user.user_id
            )
            yield users_messages.GetUsersResult(user=user)


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), 
        interceptors=[LoggingInterceptor(), MetricInterceptor(),],
        )
    users_service.add_UsersServicer_to_server(UsersService(), server)

    # read in key and certificate
    with open(os.path.join(os.path.split(__file__)[0], 'server.key')) as f:
        private_key = f.read().encode()
    with open(os.path.join(os.path.split(__file__)[0], 'server.crt')) as f:
        certificate_chain = f.read().encode()
    # create server credentials
    server_creds = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))
    server.add_secure_port('0.0.0.0:50051', server_creds)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
