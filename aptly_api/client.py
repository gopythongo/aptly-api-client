# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from requests.auth import AuthBase
from typing import Union, Optional, Tuple

from aptly_api.parts.misc import MiscAPISection
from aptly_api.parts.packages import PackageAPISection
from aptly_api.parts.publish import PublishAPISection
from aptly_api.parts.repos import ReposAPISection
from aptly_api.parts.files import FilesAPISection
from aptly_api.parts.snapshots import SnapshotAPISection


class Client:
    def __init__(self, aptly_server_url: str, ssl_verify: Union[str, bool, None] = None,
                 ssl_cert: Optional[Tuple[str, str]] = None, http_auth: Optional[AuthBase] = None,
                 timeout: int = 60) -> None:
        self.__aptly_server_url = aptly_server_url
        self.files = FilesAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                     ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)
        self.misc = MiscAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                   ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)
        self.packages = PackageAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                          ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)
        self.publish = PublishAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                         ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)
        self.repos = ReposAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                     ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)
        self.snapshots = SnapshotAPISection(base_url=self.__aptly_server_url, ssl_verify=ssl_verify,
                                            ssl_cert=ssl_cert, http_auth=http_auth, timeout=timeout)

    @property
    def aptly_server_url(self) -> str:
        return self.__aptly_server_url

    def __repr__(self) -> str:
        return "Client (Aptly API Client) <%s>" % self.aptly_server_url
