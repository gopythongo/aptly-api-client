# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import IO, TextIO, BinaryIO, Sequence, Dict, Tuple, Optional, Union, List, Any, MutableMapping, Iterable, \
    Mapping
from urllib.parse import urljoin

import requests
from requests.auth import AuthBase

_filetype = Optional[
    Union[
        Dict[
            str, Union[
                Union[TextIO, BinaryIO, str, bytes],
                Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes]],
                Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes], str],
                Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes], str, Dict[str, str]]
            ]
        ],
        Sequence[
            Tuple[
                str, Union[
                    Union[TextIO, BinaryIO, str, bytes],
                    Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes]],
                    Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes], str],
                    Tuple[Optional[str], Union[TextIO, BinaryIO, str, bytes], str, Dict[str, str]]
                ]
            ]
        ],
    ]
]

_datatype = Optional[
    Union[
        Iterable[bytes],
        str,
        bytes,
        Union[TextIO, BinaryIO],
        List[Tuple[Any, Any]],
        Tuple[Tuple[Any, Any], ...],
        Mapping[Any, Any]
    ]
]


class AptlyAPIException(Exception):
    def __init__(self, *args: Any, status_code: int = 0) -> None:
        super().__init__(*args)
        self.status_code = status_code


class BaseAPIClient:
    def __init__(self, base_url: str, ssl_verify: Union[str, bool, None] = None,
                 ssl_cert: Optional[Tuple[str, str]] = None, http_auth: Optional[AuthBase] = None,
                 timeout: int = 60) -> None:
        self.base_url = base_url
        self.ssl_verify = ssl_verify
        self.ssl_cert = ssl_cert
        self.http_auth = http_auth
        self.exc_class = AptlyAPIException
        self.timeout = timeout

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

    def _make_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def do_get(self, urlpath: str, params: Optional[Dict[str, str]] = None) -> requests.Response:
        resp = requests.get(self._make_url(urlpath), params=params, verify=self.ssl_verify,
                            cert=self.ssl_cert, auth=self.http_auth, timeout=self.timeout)

        if resp.status_code < 200 or resp.status_code >= 300 and resp.status_code != 503:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_post(self, urlpath: str, data: Union[bytes, MutableMapping[str, str], IO[Any], None] = None,
                params: Optional[Dict[str, str]] = None,
                files: _filetype = None,
                json: Optional[MutableMapping[Any, Any]] = None) -> requests.Response:
        resp = requests.post(self._make_url(urlpath), data=data, params=params, files=files, json=json,
                             verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth,
                             timeout=self.timeout)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_put(self, urlpath: str, data: Union[bytes, MutableMapping[str, str], IO[Any], None] = None,
               files: _filetype = None,
               json: Optional[MutableMapping[Any, Any]] = None) -> requests.Response:
        resp = requests.put(self._make_url(urlpath), data=data, files=files, json=json,
                            verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth,
                            timeout=self.timeout)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp

    def do_delete(self, urlpath: str, params: Optional[Dict[str, str]] = None,
                  data: _datatype = None,
                  json: Union[List[Dict[str, Any]], Dict[str, Any], None] = None) -> requests.Response:
        resp = requests.delete(self._make_url(urlpath), params=params, data=data, json=json,
                               verify=self.ssl_verify, cert=self.ssl_cert, auth=self.http_auth,
                               timeout=self.timeout)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp
