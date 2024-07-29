# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any
from unittest.case import TestCase
from inspect import signature
import json

import requests_mock

from aptly_api.parts.packages import Package
from aptly_api.parts.mirrors import MirrorsAPISection, Mirror


@requests_mock.Mocker(kw='rmock')
class MirrorsAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.miapi = MirrorsAPISection("http://test/")

    def test_create(self, *, rmock: requests_mock.Mocker) -> None:
        expected = {"Name": "testname", "ArchiveURL": "http://randomurl.url"}

        rmock.post("http://test/api/mirrors", text="""{"Name":"nocheck", "ArchiveRoot":"nocheck"}""")
        self.miapi.create(expected["Name"], expected["ArchiveURL"])

        self.assertEqual(rmock.request_history[0].method, "POST")
        self.assertEqual(len(rmock.request_history[0].json()), len(expected))
        self.assertEqual(rmock.request_history[0].json(), expected)

    def test_create_all_args(self, *, rmock: requests_mock.Mocker) -> None:
        expected = {
            "Name": "aptly-mirror",
            "ArchiveURL": "https://deb.nodesource.com/node_10.x/",
            "Distribution": "bionic",
            "Filter": "test",
            "Components": ["main"],
            "Architectures": ["amd64"],
            "Keyrings": ["/path/to/keyring"],
            "DownloadSources": True,
            "DownloadUdebs": True,
            "DownloadInstaller": True,
            "FilterWithDeps": True,
            "SkipComponentCheck": True,
            "SkipArchitectureCheck": True,
            "IgnoreSignatures": True,
        }
        # Keep us from getting out of lockstep with the number of args to create
        self.assertEqual(len(signature(self.miapi.create).parameters), len(expected))

        rmock.post("http://test/api/mirrors", text="""{"Name":"nocheck", "ArchiveRoot":"nocheck"}""")
        self.miapi.create(
            name="aptly-mirror",
            archiveurl="https://deb.nodesource.com/node_10.x/",
            distribution="bionic",
            filter="test",
            components=["main"],
            architectures=["amd64"],
            keyrings=["/path/to/keyring"],
            download_sources=True,
            download_udebs=True,
            download_installer=True,
            filter_with_deps=True,
            skip_component_check=True,
            skip_architecture_check=True,
            ignore_signatures=True,
        )

        self.assertEqual(rmock.request_history[0].method, "POST")
        self.assertEqual(len(rmock.request_history[0].json()), len(expected))
        self.assertEqual(rmock.request_history[0].json(), expected)

    def test_mirror_from_response(self, *, rmock: requests_mock.Mocker) -> None:
        self.assertSequenceEqual(
            self.miapi.mirror_from_response(
                json.loads("""{
                    "UUID": "2cb5985a-a23f-4a1f-8eb6-d5409193b4eb",
                    "Name": "aptly-mirror",
                    "ArchiveRoot": "https://deb.nodesource.com/node_10.x/",
                    "Distribution": "bionic",
                    "Components": ["main"],
                    "Architectures": ["amd64"],
                    "LastDownloadDate": "0001-01-01T00:00:00Z",
                    "Meta": [{"Architectures": "i386 amd64 armhf arm64",
                            "Codename": "bionic",
                            "Components": "main",
                            "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                            "Description": " Apt Repository for the Node.JS 10.x Branch",
                            "Label": "Node Source",
                            "Origin": "Node Source"}],
                    "Filter": "test",
                    "Status": 0,
                    "WorkerPID": 0,
                    "FilterWithDeps": true,
                    "SkipComponentCheck": true,
                    "SkipArchitectureCheck": true,
                    "DownloadSources": true,
                    "DownloadUdebs": true,
                    "DownloadInstaller": true
                }""")
            ),
            Mirror(
                uuid='2cb5985a-a23f-4a1f-8eb6-d5409193b4eb',
                name="aptly-mirror",
                archiveurl="https://deb.nodesource.com/node_10.x/",
                distribution='bionic',
                components=['main'],
                architectures=['amd64'],
                downloaddate='0001-01-01T00:00:00Z',
                meta=[{"Architectures": "i386 amd64 armhf arm64",
                      "Codename": "bionic",
                       "Components": "main",
                       "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                       "Description": " Apt Repository for the Node.JS 10.x Branch",
                       "Label": "Node Source", "Origin": "Node Source"}],
                filter="test",
                status=0,
                worker_pid=0,
                filter_with_deps=True,
                skip_component_check=True,
                skip_architecture_check=True,
                download_sources=True,
                download_udebs=True,
                download_installer=True
            )
        )

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/mirrors",
                  text="""[{"UUID": "2cb5985a-a23f-4a1f-8eb6-d5409193b4eb",
                       "Name": "aptly-mirror",
                       "ArchiveRoot": "https://deb.nodesource.com/node_10.x/",
                       "Distribution": "bionic", "Components": ["main"],
                       "Architectures": ["amd64"],
                       "Meta": [{"Architectures": "i386 amd64 armhf arm64",
                       "Codename": "bionic", "Components": "main",
                       "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                       "Description": " Apt Repository for the Node.JS 10.x Branch",
                       "Label": "Node Source", "Origin": "Node Source"}],
                       "LastDownloadDate": "0001-01-01T00:00:00Z", "Filter": "",
                       "Status": 0, "WorkerPID": 0, "FilterWithDeps": false,
                       "SkipComponentCheck": false, "SkipArchitectureCheck": false,
                       "DownloadSources": false, "DownloadUdebs": false,
                       "DownloadInstaller": false}]""")
        self.assertSequenceEqual(
            self.miapi.list(),
            [
                Mirror(
                    uuid='2cb5985a-a23f-4a1f-8eb6-d5409193b4eb',
                    name="aptly-mirror",
                    archiveurl="https://deb.nodesource.com/node_10.x/",
                    distribution='bionic',
                    components=["main"],
                    architectures=["amd64"],
                    downloaddate='0001-01-01T00:00:00Z',
                    meta=[{"Architectures": "i386 amd64 armhf arm64",
                          "Codename": "bionic",
                           "Components": "main",
                           "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                           "Description": " Apt Repository for the Node.JS 10.x Branch",
                           "Label": "Node Source", "Origin": "Node Source"}],
                    filter="",
                    status=0,
                    worker_pid=0,
                    filter_with_deps=False,
                    skip_component_check=False,
                    skip_architecture_check=False,
                    download_sources=False,
                    download_udebs=False,
                    download_installer=False

                )
            ]
        )

    def test_show(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/mirrors/aptly-mirror",
                  text="""{"UUID": "2cb5985a-a23f-4a1f-8eb6-d5409193b4eb",
                       "Name": "aptly-mirror",
                       "ArchiveRoot": "https://deb.nodesource.com/node_10.x/",
                       "Distribution": "bionic", "Components": ["main"],
                       "Architectures": ["amd64"],
                       "Meta": [{"Architectures": "i386 amd64 armhf arm64",
                       "Codename": "bionic", "Components": "main",
                       "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                       "Description": " Apt Repository for the Node.JS 10.x Branch",
                       "Label": "Node Source", "Origin": "Node Source"}],
                       "LastDownloadDate": "0001-01-01T00:00:00Z", "Filter": "",
                       "Status": 0, "WorkerPID": 0, "FilterWithDeps": false,
                       "SkipComponentCheck": false, "SkipArchitectureCheck": false,
                       "DownloadSources": false, "DownloadUdebs": false,
                       "DownloadInstaller": false}""")
        self.assertSequenceEqual(
            self.miapi.show(name="aptly-mirror"),
            Mirror(
                uuid='2cb5985a-a23f-4a1f-8eb6-d5409193b4eb',
                name="aptly-mirror",
                archiveurl="https://deb.nodesource.com/node_10.x/",
                distribution='bionic',
                components=["main"],
                architectures=["amd64"],
                downloaddate='0001-01-01T00:00:00Z',
                meta=[{"Architectures": "i386 amd64 armhf arm64",
                      "Codename": "bionic",
                       "Components": "main",
                       "Date": "Tue, 06 Apr 2021 21:05:41 UTC",
                       "Description": " Apt Repository for the Node.JS 10.x Branch",
                       "Label": "Node Source", "Origin": "Node Source"}],
                filter="",
                status=0,
                worker_pid=0,
                filter_with_deps=False,
                skip_component_check=False,
                skip_architecture_check=False,
                download_sources=False,
                download_udebs=False,
                download_installer=False

            )
        )

    def test_list_packages(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/mirrors/aptly-mirror/packages",
                  text='["Pamd64 nodejs 10.24.1-1nodesource1 1f74a6abf6acc572"]')
        self.assertSequenceEqual(
            self.miapi.list_packages(
                name="aptly-mirror", query=("nodejs"), with_deps=True),
            [
                Package(
                    key="Pamd64 nodejs 10.24.1-1nodesource1 1f74a6abf6acc572",
                    short_key=None,
                    files_hash=None,
                    fields=None,
                )
            ],
        )

    def test_list_packages_details(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get(
            "http://test/api/mirrors/aptly-mirror/packages?format=details",
            text='[{"Architecture":"amd64",'
                 '"Conflicts":"nodejs-dev, nodejs-legacy, npm",'
                 '"Depends":"1libc6 (>= 2.9), libgcc1 (>= 1:3.4), '
                 'libstdc++6 (>= 4.4.0), python-minimal, ca-certificates",'
                 '"Description":" Node.js event-based server-side javascript engine\\n",'
                 '"Filename":"nodejs_10.24.1-1nodesource1_amd64.deb",'
                 '"FilesHash":"1f74a6abf6acc572",'
                 '"Homepage":"https://nodejs.org",'
                 '"Installed-Size":"78630", "Key":"Pamd64 nodejs 10.24.1-1nodesource1 1f74a6abf6acc572",'
                 '"License":"unknown",'
                 '"MD5sum":"6d9f0e30396cb6c20945ff6de2f9f322","Maintainer":"Ivan Iguaran <ivan@nodesource.com>",'
                 '"Package":"nodejs",'
                 '"Priority":"optional",'
                 '"Provides":"nodejs-dev, nodejs-legacy, npm",'
                 '"SHA1":"a3bc5a29614eab366bb3644abb1e602b5c8953d5",'
                 '"SHA256":"4b374d16b536cf1a3963ddc4575ed2b68b28b0b5ea6eefe93c942dfc0ed35177",'
                 '"SHA512":"bf203bb319de0c5f7ed3b6ba69de39b1ea8b5086b872561379bd462dd93f0796'
                 '9ca64fa01ade01ff08fa13a4e5e28625b59292ba44bc01ba876ec95875630460",'
                 '"Section":"web",'
                 '"ShortKey":"Pamd64 nodejs 10.24.1-1nodesource1",'
                 '"Size":"15949164",'
                 '"Version":"10.24.1-1nodesource1"}]')
        self.assertSequenceEqual(
            self.miapi.list_packages(
                "aptly-mirror", detailed=True, with_deps=True, query="nodejs"),
            [
                Package(
                    key='Pamd64 nodejs 10.24.1-1nodesource1 1f74a6abf6acc572',
                    short_key='Pamd64 nodejs 10.24.1-1nodesource1',
                    files_hash='1f74a6abf6acc572',
                    fields={
                        "Architecture": "amd64",
                        'Conflicts': 'nodejs-dev, nodejs-legacy, npm',
                        'Depends': '1libc6 (>= 2.9), libgcc1 (>= 1:3.4), '
                        'libstdc++6 (>= 4.4.0), python-minimal, ca-certificates',
                        'Description': ' Node.js event-based server-side javascript engine\n',
                        'Filename': 'nodejs_10.24.1-1nodesource1_amd64.deb',
                        'FilesHash': '1f74a6abf6acc572',
                        'Homepage': 'https://nodejs.org',
                        'Installed-Size': '78630',
                        'Key': 'Pamd64 nodejs 10.24.1-1nodesource1 1f74a6abf6acc572',
                        'License': 'unknown',
                        'MD5sum': '6d9f0e30396cb6c20945ff6de2f9f322',
                        'Maintainer': 'Ivan Iguaran <ivan@nodesource.com>',
                        'Package': 'nodejs',
                        'Priority': 'optional',
                        'Provides': 'nodejs-dev, nodejs-legacy, npm',
                        'SHA1': 'a3bc5a29614eab366bb3644abb1e602b5c8953d5',
                        'SHA256': '4b374d16b536cf1a3963ddc4575ed2b68b28b0b5ea6eefe93c942dfc0ed35177',
                        'SHA512': 'bf203bb319de0c5f7ed3b6ba69de39b1ea8b5086b872561379bd462dd93f0796'
                        '9ca64fa01ade01ff08fa13a4e5e28625b59292ba44bc01ba876ec95875630460',
                        'Section': 'web',
                        'ShortKey': 'Pamd64 nodejs 10.24.1-1nodesource1',
                        'Size': '15949164',
                        'Version': '10.24.1-1nodesource1'
                    }
                )
            ]
        )

    def test_delete(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(requests_mock.NoMockAddress):
            self.miapi.delete(name="aptly-mirror")

    def test_update(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(requests_mock.NoMockAddress):
            self.miapi.update(name="aptly-mirror", ignore_signatures=True)

    def test_edit(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(requests_mock.NoMockAddress):
            self.miapi.edit(name="aptly-mirror", newname="aptly-mirror-renamed",
                            archiveurl='https://deb.nodesource.com/node_10.x/',
                            architectures=["i386", "amd64"], filter="test",
                            components=["main"], keyrings=["/path/to/keyring"],
                            skip_existing_packages=True, ignore_checksums=True,
                            download_udebs=True, download_sources=True,
                            skip_component_check=True, filter_with_deps=True,
                            ignore_signatures=True, force_update=True)

    def test_delete_validation(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.delete("http://test/api/mirrors/aptly-mirror")
        self.miapi.delete(name="aptly-mirror")

    def test_update_validation(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/mirrors/aptly-mirror")
        self.miapi.update(name="aptly-mirror")

    def test_edit_validation(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/mirrors/aptly-mirror",
                  text='{"Name":"aptly-mirror-bla", "IgnoreSignatures": true}')
        self.miapi.edit(name="aptly-mirror", newname="aptly-mirror-renamed")
