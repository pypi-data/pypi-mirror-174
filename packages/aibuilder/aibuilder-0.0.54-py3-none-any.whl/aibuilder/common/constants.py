#  -----------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License in the project root for
#  license information.
#  -----------------------------------------------------------------------------


from enum import Enum


class OpenAPIConstants(Enum):
    """
    Open API constants

    """
    filter = "$filter"
    equals = "eq"
    value = "value"
    object_id = "id"


class GraphClientConstants(Enum):
    """
    Graph client constants

    """
    graph_api_version = "v1.0"
    service_principal_path = "servicePrincipals"
    application_id_key = "appId"
    application_id = "be5f0473-6b57-40f8-b0a9-b3054b41b99e"
