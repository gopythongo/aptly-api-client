# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from typing import Sequence, List, Tuple, BinaryIO, cast, Optional  # noqa: F401

from aptly_api.base import BaseAPIClient, AptlyAPIException


class FilesAPISection(BaseAPIClient):
    def list(self, directory: Optional[str] = None) -> Sequence[str]:
        if directory is None:
            resp = self.do_get("api/files")
        else:
            resp = self.do_get("api/files/%s" % directory)

        return cast(List[str], resp.json())

    def upload(self, destination: str, *files: str) -> Sequence[str]:
        to_upload = []  # type: List[Tuple[str, BinaryIO]]
        for f in files:
            if not os.path.exists(f) or not os.access(f, os.R_OK):
                raise AptlyAPIException("File to upload %s can't be opened or read" % f)
            fh = open(f, mode="rb")
            to_upload.append((f, fh),)

        try:
            resp = self.do_post("api/files/%s" % destination,
                                files=to_upload)
        except AptlyAPIException:
            raise
        finally:
            for fn, to_close in to_upload:
                if not to_close.closed:
                    to_close.close()

        return cast(List[str], resp.json())

    def delete(self, path: Optional[str] = None) -> None:
        self.do_delete("api/files/%s" % path)
