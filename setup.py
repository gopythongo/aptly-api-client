#!/usr/bin/python
# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
from setuptools import setup, find_packages

_package_root = "."
_root_package = 'aptly_api'
_HERE = os.path.abspath(os.path.dirname(__file__))

with open("aptly_api/__init__.py", "rt", encoding="utf-8") as vf:
    lines = vf.readlines()

_version = "0.0.0+local"
for l in lines:
    m = re.match("version = \"(.*?)\"", l)
    if m:
        _version = m.group(1)

_packages = find_packages(_package_root, exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_requirements = [
    # intentionally unpinned. We're a library, so we don't need to conflict with others by pinning versions
    # and we don't depend on a specific minimum version.
    'typing',
    'requests',
    'iso8601',
    'pytz',
]

try:
    long_description = open(os.path.join(_HERE, 'README.rst')).read()
except IOError:
    long_description = None

setup(
    name='aptly-api-client',
    version=_version,
    packages=_packages,
    package_dir={
        '': _package_root,
    },
    install_requires=_requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
    ],
    author="Jonas Maurus (@jdelic)",
    author_email="jonas@gopythongo.com",
    maintainer="GoPythonGo.com",
    maintainer_email="info@gopythongo.com",
    description="A Python 3 client for the Aptly API",
    long_description=long_description,
)
