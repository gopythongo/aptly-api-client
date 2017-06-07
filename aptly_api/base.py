# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Sequence, Dict, Tuple, Optional, Union, List, Any, MutableMapping
from urllib.parse import urljoin

from typing.io import IO

import requests
from requests.auth import AuthBase


class AptlyAPIException(Exception):
    def __init__(self, *args: Any, status_code: int=0) -> None:
        super().__init__(*args)
        self.status_code = status_code


class BaseAPIClient:
    def __init__(self, base_url: str, ssl_verify: Union[str, bool, None]=None,
                 ssl_cert: Optional[Tuple[str, str]]=None, http_auth: Optional[AuthBase]=None) -> None:
        self.base_url = base_url
        self.ssl_verify = ssl_verify
        self.ssl_cert = ssl_cert
        self.http_auth = http_auth
        self.exc_class = AptlyAPIException

        while self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]

    def _error_from_response(self, resp: requests.Response) -> str:
        if resp.status_code == 200:
            return "no error (status 200)"

        try:
            rcnt = resp.json()
        except ValueError:
            return "%s %s %s" % (resp.status_code, resp.reason, resp.text,)

        if isinstance(rcnt, dict):
            content = rcnt
        else:
            content = rcnt[0]

        ret = "%s - %s -" % (resp.status_code, resp.reason)
        if "error" in content:
            ret = "%s %s" % (ret, content["error"],)
        if "meta" in content:
            ret = "%s (%s)" % (ret, content["meta"],)
        return ret

    def _makeurl(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def do_get(self, urlpath: str, params: Dict[str, str]=None) -> requests.Response:
        resp = requests.get(self._makeurl(urlpath), params=params, verify=self.ssl_verify,
                            cert=self.ssl_cert, auth=self.http_auth)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_post(self, urlpath: str, data: Union[bytes, MutableMapping[str, str], IO[Any]]=None,
                params: Dict[str, str]=None,
                files: Union[
                    Dict[str, IO],
                    Dict[str, Tuple[str, IO, Optional[str], Optional[Dict[str, str]]]],
                    Dict[str, Tuple[str, str]],
                    Sequence[Tuple[str, IO]],
                    Sequence[Tuple[str, IO, Optional[str], Optional[Dict[str, str]]]]
                ]=None,
                json: MutableMapping[Any, Any]=None) -> requests.Response:
        resp = requests.post(self._makeurl(urlpath), data=data, params=params, files=files, json=json,
                             verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_put(self, urlpath: str, data: Union[bytes, MutableMapping[str, str], IO[Any]]=None,
               files: Union[
                   Dict[str, IO],
                   Dict[str, Tuple[str, IO, Optional[str], Optional[Dict[str, str]]]],
                   Dict[str, Tuple[str, str]],
                   Sequence[Tuple[str, IO]],
                   Sequence[Tuple[str, IO, Optional[str], Optional[Dict[str, str]]]]
               ]=None,
               json: MutableMapping[Any, Any]=None) -> requests.Response:
        resp = requests.put(self._makeurl(urlpath), data=data, files=files, json=json,
                            verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_delete(self, urlpath: str, params: Dict[str, str]=None,
                  data: Union[str, Dict[str, str], Sequence[Tuple[str, str]]]=None,
                  json: Union[List[Dict[str, Any]], Dict[str, Any]]=None) -> requests.Response:
        resp = requests.delete(self._makeurl(urlpath), params=params, data=data, json=json,
                               verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp
