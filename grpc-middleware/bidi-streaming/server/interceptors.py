import time
import grpc

# wrap an RPC call
# see https://github.com/grpc/grpc/issues/18191
def _wrap_rpc_behavior(handler, continuation):
    if handler is None:
        return None

    if handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.stream_stream
        handler_factory = grpc.stream_stream_rpc_method_handler
    elif handler.request_streaming and not handler.response_streaming:
        behavior_fn = handler.stream_unary
        handler_factory = grpc.stream_unary_rpc_method_handler
    elif not handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.unary_stream
        handler_factory = grpc.unary_stream_rpc_method_handler
    else:
        behavior_fn = handler.unary_unary
        handler_factory = grpc.unary_unary_rpc_method_handler

    return handler_factory(
        continuation(
            behavior_fn, handler.request_streaming, handler.response_streaming
        ),
        request_deserializer=handler.request_deserializer,
        response_serializer=handler.response_serializer,
    )

# Learned this technique from:
# https://github.com/open-telemetry/opentelemetry-python-contrib/blob/main/instrumentation/opentelemetry-instrumentation-grpc/src/opentelemetry/instrumentation/grpc/_server.py
class LoggingServicerContext(grpc.ServicerContext):
    def __init__(self, servicer_context):
        self._servicer_context = servicer_context
        super().__init__()

    def __getattr__(self, attr):
        return getattr(self._servicer_context, attr)

    def is_active(self, *args, **kwargs):
        return self._servicer_context.is_active(*args, **kwargs)

    def time_remaining(self, *args, **kwargs):
        return self._servicer_context.time_remaining(*args, **kwargs)

    def cancel(self, *args, **kwargs):
        return self._servicer_context.cancel(*args, **kwargs)

    def add_callback(self, *args, **kwargs):
        return self._servicer_context.add_callback(*args, **kwargs)

    def disable_next_message_compression(self):
        return self._service_context.disable_next_message_compression()

    def invocation_metadata(self, *args, **kwargs):
        return self._servicer_context.invocation_metadata(*args, **kwargs)

    def peer(self):
        return self._servicer_context.peer()

    def peer_identities(self):
        return self._servicer_context.peer_identities()

    def peer_identity_key(self):
        return self._servicer_context.peer_identity_key()

    def auth_context(self):
        return self._servicer_context.auth_context()

    def set_compression(self, compression):
        return self._servicer_context.set_compression(compression)

    def send_initial_metadata(self, *args, **kwargs):
        return self._servicer_context.send_initial_metadata(*args, **kwargs)

    def set_trailing_metadata(self, *args, **kwargs):
        return self._servicer_context.set_trailing_metadata(*args, **kwargs)

    def trailing_metadata(self):
        return self._servicer_context.trailing_metadata()

    def abort(self, code, details):
        self.code = code
        self.details = details
        return self._servicer_context.abort(code, details)

    def abort_with_status(self, status):
        return self._servicer_context.abort_with_status(status)

    def set_code(self, code):
        self.code = code
        # use details if we already have it, otherwise the status description
        return self._servicer_context.set_code(code)

    def set_details(self, details):
        self.details = details
        return self._servicer_context.set_details(details)

class LoggingInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        pass


    def intercept_service(self, continuation, handler_call_details):
        self.stream_started = time.time()
        print(handler_call_details.method, handler_call_details.invocation_metadata)

        def logging_wrapper(behavior, request_streaming, response_streaming):
            def logging_interceptor(request_or_iterator, context):
                context = LoggingServicerContext(context)
                if request_streaming or response_streaming:
                    return self._intercept_server_stream(
                        behavior,
                        request_or_iterator,
                        context,
                    )
                try:
                    return behavior(request_or_iterator, context)
                except Exception as error:
                    raise error

            return logging_interceptor

        return _wrap_rpc_behavior(
            continuation(handler_call_details), logging_wrapper
        )

    def _intercept_server_stream(
        self, behavior, request_or_iterator, context
    ):
        def wrapd(behavior, request_or_iterator, context):
            for r in request_or_iterator:
                print("Processing stream message", r)
                resp = behavior(list([r]), context)
                yield from resp
        yield from wrapd(behavior, request_or_iterator, context)
        stream_duration = time.time() - self.stream_started
        print("Stream duration: {0} seconds".format(stream_duration))

