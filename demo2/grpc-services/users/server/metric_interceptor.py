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
        
        service_name, method_name = args[2].method.rsplit('/')[1::]
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


class MetricInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        print("Initializing metric interceptor")
    
    @send_metrics
    def intercept_service(self, continuation, handler_call_details):
        # Only intercept unary call and reponse streaming RPCs
        handler = continuation(handler_call_details)
        if handler and handler.request_streaming:
            return handler
        return continuation(handler_call_details)
