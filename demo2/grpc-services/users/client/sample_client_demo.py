import sys

import grpc

import users_pb2_grpc as users_service
import users_types_pb2 as users_messages


def run():
    # read in certificate
    with open('server.crt') as f:
        trusted_certs = f.read().encode()

    # create credentials
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('localhost:50051', credentials)
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        sys.exit('Error connecting to server')
    else:
        stub = users_service.UsersStub(channel)
        metadata = [('ip', '127.0.0.1')]

        try:
            response = stub.CreateUser(
                users_messages.CreateUserRequest(username='tom'),
                metadata=metadata,
            )
        except grpc.RpcError as e:
            print('CreateUser failed with {0}: {1}'.format(e.code(), e.details()))
        else:
            print("User created:", response.user.username)

        request = users_messages.GetUsersRequest(
            user=[users_messages.User(username="alexa", user_id=1),
                  users_messages.User(username="christie", user_id=1)]
        )
        response = stub.GetUsers(request)
        for resp in response:
            print(resp)


if __name__ == '__main__':
    run()
