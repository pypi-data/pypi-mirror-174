#  -----------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License in the project root for
#  license information.
#  -----------------------------------------------------------------------------

import os
from abc import ABC, abstractmethod
from typing import Optional, Callable, List


class ModelConnection(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """
        Model connection abstract class.

        """
        pass

    @abstractmethod
    def get_keys(self) -> Optional[List[str]]:
        """Returns list of API Keys"""
        raise NotImplementedError


class LocalFileConnection(ModelConnection):
    def __init__(self, swagger_file_path: str, api_key_function: Optional[Callable] = None) -> None:
        """

        :param swagger_file_path: Local file path to swagger file
        :param api_key_function: Optional method to retrieve list of api key strings.
        Eg: (<api_key_1>, <api_key_2>)
        """
        super().__init__()
        if not os.path.isfile(swagger_file_path):
            raise ValueError(f"Please provide a valid local file path. Got: {swagger_file_path}")
        if not (api_key_function is None or isinstance(api_key_function, Callable)):
            raise ValueError(f"Please provide a valid function as input. Got: {type(api_key_function)}")

        self.swagger_file_path = swagger_file_path
        self._api_key_function = api_key_function

    def get_keys(self) -> Optional[List[str]]:
        """Returns list of API Key strings"""
        if self._api_key_function is None:
            return None

        api_keys = self._api_key_function()
        if not (isinstance(api_keys, List)):
            raise TypeError(f"API Key method should return a list of api keys")

        return api_keys
