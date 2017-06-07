# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any
from unittest.case import TestCase

import requests_mock

from aptly_api.parts.packages import PackageAPISection, Package


@requests_mock.Mocker(kw='rmock')
class PackageAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.papi = PackageAPISection("http://test/")

    def test_show(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get(
            "http://test/api/packages/Pamd64%20authserver%200.1.14~dev0-1%201cc572a93625a9c9",
            text="""{"Architecture":"amd64",
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
                 "SHA512":"01f9ca888014599374bf7a2c8c46f895d7ef0dfea99dfd092007f9fc5d5fe57a2755b843eda296b65"""
                 """cb6ac0f64b9bd88b507221a71825f5329fdda0e58728cd7",
                 "Section":"default",
                 "ShortKey":"Pamd64 authserver 0.1.14~dev0-1",
                 "Size":"26623042",
                 "Vendor":"root@test",
                 "Version":"0.1.14~dev0-1"}"""
        )
        pkg = self.papi.show("Pamd64 authserver 0.1.14~dev0-1 1cc572a93625a9c9")
        self.assertEqual(
            pkg,
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
                    'SHA512': '01f9ca888014599374bf7a2c8c46f895d7ef0dfea99dfd092007f9fc5d5fe57a2755b843eda296b65cb6ac'
                              '0f64b9bd88b507221a71825f5329fdda0e58728cd7',
                    'Section': 'default',
                    'ShortKey': 'Pamd64 authserver 0.1.14~dev0-1',
                    'Size': '26623042',
                    'Vendor': 'root@test',
                    'Version': '0.1.14~dev0-1'
                }
            )
        )
