# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import NamedTuple, Sequence, Dict, Tuple, Optional, Union, List, Any
from typing.io import IO

import requests
from requests.auth import AuthBase
from wheel.tool import verify


class AptlyAPIException(Exception):
    pass


class BaseAPIClient:
    def __init__(self, base_url: str, ssl_verify: Optional[str, bool]=None,
                 ssl_cert: Optional[Tuple[str, str]]=None, http_auth: Optional[AuthBase]=None) -> None:
        self.base_url = base_url
        self.ssl_verify = ssl_verify
        self.ssl_cert = ssl_cert
        self.http_auth = http_auth

    def do_get(self, url: str, params: Dict[str, str]=None) -> requests.Response:
        return requests.get(url, params=params, verify=self.ssl_verify, cert=self.ssl_cert,
                            auth=self.http_auth)

    def do_post(self, url: str, data: Union[str, Dict[str, str], Sequence[Tuple[str, str]]]=None,
                files=Union[Dict[str, IO], Dict[str, Tuple[str, IO, str, Optional[Dict[str, str]]]],
                            Dict[str, Tuple[str, str]]],
                json: Union[List[Dict[str, Any]], Dict[str, Any]]=None) -> requests.Response:
        return requests.post(url, data=data, files=files, json=json, verify=self.ssl_verify,
                             cert=self.ssl_cert, auth=self.http_auth)

    def do_put(self, url: str, data: Union[str, Dict[str, str], Sequence[Tuple[str, str]]]=None,
               files=Union[Dict[str, IO], Dict[str, Tuple[str, IO, str, Optional[Dict[str, str]]]],
                           Dict[str, Tuple[str, str]]],
               json: Union[List[Dict[str, Any]], Dict[str, Any]]=None) -> requests.Response:
        return requests.put(url, data=data, files=files, json=json, verify=self.ssl_verify,
                            cert=self.ssl_cert, auth=self.http_auth)

    def do_delete(self, url: str) -> requests.Response:
        return requests.delete(url, verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth)
