import users_pb2_grpc as users_service
import users_types_pb2 as users_messages
from client_wrapper import ServiceClient


def run():
    users = ServiceClient(users_service, 'UsersStub', 'localhost', 50051)
    # Insert example metadata
    metadata = [('ip', '127.0.0.1')]
    response = users.CreateUser(
        users_messages.CreateUserRequest(username='tom'),
        metadata=metadata
    )
    if response:
        print("User created:", response.user.username)
    request = users_messages.GetUsersRequest(
        user=[users_messages.User(username="alexa", user_id=1),
              users_messages.User(username="christie", user_id=1)]
    )
    response = users.GetUsers(request)
    for resp in response:
        print(resp)


if __name__ == '__main__':
    run()
