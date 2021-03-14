# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# explicit exports for mypy
from aptly_api.client import Client as Client
from aptly_api.base import AptlyAPIException as AptlyAPIException
from aptly_api.parts.packages import Package as Package
from aptly_api.parts.publish import PublishEndpoint as PublishEndpoint
from aptly_api.parts.repos import Repo as Repo, FileReport as FileReport
from aptly_api.parts.snapshots import Snapshot as Snapshot

version = "0.2.3"


__all__ = ['Client', 'AptlyAPIException', 'version', 'Package', 'PublishEndpoint', 'Repo', 'FileReport',
           'Snapshot']
