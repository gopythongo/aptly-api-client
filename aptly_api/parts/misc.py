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

    def _do_get_healthy_clear_404(self) -> requests.Response:
        try:
            return self.do_get("api/healthy")
        except AptlyAPIException as error:
            if error.status_code == HTTP_CODE_404:
                msg = "The Healthy API is not yet supported"
                raise NotImplementedError(msg) from error
            raise

    def healthy(self) -> str:
        resp = self._do_get_healthy_clear_404()

        if "Status" not in resp.json():
            msg = f"Aptly server didn't return a valid response object:\n{resp.text}"
            raise AptlyAPIException(msg)

        return cast(str, resp.json()["Status"])
