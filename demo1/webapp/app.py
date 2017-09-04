from flask import Flask, Response
import sys
from functools import partial
from google.protobuf.json_format import MessageToJson

import grpc
import users_pb2_grpc as users_service
import users_types_pb2 as users_messages


app = Flask(__name__)

# client timeout
TIMEOUT = 30
class UsersService:

    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        self.stub = users_service.UsersStub(channel)

    def __getattr__(self, attr):
        return partial(self._wrapped_call, self.stub, attr)

    # args[0]: stub, args[1]: function to call, args[3]: Request
    # kwargs: keyword arguments
    def _wrapped_call(self, *args, **kwargs):
        try:
            return getattr(args[0], args[1])(args[2], **kwargs, timeout=TIMEOUT)
        except grpc.RpcError as e:
            print('Call {0} failed with {1}'.format(
                args[1], e.code())
            )
            raise

@app.route('/users/')
def users_get():
    users = UsersService()
    request = users_messages.GetUsersRequest(
        user=[users_messages.User(username="alexa", user_id=1),
              users_messages.User(username="christie", user_id=1)]
    )
    def get_user():
        response = users.GetUsers(request)
        for resp in response:
            yield MessageToJson(resp)
    return Response(get_user(), content_type='application/json')

if __name__ == '__main__':
    app.run()
