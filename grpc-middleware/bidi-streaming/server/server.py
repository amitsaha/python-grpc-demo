import json
import os
import signal
import sys
from concurrent import futures
import threading

import grpc
import identity_pb2
import identity_pb2_grpc


from interceptors import LoggingInterceptor

class Identity(identity_pb2_grpc.IdentityServicer):

    def __init__(self):
        super().__init__()

    def ValidateToken(self, request: identity_pb2.ValidateTokenRequest, context):
        user_details = identity_pb2.ValidateTokenReply(user_id="default-user-id")        
        return user_details 

    def ExpireToken(self, request_iterator, context):
        for r in request_iterator:
            yield identity_pb2.ExpireTokenReply(result=True)


def _read_credentials_from_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        data = f.read()
    return data


def serve(app_config: dict):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors = (LoggingInterceptor(),) 
    )
    identity_pb2_grpc.add_IdentityServicer_to_server(
        Identity(), server,
    )

    SERVER_CERTIFICATE = _read_credentials_from_file(
        app_config["tls_cert_path"])
    SERVER_CERTIFICATE_KEY = _read_credentials_from_file(
        app_config["tls_key_path"])

    server_credentials = grpc.ssl_server_credentials(((
        SERVER_CERTIFICATE_KEY,
        SERVER_CERTIFICATE,
    ),))

    server.add_secure_port(
        app_config['listen_addr'], server_credentials
    )
    print('Starting server at ' + app_config['listen_addr'])
    server.start()

    # Shutdown logic with signal handling copied from:
    # https://stackoverflow.com/a/58411106
    print('Started server at ' + app_config['listen_addr'])
    done = threading.Event()

    def on_done(signum, frame):
        print('Got signal {}, {}'.format(signum, frame))
        done.set()
    signal.signal(signal.SIGTERM, on_done)
    done.wait()
    print('Stopped RPC server, Waiting for RPCs to complete...')
    NUM_SECS_TO_WAIT = 30
    server.stop(NUM_SECS_TO_WAIT).wait()
    print('Done stopping server')


def app_config() -> dict:
    config = {
        "listen_addr": os.getenv("LISTEN_ADDR", "[::]:50051"),
        "tls_cert_path": os.getenv("TLS_CERT_PATH"),
        "tls_key_path": os.getenv("TLS_KEY_PATH"),
    }

    if not all(config.values()):
        sys.exit(
            print("Required environment variables: ", [
                  v.upper() for v in config.keys() if not config[v]])
        )
    return config


if __name__ == '__main__':
    serve(app_config())
