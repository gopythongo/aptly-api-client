# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any
from unittest.case import TestCase

import requests_mock

from aptly_api.base import AptlyAPIException
from aptly_api.parts.misc import MiscAPISection


@requests_mock.Mocker(kw='rmock')
class MiscAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.mapi = MiscAPISection("http://test/")

    def test_version(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/version", text='{"Version":"1.0.1"}')
        self.assertEqual(self.mapi.version(), "1.0.1")

    def test_graph(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(NotImplementedError):
            self.mapi.graph("png")

    def test_version_error(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/version", text='{"droenk": "blah"}')
        with self.assertRaises(AptlyAPIException):
            self.mapi.version()

    def test_healthy(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/healthy", text='{"Status":"Aptly is healthy"}')
        self.assertEqual(self.mapi.healthy(), "Aptly is healthy")

    def test_healthy_error(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/healthy", text='{"dronek": "blah"}')
        with self.assertRaises(AptlyAPIException):
            self.mapi.healthy()

    def test_healthy_aptly_to_old(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("GET", "http://test/api/healthy", status_code=404, text="Not Found")
        rmock.get("http://test/api/healthy")
        with self.assertRaises(NotImplementedError):
            self.mapi.healthy()
