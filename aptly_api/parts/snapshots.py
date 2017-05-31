# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
from typing import NamedTuple, Sequence, Optional, Union, Dict

from aptly_api.base import AptlyAPIException, BaseAPIClient


class SnapshotAPIException(AptlyAPIException):
    pass


Snapshot = NamedTuple('Snapshot', [('name', str), ('description', str), ('created_at', datetime)])


class SnapshotAPISection(BaseAPIClient):
    def list(self, sort: str='name') -> Sequence[Snapshot]:
        if sort not in ['name', 'time']:
            raise SnapshotAPIException("Snapshot LIST only supports two sort modes: 'name' and 'time'. %s is not "
                                       "supported." % sort)
        return []

    def create_from_repo(self, reponame: str, snapshotname: str, description: str=None) -> Snapshot:
        pass

    def create_from_packages(self, snapshotname: str, description: str=None,
                             source_snapshots: Optional[Sequence[str]]=None,
                             package_refs: Optional[Sequence[str]] = None) -> Snapshot:
        pass

    def update(self, snapshotname: str, newname: str=None, description: str=None) -> Snapshot:
        if newname is None and description is None:
            raise SnapshotAPIException("When updating a Snapshot you must at lease provide either a new name or a "
                                       "new description.")
        pass

    def show(self, snapshotname: str) -> Snapshot:
        pass

    def list_packages(self, snapshotname: str, query: str=None, with_deps: bool=False,
                      detailed: bool=False) -> Union[Sequence[str], Sequence[Dict[str, str]]]:
        pass

    def delete(self, snapshotname: str, force: bool=False) -> None:
        pass

    def diff(self, snapshot1: str, snapshot2: str) -> Sequence[Dict[str, str]]:
        pass
