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

    def test_metrics(self, *, rmock: requests_mock.Mocker) -> None:
        with open('./aptly_api/tests/test_data/metrics.txt') as test_file:
            test_data = test_file.read()
            rmock.get("http://test/api/metrics", text=test_data)
            self.assertEqual(self.mapi.metrics(), test_data)

    def test_metrics_non_200_status_code(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("GET", "http://test/api/metrics", status_code=204, text="")
        with self.assertRaises(AptlyAPIException):
            self.mapi.metrics()

    def test_metrics_api_disabled_or_missing(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("GET", "http://test/api/metrics", status_code=404, text="404 page not found")
        with self.assertRaises(NotImplementedError):
            self.mapi.metrics()

