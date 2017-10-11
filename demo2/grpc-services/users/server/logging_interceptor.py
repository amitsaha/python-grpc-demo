import datetime
import grpc
import logging
from pythonjsonlogger import jsonlogger

from grpc_interceptors import UnaryUnaryServerInterceptor, UnaryStreamServerInterceptor

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def log_errors(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kw):
        metadata = {}
        metadata['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        servicer_context = None
        if isinstance(args[4], grpc._server._Context):
            servicer_context = args[4]
            metadata.update(dict(servicer_context.invocation_metadata()))
        try:
            result = func(*args, **kw)
        except Exception as e:
            logger.error(e, exc_info=True, extra=metadata)
            if servicer_context:
                servicer_context.set_details(str(e))
                servicer_context.set_code(grpc.StatusCode.UNKNOWN)
            # TODO: need to return an appropriate response type here
            # Currently this will raise a serialization error on the server
            # side
            return None
        else:
            return result
    return wrapper


class LoggingInterceptor(UnaryUnaryServerInterceptor, UnaryStreamServerInterceptor):

    def __init__(self):
        print("Initializing logging interceptor")

    @log_errors
    def intercept_unary_unary_handler(self, handler, method, request, servicer_context):
        return handler(request, servicer_context)

    @log_errors
    def intercept_unary_stream_handler(self, handler, method, request, servicer_context):
        result = handler(request, servicer_context)
        for response in result:
            yield response
