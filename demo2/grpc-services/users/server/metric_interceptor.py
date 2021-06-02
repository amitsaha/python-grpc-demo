import time
import grpc
import logging

from grpc import ServerInterceptor
from datadog import DogStatsd

statsd = DogStatsd(host="statsd", port=9125)
REQUEST_LATENCY_METRIC_NAME = 'request_latency_seconds'


def push_to_statsd_histogram(metric, value, tags=[]):
    statsd.histogram(metric, value, tags)


def send_metrics(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kw):
        service_method = None
        service_name = None
        if isinstance(args[4], grpc._server._Context):
            servicer_context = args[4]
            # This gives us <service>/<method name>
            service_method = servicer_context._rpc_event.request_call_details.method
            service_name, method_name = str(service_method).rsplit('/')[1::]
        else:
            logging.warning('Cannot derive the service name and method')
        try:
            start_time = time.time()
            result = func(*args, **kw)
            result_status = 'success'
        except Exception:
            result_status = 'error'
            raise
        finally:
            resp_time = time.time() - start_time
            push_to_statsd_histogram(
                REQUEST_LATENCY_METRIC_NAME,
                resp_time, [
                    'service:{0}'.format(service_name),
                    'method:{0}'.format(method_name),
                    'status:{0}'.format(result_status),
                ])
        return result
    return wrapper


class MetricInterceptor(ServerInterceptor):

    def __init__(self):
        print("Initializing metric interceptor")

    @abc.abstractmethod
    def intercept_service(self, continuation, handler_call_details):
        return handler(request, servicer_context)

    @send_metrics
    def intercept_unary_unary_handler(self, handler, method, request, servicer_context):
        return handler(request, servicer_context)

    @send_metrics
    def intercept_unary_stream_handler(self, handler, method, request, servicer_context):
        result = handler(request, servicer_context)
        for response in result:
            yield response
