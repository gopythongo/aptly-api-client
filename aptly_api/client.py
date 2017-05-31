# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import NamedTuple, Sequence, Dict

from aptly_api.base import AptlyAPIException
from aptly_api.parts.repos import ReposClient
from aptly_api.parts.files import FilesClient


class Client:
    def __init__(self, aptly_server_url: str) -> None:
        self.aptly_server_url = aptly_server_url
        self.repos = ReposClient()
