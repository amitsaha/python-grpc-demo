import grpc
import identity_pb2
import identity_pb2_grpc
import logging_client_interceptor

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
        response = stub.ValidateToken(
            identity_pb2.ValidateTokenRequest(token="a-token")
        )
    print("Reply:", response.user_id)


if __name__ == '__main__':
    run()
