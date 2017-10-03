import time
import grpc
import sys

from grpc_interceptors import UnaryUnaryServerInterceptor, UnaryStreamServerInterceptor
from datadog import DogStatsd

statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'


def push_to_statsd_histogram(metric, value, tags=[]):
    statsd.histogram(metric, value, tags)


def push_to_statsd_increment(metric, value=1, tags=[]):
    statsd.increment(metric, value, tags)


def send_metrics(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kw):
        servicer_context = None
        if isinstance(args[4], grpc._server._Context):
            servicer_context = args[4]
        else:
            raise Exception('MetricInterceptor cannot run. Expecting grpc._server.Context')
        # This gives us <service>/<method name>
        service_method = servicer_context._rpc_event.request_call_details.method
        service_name, method_name = str(service_method).rsplit('/')[1::]
        try:
            start_time = time.time()
            result = func(*args, **kw)
        except:
            resp_time = time.time() - start_time
            push_to_statsd_histogram(
                REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                ['service:{0}'.format(service_name),
                 'method:{0}'.format(method_name),
                 'status:error',
                ]
            )
            raise
        resp_time = time.time() - start_time
        push_to_statsd_histogram(
                REQUEST_LATENCY_METRIC_NAME,
                resp_time,
                ['service:{0}'.format(service_name),
                 'method:{0}'.format(method_name),
                 'status:success',
                ]
            )
        return result
    return wrapper


class MetricInterceptor(UnaryUnaryServerInterceptor, UnaryStreamServerInterceptor):

    def __init__(self):
        print("Initializing metric interceptor")

    @send_metrics
    def intercept_unary_unary_handler(self, handler, method, request, servicer_context):
        response = None
        try:
            response = handler(request, servicer_context)
        except:
            e = sys.exc_info()[0]
            print(str(e))
            raise
        return response

    @send_metrics
    def intercept_unary_stream_handler(self, handler, method, request, servicer_context):
        try:
            result = handler(request, servicer_context)
            for response in result:
                yield response
        except:
            e = sys.exc_info()[0]
            print(str(e))
            raise
