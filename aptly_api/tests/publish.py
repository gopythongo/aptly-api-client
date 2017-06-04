# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from unittest.case import TestCase
from typing import Any

import requests_mock

from aptly_api.parts.publish import PublishEndpoint, PublishAPISection


@requests_mock.Mocker(kw='rmock')
class PublishAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.papi = PublishAPISection("http://test/")

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/publish",
                  text='[{"Architectures":["amd64"],"Distribution":"mn-nightly","Label":"",'
                       '"Origin":"","Prefix":"nightly/stretch","SkipContents":false,'
                       '"SourceKind":"local","Sources":[{"Component":"main","Name":"maurusnet"}],'
                       '"Storage":"s3:maurusnet"}]')
        self.assertListEqual(
            self.papi.list(),
            [
                PublishEndpoint(
                    storage='s3:maurusnet',
                    prefix='nightly/stretch',
                    distribution='mn-nightly',
                    source_kind='local',
                    sources=[{
                        'Name': 'maurusnet',
                        'Component': 'main'
                    }],
                    architectures=['amd64'],
                    label='',
                    origin=''
                )
            ]
        )

    def test_update(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/publish/s3%3Aaptly-repo%3Atest_xyz__1/test",
                  text='{"Architectures":["amd64"],"Distribution":"test","Label":"",'
                       '"Origin":"","Prefix":"test/xyz_1","SkipContents":false,'
                       '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                       '"Storage":"s3:aptly-repo"}')
        self.assertEqual(
            self.papi.update(
                prefix="s3:aptly-repo:test/xyz_1",
                distribution="test",
                sign_batch=True,
                sign_gpgkey="A16BE921",
                sign_passphrase="123456",
            ),
            PublishEndpoint(
                storage='s3:aptly-repo',
                prefix='test/xyz_1',
                distribution='test',
                source_kind='local',
                sources=[{
                    'Name': 'aptly-repo',
                    'Component': 'main'
                }],
                architectures=['amd64'],
                label='',
                origin=''
            )
        )

    def test_publish(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/publish/s3%3Amyendpoint%3Atest_a__1",
                   text='{"Architectures":["amd64"],"Distribution":"test","Label":"",'
                        '"Origin":"","Prefix":"test/a_1","SkipContents":false,'
                        '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                        '"Storage":"s3:myendpoint"}')
        self.assertEqual(
            self.papi.publish(
                sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                prefix='s3:myendpoint:test/a_1', distribution='test', sign_batch=True,
                sign_gpgkey='A16BE921', sign_passphrase='*********'
            ),
            PublishEndpoint(
                storage='s3:myendpoint',
                prefix='test/a_1',
                distribution='test',
                source_kind='local',
                sources=[{'Component': 'main', 'Name': 'aptly-repo'}],
                architectures=['amd64'],
                label='',
                origin=''
            )
        )
