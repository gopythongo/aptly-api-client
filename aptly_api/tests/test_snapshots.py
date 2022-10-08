# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any
from unittest.case import TestCase

import iso8601
import pytz
import requests_mock

from aptly_api.base import AptlyAPIException
from aptly_api.parts.packages import Package
from aptly_api.parts.snapshots import SnapshotAPISection, Snapshot


@requests_mock.Mocker(kw='rmock')
class SnapshotAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.sapi = SnapshotAPISection("http://test/")
        self.maxDiff = None

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/snapshots",
                  text='[{"Name":"stretch-security-1","CreatedAt":"2017-06-03T21:36:22.2692213Z",'
                       '"Description":"Snapshot from mirror [stretch-security]: '
                       'http://security.debian.org/debian-security/ stretch/updates"},'
                       '{"Name":"stretch-updates-1","CreatedAt":"2017-06-03T21:36:22.431767659Z",'
                       '"Description":"Snapshot from mirror [stretch-updates]: '
                       'http://ftp-stud.hs-esslingen.de/debian/ stretch-updates"}]')
        self.assertSequenceEqual(
            self.sapi.list(),
            [
                Snapshot(
                    name='stretch-security-1',
                    description='Snapshot from mirror [stretch-security]: http://security.debian.org/debian-security/ '
                                'stretch/updates',
                    created_at=iso8601.parse_date('2017-06-03T21:36:22.2692213Z')
                ),
                Snapshot(
                    name='stretch-updates-1',
                    description='Snapshot from mirror [stretch-updates]: http://ftp-stud.hs-esslingen.de/debian/ '
                                'stretch-updates',
                    created_at=iso8601.parse_date('2017-06-03T21:36:22.431767659Z')
                )
            ]
        )

    def test_list_invalid(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.sapi.list("snoepsort")

    def test_update_noparams(self, *, rmock: requests_mock.Mocker) -> None:
        with self.assertRaises(AptlyAPIException):
            self.sapi.update("test")

    def test_create(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/repos/aptly-repo/snapshots",
                   text='{"Name":"aptly-repo-1","CreatedAt":"2017-06-03T23:43:40.275605639Z",'
                        '"Description":"Snapshot from local repo [aptly-repo]"}')
        self.assertEqual(
            self.sapi.create_from_repo("aptly-repo", "aptly-repo-1",
                                       description='Snapshot from local repo [aptly-repo]'),
            Snapshot(
                name='aptly-repo-1',
                description='Snapshot from local repo [aptly-repo]',
                created_at=iso8601.parse_date('2017-06-03T23:43:40.275605639Z', default_timezone=pytz.UTC)
            )
        )

    def test_list_packages(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/snapshots/aptly-repo-1/packages",
                  text='["Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1 5f70af798690300d"]')
        self.assertEqual(
            self.sapi.list_packages("aptly-repo-1"),
            [
                Package(
                    key='Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1 5f70af798690300d',
                    short_key=None,
                    files_hash=None,
                    fields=None
                ),
            ]
        )

    def test_list_packages_details(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/snapshots/aptly-repo-1/packages",
                  text='[{"Architecture":"all","Depends":"postgresql-9.6-postgis-2.3-scripts",'
                       '"Description":" transitional dummy package\\n This is a transitional dummy package. '
                       'It can safely be removed.\\n",'
                       '"Filename":"postgresql-9.6-postgis-scripts_2.3.2+dfsg-1~exp2.pgdg90+1_all.deb",'
                       '"FilesHash":"5f70af798690300d",'
                       '"Homepage":"http://postgis.net/",'
                       '"Installed-Size":"491",'
                       '"Key":"Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1 5f70af798690300d",'
                       '"MD5sum":"56de7bac497e4ac34017f4d11e75fffb",'
                       '"Maintainer":"Debian GIS Project \u003cpkg-grass-devel@lists.alioth.debian.org\u003e",'
                       '"Package":"postgresql-9.6-postgis-scripts",'
                       '"Priority":"extra",'
                       '"SHA1":"61bb9250e7a35be9b78808944e8cfbae1e70f67d",'
                       '"SHA256":"01c0c4645e9100f7ddb6d05a9d36ad3866ac8d2e412b7c04163a9e65397ce05e",'
                       '"Section":"oldlibs",'
                       '"ShortKey":"Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1",'
                       '"Size":"468824","Source":"postgis","Version":"2.3.2+dfsg-1~exp2.pgdg90+1"}]')
        parsed = self.sapi.list_packages("aptly-repo-1", query="Name (% postgresql-9.6.-postgis-sc*)", detailed=True,
                                         with_deps=True)[0]
        expected = Package(
            key='Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1 5f70af798690300d',
            short_key='Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1',
            files_hash='5f70af798690300d',
            fields={
                'Maintainer': 'Debian GIS Project <pkg-grass-devel@lists.alioth.debian.org>',
                'Size': '468824',
                'MD5sum': '56de7bac497e4ac34017f4d11e75fffb',
                'ShortKey': 'Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1',
                'FilesHash': '5f70af798690300d',
                'Filename': 'postgresql-9.6-postgis-scripts_2.3.2+dfsg-1~exp2.pgdg90+1_all.deb',
                'Section': 'oldlibs',
                'Homepage': 'http://postgis.net/',
                'Description': ' transitional dummy package\n This is a transitional dummy package. '
                               'It can safely be removed.\n',
                'Architecture': 'all',
                'Priority': 'extra',
                'Source': 'postgis',
                'SHA1': '61bb9250e7a35be9b78808944e8cfbae1e70f67d',
                'Installed-Size': '491',
                'Version': '2.3.2+dfsg-1~exp2.pgdg90+1',
                'Depends': 'postgresql-9.6-postgis-2.3-scripts',
                'Key': 'Pall postgresql-9.6-postgis-scripts 2.3.2+dfsg-1~exp2.pgdg90+1 5f70af798690300d',
                'SHA256': '01c0c4645e9100f7ddb6d05a9d36ad3866ac8d2e412b7c04163a9e65397ce05e',
                'Package': 'postgresql-9.6-postgis-scripts'
            }
        )

        # mypy should detect this as ensuring that parsed.fields is not None, but it doesn't
        self.assertIsNotNone(parsed.fields)
        self.assertIsNotNone(expected.fields)

        self.assertDictEqual(
            parsed.fields if parsed.fields else {},  # make sure that mypy doesn't error on this being potentially None
            expected.fields if expected.fields else {},  # this can't happen unless Package.__init__ is fubared
        )

    def test_show(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/snapshots/aptly-repo-1",
                  text='{"Name":"aptly-repo-1",'
                       '"CreatedAt":"2017-06-03T23:43:40.275605639Z",'
                       '"Description":"Snapshot from local repo [aptly-repo]"}')
        self.assertEqual(
            self.sapi.show("aptly-repo-1"),
            Snapshot(
                name='aptly-repo-1',
                description='Snapshot from local repo [aptly-repo]',
                created_at=iso8601.parse_date('2017-06-03T23:43:40.275605639Z', default_timezone=pytz.UTC)
            )
        )

    def test_update(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.put("http://test/api/snapshots/aptly-repo-1",
                  text='{"Name":"aptly-repo-2","CreatedAt":"2017-06-03T23:43:40.275605639Z",'
                       '"Description":"test"}')
        self.assertEqual(
            self.sapi.update("aptly-repo-1", newname="aptly-repo-2", newdescription="test"),
            Snapshot(
                name='aptly-repo-2',
                description='test',
                created_at=iso8601.parse_date('2017-06-03T23:43:40.275605639Z', default_timezone=pytz.UTC)
            )
        )

    def test_delete(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.delete("http://test/api/snapshots/aptly-repo-1",
                     text='{}')
        self.sapi.delete("aptly-repo-1", force=True)

    def test_diff(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/snapshots/aptly-repo-1/diff/aptly-repo-2",
                  text='[{"Left":null,"Right":"Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9"},'
                       '{"Left":"Pamd64 radicale 1.1.1 fbc974fa526f14e9","Right":null}]')
        self.assertSequenceEqual(
            self.sapi.diff("aptly-repo-1", "aptly-repo-2"),
            [
                {'Left': None, 'Right': 'Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9'},
                {'Left': 'Pamd64 radicale 1.1.1 fbc974fa526f14e9', 'Right': None}
            ]
        )

    def test_create_from_packages(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/snapshots",
                   text='{"Name":"aptly-repo-2","CreatedAt":"2017-06-07T14:19:07.706408213Z","Description":"test"}')
        self.assertEqual(
            self.sapi.create_from_packages(
                "aptly-repo-2",
                description="test",
                package_refs=["Pamd64 dirmngr 2.1.18-6 4c7412c5f0d7b30a"],
                source_snapshots=["aptly-repo-1"]
            ),
            Snapshot(
                name='aptly-repo-2',
                description='test',
                created_at=iso8601.parse_date('2017-06-07T14:19:07.706408213Z', default_timezone=pytz.UTC)
            )
        )
