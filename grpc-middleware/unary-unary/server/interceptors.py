import grpc

class LoggingInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        pass

    def intercept_service(self, continuation, handler_call_details):
        print(handler_call_details.method, handler_call_details.invocation_metadata)
        return continuation(handler_call_details)
