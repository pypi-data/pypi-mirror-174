#  -----------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License in the project root for
#  license information.
#  -----------------------------------------------------------------------------

from unittest import mock

import pytest
import requests

from aibuilder.common.paconnector.exceptions import RequestFormatException
from aibuilder.common.paconnector.request_builder import _RequestBuilder
from aibuilder.models.helpers.ai_model import AiModel
from aibuilder.models.helpers.constants import _AIBuilderTemplateIds
from aibuilder.models.helpers.exceptions import RegistrationException


def test_ai_model_init():
    ai_model = AiModel(url="https://foobar.com", token="token")

    assert isinstance(ai_model, AiModel)
    assert ai_model._url == "https://foobar.com"
    assert isinstance(ai_model._request_builder, _RequestBuilder)


@pytest.mark.parametrize("template_id",
                         [_AIBuilderTemplateIds.GP_TEMPLATE_ID.value, _AIBuilderTemplateIds.BYOM_TEMPLATE_ID.value])
def test_create_ai_model(template_id):
    with mock.patch('requests.request') as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.headers = {"OData-EntityId": "Model(config_id)"}

        ai_model = AiModel(url="https://foobar.com", token="token")

        model_id = ai_model.create(model_name="test", template_id=template_id)

        assert model_id == "config_id"

        assert mock_request.call_args[0][0] == "POST"
        assert mock_request.call_args[0][1] == "https://foobar.com/api/data/v9.0/msdyn_aimodels"
        assert mock_request.call_args[1]["json"] == {'msdyn_name': 'test',
                                                     'msdyn_TemplateId@odata.bind':
                                                         f'/msdyn_aitemplates({template_id})'}


@pytest.mark.parametrize("url, token, model_name", [
    ("https://foobar.com", "token", "test"),
    ("https://test.com", "token_test", "test-model"),
])
@pytest.mark.parametrize("status_code, json, expected_model_id", [
    (200, {"value": [{"msdyn_aimodelid": "model_123"}]}, "model_123"),
    (500, {"value": []}, None)
])
def test_get_ai_model(url, token, model_name, status_code, json, expected_model_id):
    with mock.patch('requests.request') as mock_request:
        mock_response = mock.Mock(requests.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json

        mock_request.return_value = mock_response

        ai_model = AiModel(url=url, token=token)

        model_id = ai_model.retrieve(model_name=model_name)

        assert model_id == expected_model_id

        assert mock_request.call_args[0][0] == "GET"
        assert mock_request.call_args[0][1] == \
               f"{url}/api/data/v9.0/msdyn_aimodels?%24filter=msdyn_name%20eq%20%27{model_name}%27"


@pytest.mark.parametrize("url, token, model_id", [
    ("https://foobar.com", "token", "123"),
    ("https://test.com", "token_test", "foo-bar"),
])
@pytest.mark.parametrize("status_code, json", [
    (200, {"value": [{"msdyn_aimodelid": "model_123"}]}),
    (500, {"value": []})
])
def test_ai_model_schedule(url, token, model_id, status_code, json):
    with mock.patch('requests.request') as mock_request:
        mock_response = mock.Mock(requests.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json

        mock_request.return_value = mock_response

        ai_model = AiModel(url=url, token=token)

        response = ai_model.schedule(model_id=model_id)

        assert isinstance(response, requests.Response)
        assert response.status_code == status_code
        assert response.json() == json

        assert mock_request.call_args[0][0] == "POST"
        assert mock_request.call_args[0][1] == \
               f"{url}/api/data/v9.0/msdyn_aimodels({model_id})/Microsoft.Dynamics.CRM.SchedulePrediction"
        assert mock_request.call_args[1]["json"] == {
            "version": "1.0",
            "predictImmediately": False
        }


@mock.patch.object(AiModel, "_has_scheduled_run_config")
@pytest.mark.parametrize("url, token, model_id", [
    ("https://foobar.com", "token", "123"),
    ("https://test.com", "token_test", "foo-bar"),
])
@pytest.mark.parametrize("has_scheduled_ai_model, status_code, json, throws_exception", [
    (True, 200, {"value": [{"msdyn_aimodelid": "model_123"}]}, None),
    (False, 200, {"value": [{"msdyn_aimodelid": "model_123"}]}, None),
    (True, 400, {"value": [{"msdyn_aimodelid": "model_123"}]},
     RequestFormatException("foo bar UnPublishedModel foo bar")),
    (True, 500, {"value": []}, None),
    (False, 500, {"value": []}, None)
])
def test_ai_model_unschedule(mock_has_scheduled_run_config, url, token, model_id, status_code, json, throws_exception,
                             has_scheduled_ai_model):
    mock_has_scheduled_run_config.return_value = has_scheduled_ai_model
    with mock.patch('requests.request') as mock_request:
        mock_unschedule_response = mock.Mock(requests.Response)

        mock_unschedule_response.status_code = status_code
        if throws_exception:
            mock_unschedule_response.raise_for_status.side_effect = throws_exception

        mock_unschedule_response.json.return_value = json

        mock_request.return_value = mock_unschedule_response

        ai_model = AiModel(url=url, token=token)

        # if no scheduled model is found
        if not has_scheduled_ai_model:
            response = ai_model.unschedule(model_id=model_id)

            assert response is True
        elif status_code == 200 or isinstance(throws_exception, RequestFormatException):
            response = ai_model.unschedule(model_id=model_id)

            assert response is True
            assert mock_request.call_args[0][0] == "POST"
            assert mock_request.call_args[0][1] == \
                f"{url}/api/data/v9.0/msdyn_aimodels({model_id})/Microsoft.Dynamics.CRM.UnschedulePrediction"
            assert mock_request.call_args[1]["json"] == {
                "version": "1.0"
            }
        else:
            with pytest.raises(RegistrationException):
                ai_model.unschedule(model_id=model_id)

        assert mock_unschedule_response.call_count == 0 if has_scheduled_ai_model else 1
        assert mock_has_scheduled_run_config.call_count == 1


@mock.patch('requests.request')
@pytest.mark.parametrize("url, token, model_id", [
    ("https://foobar.com", "token", "123"),
    ("https://test.com", "token_test", "foo-bar"),
])
@pytest.mark.parametrize("response_status_code, response_json_body, expected_result", [
    (200, {"value": []}, False),
    (200, {"value": [{"foo": "bar"}]}, True),
    (200, {"value": [{"foo": "bar"}, {"one": "more"}]}, True),
    (200, {"new-value": [{"foo": "bar"}, {"one": "more"}]}, False),
    (400, {"value": [{"foo": "bar"}, {"one": "more"}]}, False),
    (500, {"value": [{"foo": "bar"}, {"one": "more"}]}, False),
    (500, {}, False),
    (400, {}, False)
])
def test_has_scheduled_run_config(mock_request, url, token, model_id, response_status_code, response_json_body,
                                  expected_result):
    mock_response = mock.Mock(requests.Response)
    mock_response.status_code = response_status_code
    mock_response.json.return_value = response_json_body

    mock_request.return_value = mock_response

    ai_model = AiModel(url=url, token=token)

    if response_status_code == 200:
        result = ai_model._has_scheduled_run_config(model_id=model_id)

        assert isinstance(result, bool)
        assert result is expected_result

        assert mock_request.call_args[0][0] == "GET"
        assert mock_request.call_args[0][1] == \
            f"{url}/api/data/v9.0/msdyn_aiconfigurations?%24filter=statuscode%20eq%208%20and" \
            f"%20_msdyn_aimodelid_value%20eq%20%27{model_id}%27"

        assert mock_request.call_count == 1
    else:
        with pytest.raises(RegistrationException):
            ai_model._has_scheduled_run_config(model_id=model_id)
