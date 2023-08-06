#  -----------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License in the project root for
#  license information.
#  -----------------------------------------------------------------------------

import logging
from typing import Optional

import msal

from aibuilder.common.auth.constants import _AccessConfig, _AccessTokenResponseFields, _AccessTokenType
from aibuilder.common.auth.token_cache_manager import TokenCacheManager
from aibuilder.common.utils import Credentials

logger = logging.getLogger(__name__)


class D365Connector:
    """
    D365Connector is used to connect to a Dynamics CRM 365 Organization

     .. code-block:: python
        :caption: **Example code to use D365Connector Object**

        from aibuilder.common.auth.d365_connector import D365Connector

        d365_connector = D365Connector()

    """

    def __init__(self):
        self._auth_context = msal.PublicClientApplication(
            client_id=_AccessConfig.CLIENT_ID.value, authority=_AccessConfig.AUTHORITY.value)
        self._credentials_manager = TokenCacheManager()

    @property
    def credentials_manager(self) -> TokenCacheManager:
        """
        Returns credential manager object

        """
        return self._credentials_manager

    def get_arm_token_with_username_and_password(self, credentials: Credentials) -> str:
        """
        Authenticate using username and password named tuple

        .. code-block:: python
            :caption: **Example code to get arm token based on credentials**

            from aibuilder.common.utils import Credentials
            from aibuilder.common.auth.d365_connector import D365Connector

            credentials = Credentials(username="your_username", password="your_password")
            arm_token = D365Connector.get_arm_token_with_username_and_password(credentials=credentials)

        :param credentials: dict containing username and password
        :return: Return an ARM token
        """
        if not isinstance(credentials, Credentials):
            raise TypeError(f"Expected Credentials namedtuple, but got {type(credentials)}")

        scopes = D365Connector.construct_scopes(resource=_AccessConfig.RESOURCE.value)
        arm_token = self._get_token_with_username_password(credentials=credentials, scopes=scopes)

        self.credentials_manager.save_token(token_dict=arm_token, token_type=_AccessTokenType.ARM_TOKEN)
        return arm_token.get(_AccessTokenResponseFields.ACCESS_TOKEN.value)

    def authenticate_with_dynamics_crm(self, organization_url: str) -> str:
        """
        Retrieves token if expired or credentials do not yet exist

         .. code-block:: python
            :caption: **Example code to retrieve the token if it is expired or non existent**

            from aibuilder.common.auth.d365_connector import D365Connector

            organization_url = "https://your-organization-url-from-powerapps.com"
            arm_token = D365Connector.authenticate_with_dynamics_crm(organization_url=organization_url)

        :param organization_url: Org url
        :return: Valid user token
        """
        crm_token_dict = self.credentials_manager.get_token(token_type=_AccessTokenType.CRM_TOKEN)
        is_expired = not self.credentials_manager.is_valid_token(crm_token_dict)

        if is_expired or not crm_token_dict:
            crm_token_dict = self._refresh_crm_token(organization_url=organization_url)

        return crm_token_dict.get(_AccessTokenResponseFields.ACCESS_TOKEN.value)

    def authenticate_with_device_code(self, force_authenticate=False):
        """
        Authenticates user by sending them a code for their device

         .. code-block:: python
            :caption: **Example code to get arm token based on device based token authentication**

            from aibuilder.common.auth.d365_connector import D365Connector

            arm_token = D365Connector.authenticate_with_device_code()

        :param force_authenticate: Boolean whether user needs to be authenticated again
        :return: Valid user token
        """
        credentials = self._credentials_manager.get_token(token_type=_AccessTokenType.ARM_TOKEN)
        is_expired = not self.credentials_manager.is_valid_token(credentials)
        if not credentials or is_expired or force_authenticate:
            scopes = D365Connector.construct_scopes(resource=_AccessConfig.RESOURCE.value)
            arm_token = self._get_token_with_device_code(scopes=scopes)
            self._credentials_manager.save_token(token_dict=arm_token, token_type=_AccessTokenType.ARM_TOKEN)
            return arm_token.get(_AccessTokenResponseFields.ACCESS_TOKEN.value, 'accessToken not found')
        return credentials.get(_AccessTokenResponseFields.ACCESS_TOKEN.value, 'accessToken not found')

    def _refresh_crm_token(self, organization_url: str) -> dict:
        """
        Refreshes CRM token

        :param organization_url: Org url
        :return: Dictionary containing crm token and token metadata
        """
        scopes = D365Connector.construct_scopes(resource=organization_url)
        account = self._get_user_account()
        crm_token_dict = self._auth_context.acquire_token_silent(scopes=scopes, account=account)

        # If account parameter is None, then acquire token silent method won't return a token,
        # using device code authentication to get crm token
        if crm_token_dict is None:
            crm_token_dict = self._get_token_with_device_code(scopes=scopes)

        self.credentials_manager.save_token(token_dict=crm_token_dict,
                                            token_type=_AccessTokenType.CRM_TOKEN)

        return crm_token_dict

    def _get_username_from_arm_token(self) -> Optional[str]:
        """Returns username from ARM token"""
        credentials = self._credentials_manager.get_token(token_type=_AccessTokenType.ARM_TOKEN)
        if credentials and _AccessTokenResponseFields.ID_TOKEN_CLAIMS.value in credentials:
            return credentials[_AccessTokenResponseFields.ID_TOKEN_CLAIMS.value]\
                .get(_AccessTokenResponseFields.PREFERRED_USERNAME.value)

    def _get_user_account(self) -> Optional[str]:
        """Returns user account if only one account is found"""
        all_accounts = self._auth_context.get_accounts(username=self._get_username_from_arm_token())

        # If accounts list is not empty and only one account is found, then return user account
        return all_accounts[0] if all_accounts and len(all_accounts) == 1 else None

    def _get_token_with_username_password(self, credentials: Credentials, scopes: list) -> dict:
        """
        Call Azure Active Directory acquire token method using username and password

        :param credentials: Credentials object containing username and password
        :param scopes: Scopes requested to access
        :return: Dictionary containing token and token metadata returned by Azure Active Directory
        """
        arm_token = self._auth_context.acquire_token_by_username_password(
            username=credentials.username,
            password=credentials.password,
            scopes=scopes)

        return arm_token

    def _get_token_with_device_code(self, scopes: list) -> dict:
        """
        :param scopes: Scopes requested to access
        :return: Dictionary containing token and token metadata returned by Azure Active Directory
        """
        code = self._auth_context.initiate_device_flow(scopes=scopes)
        print(code['message'])
        arm_token = self._auth_context.acquire_token_by_device_flow(flow=code)

        return arm_token

    def get_token_using_refresh_token(self, scopes: list) -> dict:
        """
        Get token for any resource using refresh token. This method can be used to get access token for any resource
        using refresh token of a resource.

        :param scopes: Scopes requested to access
        :return: Dictionary containing access token, user id and other token parameters
        """
        arm_token_dict = self.credentials_manager.get_token(token_type=_AccessTokenType.ARM_TOKEN)
        return self._auth_context.acquire_token_by_refresh_token(
            refresh_token=arm_token_dict.get(_AccessTokenResponseFields.REFRESH_TOKEN.value), scopes=scopes)

    @staticmethod
    def construct_scopes(resource: str, required_scopes: Optional[list] = None) -> list:
        """
        Construct scopes using resource and required scope for the resource
        :param resource: Url of resource
        :param required_scopes: Optional list of scopes required. Default scope value will be used if not passed
        :return: List of fully constructed scopes
        """
        if not required_scopes:
            required_scopes = [".default"]

        scopes_with_resource = [f"{resource}/{scope}" for scope in required_scopes]

        return scopes_with_resource
