import grpc

class LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):

    def intercept_unary_unary(self, continuation, client_call_details, request):
        print("Call details", client_call_details)
        response = continuation(client_call_details, request)
        return response