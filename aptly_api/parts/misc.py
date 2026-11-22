# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import cast

import requests

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

    def _do_get_clear_404(self) -> requests.Response:
        try:
            return self.do_get("api/ready")
        except AptlyAPIException as error:
            # This is needed to hide the exception masking the 404 error
            if error.status_code == 404:
                raise NotImplementedError("The Ready API is not yet supported") from error
            # 503 is needed by api/ready for returning its unready condition
            if error.status_code not in {200, 503}:
                raise AptlyAPIException("Aptly server returned an unexpected status_code " + str(error.status_code)) from error
            raise

    def ready(self) -> str:
        resp = self._do_get_clear_404()

        if "Status" not in resp.json():
            raise AptlyAPIException("Aptly server didn't return a valid response object:\n%s" % resp.text)

        return cast(str, resp.json()["Status"])
