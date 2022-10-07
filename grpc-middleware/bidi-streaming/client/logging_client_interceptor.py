import grpc
import time

# reference: https://sourcegraph.com/github.com/grpc/grpc/-/blob/examples/python/interceptors/headers/generic_client_interceptor.py

class LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor,
                               grpc.StreamStreamClientInterceptor):

    def intercept_unary_unary(self, continuation, client_call_details, request):
        print("Call details", client_call_details)
        response = continuation(client_call_details, request)
        return response

    def _intercept_request_stream_msg(self, request_iterator):
        for r in request_iterator:
            print("Streaming request")
            yield r

    def _intercept_response_stream_msg(self, response_iterator):
        for r in response_iterator:
            print("Streaming response")
            yield r

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        self.stream_started = time.time()
        print("Call details", client_call_details)
        response_it = continuation(client_call_details, self._intercept_request_stream_msg(request_iterator))
        yield from self._intercept_response_stream_msg(response_it)
        stream_duration = time.time() - self.stream_started
        print("Stream duration: {0} seconds".format(stream_duration))


