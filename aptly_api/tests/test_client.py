# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any, cast
from unittest.case import TestCase

import requests
import requests_mock

from aptly_api import Client as AptlyClient


# as we're testing the individual parts, this is rather simple
from aptly_api.base import AptlyAPIException


class ClientTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.client = AptlyClient("http://test/")

    def test_instantiate(self) -> None:
        cl = AptlyClient("http://test/")
        self.assertEqual(
            str(cl),
            "Client (Aptly API Client) <http://test/>"
        )

    @requests_mock.Mocker(kw='rmock')
    def test_api_subdir_get(self, *, rmock: requests_mock.Mocker) -> None:
        # register mock:// scheme with urllib.parse
        import urllib.parse
        urllib.parse.uses_netloc.append('mock')
        urllib.parse.uses_relative.append('mock')
        urllib.parse.uses_fragment.append('mock')
        urllib.parse.uses_params.append('mock')

        cl = AptlyClient("mock://test/basedir/")
        rmock.get("mock://test/basedir/api/test", status_code=200, text='')
        cl.files.do_get("api/test")
        self.assertTrue(rmock.called)

    def test_error_no_error(self) -> None:
        class MockResponse:
            def __init__(self, status_code: int = 200) -> None:
                self.status_code = status_code

        self.assertEqual(
            self.client.files._error_from_response(cast(requests.Response, MockResponse())),
            "no error (status 200)"
        )

    def test_error_no_json(self) -> None:
        adapter = requests_mock.Adapter()
        adapter.register_uri("GET", "mock://test/api", status_code=400, text="this is not json", reason="test")
        session = requests.session()
        session.mount("mock", adapter)
        resp = session.get("mock://test/api")

        self.assertEqual(
            self.client.files._error_from_response(resp),
            "400 test this is not json"
        )

    def test_error_dict(self) -> None:
        adapter = requests_mock.Adapter()
        adapter.register_uri("GET", "mock://test/api", status_code=400, text='{"error": "error", "meta": "meta"}',
                             reason="test")
        session = requests.session()
        session.mount("mock", adapter)
        resp = session.get("mock://test/api")
        self.assertEqual(
            self.client.files._error_from_response(resp),
            "400 - test - error (meta)"
        )

    def test_error_list(self) -> None:
        adapter = requests_mock.Adapter()
        adapter.register_uri("GET", "mock://test/api", status_code=400, text='[{"error": "error", "meta": "meta"}]',
                             reason="test")
        session = requests.session()
        session.mount("mock", adapter)
        resp = session.get("mock://test/api")
        self.assertEqual(
            self.client.files._error_from_response(resp),
            "400 - test - error (meta)"
        )

    @requests_mock.Mocker(kw='rmock')
    def test_error_get(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("GET", "mock://test/api", status_code=400, text='[{"error": "error", "meta": "meta"}]',
                           reason="test")
        with self.assertRaises(AptlyAPIException):
            self.client.files.do_get("mock://test/api")

    @requests_mock.Mocker(kw='rmock')
    def test_error_get_api_ready_503_code(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("GET", "mock://test/api/ready", status_code=503, text='{"Status":"Aptly is unavailable"}')
        self.assertEqual(self.client.files.do_get("mock://test/api/ready").status_code, 503)
        self.assertEqual(self.client.files.do_get("mock://test/api/ready").json()["Status"], "Aptly is unavailable")

    @requests_mock.Mocker(kw='rmock')
    def test_error_post(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("POST", "mock://test/api", status_code=400, text='[{"error": "error", "meta": "meta"}]',
                           reason="test")
        with self.assertRaises(AptlyAPIException):
            self.client.files.do_post("mock://test/api")

    @requests_mock.Mocker(kw='rmock')
    def test_error_put(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("PUT", "mock://test/api", status_code=400, text='[{"error": "error", "meta": "meta"}]',
                           reason="test")
        with self.assertRaises(AptlyAPIException):
            self.client.files.do_put("mock://test/api")

    @requests_mock.Mocker(kw='rmock')
    def test_error_delete(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.register_uri("DELETE", "mock://test/api", status_code=400, text='[{"error": "error", "meta": "meta"}]',
                           reason="test")
        with self.assertRaises(AptlyAPIException):
            self.client.files.do_delete("mock://test/api")
