# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from unittest.case import TestCase
from typing import Any

import requests_mock

from aptly_api.base import AptlyAPIException
from aptly_api.parts.publish import PublishEndpoint, PublishAPISection


@requests_mock.Mocker(kw='rmock')
class PublishAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.papi = PublishAPISection("http://test/")
        self.maxDiff = None

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

    def test_update_passphrase_file(self, *, rmock: requests_mock.Mocker) -> None:
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
                sign_passphrase_file="/root/passphrase.txt",
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

    def test_update_no_sign(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/publish/s3%3Aaptly-repo%3Atest_xyz__1/test",
                  text='{"Architectures":["amd64"],"Distribution":"test","Label":"",'
                       '"Origin":"","Prefix":"test/xyz_1","SkipContents":false,'
                       '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                       '"Storage":"s3:aptly-repo"}')
        self.assertEqual(
            self.papi.update(
                prefix="s3:aptly-repo:test/xyz_1",
                distribution="test",
                sign_skip=True,
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

    def test_update_snapshots(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/publish/s3%3Aaptly-repo%3Atest_xyz__1/test",
                  text='{"Architectures":["amd64"],"Distribution":"test","Label":"",'
                       '"Origin":"","Prefix":"test/xyz_1","SkipContents":false,'
                       '"SourceKind":"snapshot","Sources":[{"Component":"main","Name":"aptly-repo-1"}],'
                       '"Storage":"s3:aptly-repo"}')
        self.assertEqual(
            self.papi.update(
                prefix="s3:aptly-repo:test/xyz_1",
                distribution="test",
                snapshots=[{"Name": "aptly-repo-1"}],
                force_overwrite=True,
                sign_batch=True,
                sign_gpgkey="A16BE921",
                sign_passphrase="123456",
                sign_keyring="/etc/gpg-managed-keyring/pubring.pub",
                sign_secret_keyring="/etc/gpg-managed-keyring/secring.gpg"
            ),
            PublishEndpoint(
                storage='s3:aptly-repo',
                prefix='test/xyz_1',
                distribution='test',
                source_kind='snapshot',
                sources=[{
                    'Name': 'aptly-repo-1',
                    'Component': 'main',
                }],
                architectures=['amd64'],
                label='',
                origin=''
            )
        )

    def test_publish(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/publish/s3%3Amyendpoint%3Atest_a__1",
                   text='{"Architectures":["amd64"],"Distribution":"test","Label":"test",'
                        '"Origin":"origin","Prefix":"test/a_1","SkipContents":false,'
                        '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                        '"Storage":"s3:myendpoint"}')
        self.assertEqual(
            self.papi.publish(
                sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                prefix='s3:myendpoint:test/a_1', distribution='test', label='test', origin='origin',
                sign_batch=True, sign_gpgkey='A16BE921', sign_passphrase='*********',
                force_overwrite=True, sign_keyring="/etc/gpg-managed-keyring/pubring.pub",
                sign_secret_keyring="/etc/gpg-managed-keyring/secring.gpg"
            ),
            PublishEndpoint(
                storage='s3:myendpoint',
                prefix='test/a_1',
                distribution='test',
                source_kind='local',
                sources=[{'Component': 'main', 'Name': 'aptly-repo'}],
                architectures=['amd64'],
                label='test',
                origin='origin'
            )
        )

    def test_publish_passphrase_file(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/publish/s3%3Amyendpoint%3Atest_a__1",
                   text='{"Architectures":["amd64"],"Distribution":"test","Label":"test",'
                        '"Origin":"origin","Prefix":"test/a_1","SkipContents":false,'
                        '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                        '"Storage":"s3:myendpoint"}')
        self.assertEqual(
            self.papi.publish(
                sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                prefix='s3:myendpoint:test/a_1', distribution='test', label='test', origin='origin',
                sign_batch=True, sign_gpgkey='A16BE921', sign_passphrase_file='/root/passphrase.txt',
                force_overwrite=True, sign_keyring="/etc/gpg-managed-keyring/pubring.pub",
                sign_secret_keyring="/etc/gpg-managed-keyring/secring.gpg"
            ),
            PublishEndpoint(
                storage='s3:myendpoint',
                prefix='test/a_1',
                distribution='test',
                source_kind='local',
                sources=[{'Component': 'main', 'Name': 'aptly-repo'}],
                architectures=['amd64'],
                label='test',
                origin='origin'
            )
        )

    def test_publish_no_sign(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/publish/s3%3Amyendpoint%3Atest_a__1",
                   text='{"Architectures":["amd64"],"Distribution":"test","Label":"test",'
                        '"Origin":"origin","Prefix":"test/a_1","SkipContents":false,'
                        '"SourceKind":"local","Sources":[{"Component":"main","Name":"aptly-repo"}],'
                        '"Storage":"s3:myendpoint"}')
        self.assertEqual(
            self.papi.publish(
                sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                prefix='s3:myendpoint:test/a_1', distribution='test', label='test', origin='origin',
                sign_skip=True
            ),
            PublishEndpoint(
                storage='s3:myendpoint',
                prefix='test/a_1',
                distribution='test',
                source_kind='local',
                sources=[{'Component': 'main', 'Name': 'aptly-repo'}],
                architectures=['amd64'],
                label='test',
                origin='origin'
            )
        )

    def test_no_key(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.papi.publish(sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                              prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False)
        with self.assertRaises(AptlyAPIException):
            self.papi.update(prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False)

    def test_double_passphrase(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.papi.publish(sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                              prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False,
                              sign_gpgkey='A16BE921', sign_passphrase="*******", sign_passphrase_file="****")
        with self.assertRaises(AptlyAPIException):
            self.papi.update(prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False,
                             sign_gpgkey='A16BE921', sign_passphrase="*******", sign_passphrase_file="****")

    def test_no_name(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.papi.publish(sources=[{'nope': 'nope'}], architectures=['amd64'],
                              prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False,
                              sign_gpgkey='A16BE921', sign_passphrase="*******")
        with self.assertRaises(AptlyAPIException):
            self.papi.update(snapshots=[{'nope': 'nope'}],
                             prefix='s3:myendpoint:test/a_1', distribution='test', sign_skip=False,
                             sign_gpgkey='A16BE921', sign_passphrase="*******")

    def test_drop(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.delete("http://test/api/publish/s3%3Amyendpoint%3Atest_a__1/test?force=1", text='{}')
        self.papi.drop(prefix='s3:myendpoint:test/a_1', distribution='test', force_delete=True)
