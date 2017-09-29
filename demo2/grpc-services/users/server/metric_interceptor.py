import six
import abc
import time

from grpcext import UnaryServerInterceptor, StreamServerInterceptor


class MetricInterceptor(UnaryServerInterceptor, StreamServerInterceptor):

    def __init__(self):
        pass

    def intercept_unary(self, request, servicer_context, server_info, handler):
        response = None
        try:
            servicer_context.start_time = time.time()
            print('I was called')
            response = handler(request)
        except:
            e = sys.exc_info()[0]
            print(str(e))
            raise
        print('Request took {0} seconds'.format(time.time()-servicer_context.start_time))
        return response

    def _intercept_server_stream(self, servicer_context, server_info, handler):
        print('I was called')

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
            print('I was called')

            try:
                return handler()
            except:
                e = sys.exc_info()[0]
                print(str(e))
                raise
