import grpc
import identity_pb2
import identity_pb2_grpc
import logging_client_interceptor
import time

GRPC_SERVER_CERT_PATH = "../tls_certs/user_sessions/tls/server.crt"


def run():
    with open(GRPC_SERVER_CERT_PATH, 'rb') as f:
        server_cert = f.read()
    channel_credentials = grpc.ssl_channel_credentials(server_cert)
    with grpc.secure_channel('localhost:50051', channel_credentials) as channel:
        intercepted_channel = grpc.intercept_channel(
                channel,
                logging_client_interceptor.LoggingClientInterceptor() 
        )
        stub = identity_pb2_grpc.IdentityStub(intercepted_channel)

        tokens = [
            identity_pb2.ExpireTokenRequest(token="a-token"), 
            identity_pb2.ExpireTokenRequest(token="b-token"),
            identity_pb2.ExpireTokenRequest(token="c-token")
        ]
        def tokens_to_expire():
            for t in tokens:
                print("Expiring: ", t.token)
                yield t
                # artificially sleep to demonstrate stream duration on the server side
                time.sleep(1)
        for resp in stub.ExpireToken(tokens_to_expire()):
            print("Status of token expiry: ", resp.result)

if __name__ == '__main__':
    run()
