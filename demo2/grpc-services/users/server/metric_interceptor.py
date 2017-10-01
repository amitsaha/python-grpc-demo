import six
import abc
import time
import random
import grpc

from grpcext import UnaryServerInterceptor, StreamServerInterceptor
from datadog import DogStatsd

statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'

def send_metrics(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kw):
        if not isinstance(args[2], grpc._server._Context):
            raise Exception('MetricInterceptor cannot run. Expecting grpc._server.Context')
        # This gives us <service>/<method name>
        servicer_context = args[2]
        service_method = servicer_context._rpc_event.request_call_details.method
        service_name, method_name = str(service_method).rsplit('/')[1::]
        try:
            start_time = time.time()
            result = func(*args, **kw)
        except:
            resp_time = time.time() - start_time
            statsd.histogram(REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                tags=[
                    'service:{0}'.format(service_name),
                    'method: {0}'.format(method_name),
                    ]
            )
            raise
        resp_time = time.time() - start_time
        statsd.histogram(REQUEST_LATENCY_METRIC_NAME,
            resp_time,
            tags=[
                'service:{0}'.format(service_name),
                'method: {0}'.format(method_name),
                ]
        )
        return result
    return wrapper

class MetricInterceptor(UnaryServerInterceptor, StreamServerInterceptor):

    def __init__(self):
        print("Initializing metric interceptor")

    @send_metrics
    def intercept_unary(self, request, servicer_context, server_info, handler):
        response = None
        try:
            response = handler(request)
        except:
            e = sys.exc_info()[0]
            print(str(e))
            raise
        return response

    def _intercept_server_stream(self, servicer_context, server_info, handler):

        try:
            result = handler()
            for response in result:
                yield response
        except:
            e = sys.exc_info()[0]
            print(str(e))
            raise

    def intercept_stream(self, servicer_context, server_info, handler):
        if server_info.is_server_stream:
            return self._intercept_server_stream(servicer_context, server_info,
                                                 handler)
            try:
                return handler()
            except:
                e = sys.exc_info()[0]
                print(str(e))
                raise
