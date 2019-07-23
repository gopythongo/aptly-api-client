# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import cast

from aptly_api.base import AptlyAPIException, BaseAPIClient


class MiscAPISection(BaseAPIClient):
    def graph(self, ext: str, layout: str = "horizontal") -> None:
        raise NotImplementedError("The Graph API is not yet supported")

    def version(self) -> str:
        resp = self.do_get("api/version")
        if "Version" in resp.json():
            return cast(str, resp.json()["Version"])
        else:
            raise AptlyAPIException("Aptly server didn't return a valid response object:\n%s" % resp.text)
