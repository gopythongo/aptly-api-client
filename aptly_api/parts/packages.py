# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import NamedTuple, Dict

from aptly_api.base import AptlyAPIException


class PackageAPIException(AptlyAPIException):
    pass


Package = NamedTuple('Package',[
    ('key', str),
    ('short_key', str),
    ('files_hash', str),
    ('fields', Dict[str, str]),
])


class PackageAPIClient:
    def __init__(self) -> None:
        pass

    def show(self, key: str) -> Package:
        pass
