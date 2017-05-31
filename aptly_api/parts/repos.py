# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import NamedTuple, Sequence, Dict, Union

from aptly_api.base import AptlyAPIException, BaseAPIClient

Repo = NamedTuple('Repo', [('name', str), ('comment', str), ('default_distribution', str),
                           ('default_component', str)])


class ReposAPIException(AptlyAPIException):
    pass


class ReposAPISection(BaseAPIClient):
    def create(self, reponame: str, comment: str=None, default_distribution: str=None,
               default_component: str=None) -> None:
        pass

    def show(self, reponame: str) -> Repo:
        pass

    def search(self, query: str=None, with_deps: bool=False,
               detailed: bool=False) -> Union[Sequence[str], Sequence[Dict[str, str]]]:
        pass

    def edit(self, reponame: str, comment: str=None, default_distribution: str=None,
             default_component: str=None) -> None:
        pass

    def list(self) -> Sequence[Repo]:
        pass

    def delete(self, reponame: str, force: bool=False) -> None:
        pass

    def add_uploaded_file(self, reponame: str, dir: str, file: str=None, remove_processed_files: bool=False,
                          force_replace: bool=False):
        pass

    def add_packages_by_key(self, reponame: str, *package_keys: str):
        pass

    def delete_packages_by_key(self, reponame: str, *package_keys: str):
        pass
