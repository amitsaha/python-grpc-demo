import datetime
import grpc
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def log_errors(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kw):
        metadata = {}
        metadata['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        servicer_context = None
        # Sample value of args:
        # 0: (<logging_interceptor.LoggingInterceptor object at 0x7fb88de03f10>, 
        # 1: <function _ServicePipeline._continuation.<locals>.<lambda> at 0x7fb88dce9670>, 
        # 2: _HandlerCallDetails(method='/Users/GetUsers', 
        #     invocation_metadata=(_Metadatum(key='user-agent', value='grpc-python/1.38.0 grpc-c/16.0.0 (linux; chttp2)'),)))
        # https://grpc.github.io/grpc/python/glossary.html#term-metadata
        metadata['method'] = args[2].method
        for k, v in args[2].invocation_metadata[0]._asdict().items():
            metadata[k] = v
        logger.info('Got Request', extra=metadata)
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


class LoggingInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        print("Initializing logging interceptor")
    
    @log_errors
    def intercept_service(self, continuation, handler_call_details):
        # Only intercept unary call and reponse streaming RPCs
        handler = continuation(handler_call_details)
        if handler and handler.request_streaming:
            return handler
        return continuation(handler_call_details)
