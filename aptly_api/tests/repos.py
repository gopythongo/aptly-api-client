# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any
from unittest.case import TestCase

import requests_mock

from aptly_api.base import AptlyAPIException
from aptly_api.parts.packages import Package
from aptly_api.parts.repos import ReposAPISection, Repo, FileReport


@requests_mock.Mocker(kw='rmock')
class ReposAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.rapi = ReposAPISection("http://test/")

    def test_create(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/repos",
                   text='{"Name":"aptly-repo","Comment":"test","DefaultDistribution":"test","DefaultComponent":"test"}')
        self.assertEqual(
            self.rapi.create("aptly-repo", comment="test", default_component="test", default_distribution="test"),
            Repo(
                name="aptly-repo",
                default_distribution="test",
                default_component="test",
                comment="test",
            )
        )

    def test_show(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/repos/aptly-repo",
                  text='{"Name":"aptly-repo","Comment":"","DefaultDistribution":"","DefaultComponent":""}')
        self.assertEqual(
            self.rapi.show("aptly-repo"),
            Repo(
                name="aptly-repo",
                default_distribution="",
                default_component="",
                comment="",
            )
        )

    def test_search(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/repos/aptly-repo/packages",
                  text='["Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9"]')
        self.assertSequenceEqual(
            self.rapi.search_packages("aptly-repo"),
            [
                Package(
                    key="Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9",
                    short_key=None,
                    files_hash=None,
                    fields=None,
                )
            ],
        )

    def test_search_details(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get(
            "http://test/api/repos/aptly-repo/packages?format=details",
            text="""[{
                      "Architecture":"amd64",
                      "Depends":"python3, python3-pip, python3-virtualenv, adduser, cron-daemon",
                      "Description":" no description given\\n",
                      "Filename":"authserver_0.1.14~dev0-1.deb",
                      "FilesHash":"1cc572a93625a9c9",
                      "Homepage":"http://example.com/no-uri-given",
                      "Installed-Size":"74927",
                      "Key":"Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9",
                      "License":"unknown",
                      "MD5sum":"03cca0794e63cf147b879e0a3695f523",
                      "Maintainer":"Jonas Maurus",
                      "Package":"authserver",
                      "Priority":"extra",
                      "Provides":"maurusnet-authserver",
                      "SHA1":"9a77a31dba51f612ee08ee096381f0c7e8f97a42",
                      "SHA256":"63555a135bf0aa1762d09fc622881aaf352cdb3b244da5d78278c7efa2dba8b7",
                      "SHA512":"01f9ca888014599374bf7a2c8c46f895d7ef0dfea99dfd092007f9fc5d5fe57a2755b843eda296b65cb"""
                 """6ac0f64b9bd88b507221a71825f5329fdda0e58728cd7",
                      "Section":"default",
                      "ShortKey":"Pamd64 authserver 0.1.14~dev0-1",
                      "Size":"26623042",
                      "Vendor":"root@test",
                      "Version":"0.1.14~dev0-1"
                 }]"""
        )
        self.assertSequenceEqual(
            self.rapi.search_packages("aptly-repo", detailed=True, with_deps=True, query="Name (authserver)"),
            [
                Package(
                    key='Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9',
                    short_key='Pamd64 authserver 0.1.14~dev0-1',
                    files_hash='1cc572a93625a9c9',
                    fields={
                        'Architecture': 'amd64',
                        'Depends': 'python3, python3-pip, python3-virtualenv, adduser, cron-daemon',
                        'Description': ' no description given\n',
                        'Filename': 'authserver_0.1.14~dev0-1.deb',
                        'FilesHash': '1cc572a93625a9c9',
                        'Homepage': 'http://example.com/no-uri-given',
                        'Installed-Size': '74927',
                        'Key': 'Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9',
                        'License': 'unknown',
                        'MD5sum': '03cca0794e63cf147b879e0a3695f523',
                        'Maintainer': 'Jonas Maurus',
                        'Package': 'authserver',
                        'Priority': 'extra',
                        'Provides': 'maurusnet-authserver',
                        'SHA1': '9a77a31dba51f612ee08ee096381f0c7e8f97a42',
                        'SHA256': '63555a135bf0aa1762d09fc622881aaf352cdb3b244da5d78278c7efa2dba8b7',
                        'SHA512': '01f9ca888014599374bf7a2c8c46f895d7ef0dfea99dfd092007f9fc5d5fe57a2755b843eda296b65'
                                  'cb6ac0f64b9bd88b507221a71825f5329fdda0e58728cd7',
                        'Section': 'default',
                        'ShortKey': 'Pamd64 authserver 0.1.14~dev0-1',
                        'Size': '26623042',
                        'Vendor': 'root@test',
                        'Version': '0.1.14~dev0-1'
                    }
                )
            ]
        )

    def test_repo_edit_validation(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.rapi.edit("aptly-repo")

    def test_repo_edit(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/repos/aptly-repo",
                  text='{"Name":"aptly-repo","Comment":"comment",'
                       '"DefaultDistribution":"stretch","DefaultComponent":"main"}')
        self.assertEqual(
            self.rapi.edit("aptly-repo", comment="comment", default_distribution="stretch", default_component="main"),
            Repo(name='aptly-repo', comment='comment', default_distribution='stretch', default_component='main')
        )

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/repos",
                  text='[{"Name":"maurusnet","Comment":"","DefaultDistribution":"",'
                       '"DefaultComponent":"main"},{"Name":"aptly-repo","Comment":"comment",'
                       '"DefaultDistribution":"stretch","DefaultComponent":"main"}]')
        self.assertSequenceEqual(
            self.rapi.list(),
            [
                Repo(name='maurusnet', comment='', default_distribution='', default_component='main'),
                Repo(name='aptly-repo', comment='comment', default_distribution='stretch', default_component='main'),
            ]
        )

    def test_delete(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(requests_mock.NoMockAddress):
            self.rapi.delete("aptly-repo", force=True)

    def test_add_file(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/repos/aptly-repo/file/test/dirmngr_2.1.18-6_amd64.deb",
                   text='{"FailedFiles":[],"Report":{"Warnings":[],'
                        '"Added":["dirmngr_2.1.18-6_amd64 added"],"Removed":[]}}')
        self.assertEqual(
            self.rapi.add_uploaded_file("aptly-repo", "test", "dirmngr_2.1.18-6_amd64.deb", force_replace=True),
            FileReport(failed_files=[],
                       report={'Added': ['dirmngr_2.1.18-6_amd64 added'],
                               'Removed': [], 'Warnings': []})
        )

    def test_add_dir(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/repos/aptly-repo/file/test",
                   text='{"FailedFiles":[],"Report":{"Warnings":[],'
                        '"Added":["dirmngr_2.1.18-6_amd64 added"],"Removed":[]}}')
        self.assertEqual(
            self.rapi.add_uploaded_file("aptly-repo", "test", force_replace=True),
            FileReport(failed_files=[],
                       report={'Added': ['dirmngr_2.1.18-6_amd64 added'],
                               'Removed': [], 'Warnings': []})
        )

    def test_add_package(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/repos/aptly-repo/packages",
                   text='{"Name":"aptly-repo","Comment":"","DefaultDistribution":"","DefaultComponent":""}')
        self.assertEqual(
            self.rapi.add_packages_by_key("aptly-repo", "Pamd64 dirmngr 2.1.18-6 4c7412c5f0d7b30a"),
            Repo(name='aptly-repo', comment='', default_distribution='', default_component='')
        )

    def test_delete_package(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.delete(
            "http://test/api/repos/aptly-repo/packages",
            text='{"Name":"aptly-repo","Comment":"","DefaultDistribution":"","DefaultComponent":""}'
        )
        self.assertEqual(
            self.rapi.delete_packages_by_key("aptly-repo", "Pamd64 dirmngr 2.1.18-6 4c7412c5f0d7b30a"),
            Repo(name='aptly-repo', comment='', default_distribution='', default_component=''),
        )

    def test_search_invalid_params(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.rapi.search_packages("aptly-repo", with_deps=True)
