#  -----------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License in the project root for
#  license information.
#  -----------------------------------------------------------------------------

import pytest

from aibuilder.core.model_connection import ModelConnection, LocalFileConnection


def test_model_connection_abstract_class():
    with pytest.raises(TypeError):
        ModelConnection()


def get_keys_dummy():
    return ["api_key_1", "api_key_2"]


def get_keys_dummy_tuple():
    return "api_key_1", "api_key_2"


def get_keys_dummy_single_element():
    return ["api_key_1"]


@pytest.mark.parametrize("api_keys_function, api_keys", [
    (None, None),
    (get_keys_dummy, ["api_key_1", "api_key_2"]),
    (get_keys_dummy_single_element, ["api_key_1"]),
    (get_keys_dummy_tuple, "type_error")
])
def test_local_file_connection(dummy_swagger_file, api_keys_function, api_keys):
    local_file_connection = LocalFileConnection(swagger_file_path=dummy_swagger_file,
                                                api_key_function=api_keys_function)

    assert isinstance(local_file_connection, ModelConnection)
    assert isinstance(local_file_connection, LocalFileConnection)
    assert hasattr(local_file_connection, "swagger_file_path")
    assert local_file_connection.swagger_file_path == dummy_swagger_file
    assert hasattr(local_file_connection, "get_keys")
    if api_keys is not "type_error":
        assert local_file_connection.get_keys() == api_keys
    else:
        with pytest.raises(TypeError):
            local_file_connection.get_keys()


@pytest.mark.parametrize("local_file_path", ["test_path", "test/path", "/test/path/path1"])
@pytest.mark.parametrize("api_key_function", [get_keys_dummy_tuple(), ("api_key", "api_key")])
def test_local_file_connection_error(local_file_path, dummy_swagger_file, api_key_function):
    with pytest.raises(ValueError):
        LocalFileConnection(swagger_file_path=local_file_path)

    with pytest.raises(ValueError):
        LocalFileConnection(swagger_file_path=dummy_swagger_file + ".test")

    # dummy swagger file input doesn't throw error
    local_file_connection = LocalFileConnection(swagger_file_path=dummy_swagger_file)
    assert isinstance(local_file_connection, LocalFileConnection)
    assert local_file_connection.get_keys() is None

    # dummy swagger file input with wrong api key function type throws value error
    with pytest.raises(ValueError):
        LocalFileConnection(swagger_file_path=dummy_swagger_file, api_key_function=api_key_function)
