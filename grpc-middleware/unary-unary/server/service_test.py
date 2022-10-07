from unittest.mock import MagicMock
import grpc
import grpc_testing
import identity_pb2
import pytest


from .server import Identity



@pytest.fixture
def test_server():
    servicers = {
        identity_pb2.DESCRIPTOR.services_by_name['Identity']: Identity()
    }

    return grpc_testing.server_from_dictionary(
        servicers, grpc_testing.strict_real_time(),
    )


def test_validate_request_valid_token(test_server):
    
    request = identity_pb2.ValidateTokenRequest(token="a-token")
    validate_request_method = test_server.invoke_unary_unary(
        method_descriptor=(identity_pb2.DESCRIPTOR
                           .services_by_name['Identity']
                           .methods_by_name['ValidateToken']),
        invocation_metadata={},
        request=request, timeout=1)
    response, metadata, code, details = validate_request_method.termination()

    assert code == grpc.StatusCode.OK
    assert response.user_id == "default-user-id"



