# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import NamedTuple, Sequence, Dict, Union

from aptly_api.base import BaseAPIClient

Repo = NamedTuple('Repo', [('name', str), ('comment', str), ('default_distribution', str),
                           ('default_component', str)])


class ReposAPISection(BaseAPIClient):
    def _repo_from_response(self, api_response: Dict[str, str]):
        return Repo(
            name=api_response["Name"],
            default_component=api_response["DefaultComponent"],
            default_distribution=api_response["DefaultDistribution"],
            comment=api_response["Comment"],
        )

    def create(self, reponame: str, comment: str=None, default_distribution: str=None,
               default_component: str=None) -> Repo:
        data = {
            "Name": reponame,
        }

        if comment:
            data["Comment"] = comment
        if default_distribution:
            data["DefaultDistribution"] = default_distribution
        if default_component:
            data["DefaultComponent"] = default_component

        resp = self.do_post("/api/repos", json=data)

        return self._repo_from_response(resp.json())

    def show(self, reponame: str) -> Repo:
        resp = self.do_get("/api/repos/%s" % reponame)

    def search(self, query: str=None, with_deps: bool=False,
               detailed: bool=False) -> Union[Sequence[str], Sequence[Dict[str, str]]]:
        pass

    def edit(self, reponame: str, comment: str=None, default_distribution: str=None,
             default_component: str=None) -> None:
        pass

    def list(self) -> Sequence[Repo]:
        resp = self.do_get("/api/repos")

        repos = []
        for rdesc in resp.json():
            repos.append(
                self._repo_from_response(rdesc)
            )
        return repos

    def delete(self, reponame: str, force: bool=False) -> None:
        pass

    def add_uploaded_file(self, reponame: str, dir: str, file: str=None, remove_processed_files: bool=False,
                          force_replace: bool=False):
        pass

    def add_packages_by_key(self, reponame: str, *package_keys: str):
        pass

    def delete_packages_by_key(self, reponame: str, *package_keys: str):
        pass
