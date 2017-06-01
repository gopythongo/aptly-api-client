# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Sequence

from aptly_api.base import BaseAPIClient


class FilesAPISection(BaseAPIClient):
    def list(self, directory: str=None) -> Sequence[str]:
        pass

    def upload(self, destination: str, *files: str) -> Sequence[str]:
        pass

    def delete(self, path: str=None) -> None:
        pass
