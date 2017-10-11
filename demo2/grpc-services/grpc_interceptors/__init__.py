import six
import abc

##############  Service-Side Interceptor Interfaces & Classes  #################


class UnaryUnaryServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-unary RPCs on the service-side.

This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_unary_handler(self, handler, method, request,
                                      servicer_context):
        """Intercepts unary-unary RPCs on the service-side.

    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns a response value.
      method: The full method name of the RPC.
      request: The request value for the RPC.
      servicer_context: The context of the current RPC.

    Returns:
      The RPC response.
    """
        raise NotImplementedError()


class UnaryStreamServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting unary-stream RPCs on the service-side.

    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_unary_stream_handler(self, handler, method, request,
                                       servicer_context):
        """Intercepts unary-stream RPCs on the service-side.

    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns an iterator of response values.
      method: The full method name of the RPC.
      request: The request value for the RPC.
      servicer_context: The context of the current RPC.

    Returns:
      An iterator of RPC response values.
    """
        raise NotImplementedError()


class StreamUnaryServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-unary RPCs on the service-side.

    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_unary_handler(self, handler, method, request_iterator,
                                       servicer_context):
        """Intercepts stream-unary RPCs on the service-side.

    Args:
      handler: The handler to continue processing the RPC.
      It takes an iterator of request values and
      a ServicerContext object and returns a response value.
      method: The full method name of the RPC.
      request_iterator: An iterator of request values for the RPC.
      servicer_context: The context of the current RPC.

    Returns:
      The RPC response.
    """
        raise NotImplementedError()


class StreamStreamServerInterceptor(six.with_metaclass(abc.ABCMeta)):
    """Affords intercepting stream-stream RPCs on the service-side.

    This is an EXPERIMENTAL API and is subject to change without notice."""

    @abc.abstractmethod
    def intercept_stream_stream_handler(self, handler, method, request_iterator,
                                        servicer_context):
        """Intercepts stream-stream RPCs on the service-side.

    Args:
      handler: The handler to continue processing the RPC.
      It takes a request value and a ServicerContext object
      and returns an iterator of response values.
      method: The full method name of the RPC.
      request_iterator: An iterator of request values for the RPC.
      servicer_context: The context of the current RPC.

    Returns:
      An iterator of RPC response values.
    """
        raise NotImplementedError()


def intercept_server(
         server,  # pylint: disable=redefined-outer-name
         *interceptors):
    """Creates an intercepted server.


       This is an EXPERIMENTAL API and is subject to change without notice.

    Args:
     server: A Server.
     interceptors: Zero or more objects of type
       UnaryUnaryServerInterceptor,
       UnaryStreamServerInterceptor,
       StreamUnaryServerInterceptor, or
       StreamStreamServerInterceptor.
       Interceptors are given control in the order they are listed.

    Returns:
     A Server that intercepts each received RPC via the provided interceptors.

    Raises:
     TypeError: If interceptor does not derive from any of
       UnaryUnaryServerInterceptor,
       UnaryStreamServerInterceptor,
       StreamUnaryServerInterceptor, or
       StreamStreamServerInterceptor.
    """
    from grpc_interceptors import _interceptor  # pylint: disable=cyclic-import
    return _interceptor.intercept_server(server, *interceptors)
