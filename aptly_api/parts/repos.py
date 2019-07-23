# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import NamedTuple, Sequence, Dict, Union, cast, Optional
from urllib.parse import quote

from aptly_api.base import BaseAPIClient, AptlyAPIException
from aptly_api.parts.packages import PackageAPISection, Package

Repo = NamedTuple('Repo', [
    ('name', str),
    ('comment', Optional[str]),
    ('default_distribution', Optional[str]),
    ('default_component', Optional[str])
])

FileReport = NamedTuple('FileReport', [
    ('failed_files', Sequence[str]),
    ('report', Dict[str, Sequence[str]])
])


class ReposAPISection(BaseAPIClient):
    @staticmethod
    def repo_from_response(api_response: Dict[str, str]) -> Repo:
        return Repo(
            name=api_response["Name"],
            default_component=api_response["DefaultComponent"] if "DefaultComponent" in api_response else None,
            default_distribution=api_response["DefaultDistribution"] if "DefaultDistribution" in api_response else None,
            comment=api_response["Comment"] if "Comment" in api_response else None,
        )

    @staticmethod
    def filereport_from_response(api_response: Dict[str, Union[Sequence[str], Dict[str, Sequence[str]]]]) -> FileReport:
        return FileReport(
            failed_files=cast(Sequence[str], api_response["FailedFiles"]),
            report=cast(Dict[str, Sequence[str]], api_response["Report"]),
        )

    def create(self, reponame: str, comment: Optional[str] = None, default_distribution: Optional[str] = None,
               default_component: Optional[str] = None) -> Repo:
        data = {
            "Name": reponame,
        }

        if comment:
            data["Comment"] = comment
        if default_distribution:
            data["DefaultDistribution"] = default_distribution
        if default_component:
            data["DefaultComponent"] = default_component

        resp = self.do_post("api/repos", json=data)

        return self.repo_from_response(resp.json())

    def show(self, reponame: str) -> Repo:
        resp = self.do_get("api/repos/%s" % quote(reponame))
        return self.repo_from_response(resp.json())

    def search_packages(self, reponame: str, query: Optional[str] = None, with_deps: bool = False,
                        detailed: bool = False) -> Sequence[Package]:
        if query is None and with_deps:
            raise AptlyAPIException("search_packages can't include dependencies (with_deps==True) without"
                                    "a query")
        params = {}
        if query:
            params["q"] = query

            if with_deps:
                params["withDeps"] = "1"

        if detailed:
            params["format"] = "details"

        resp = self.do_get("api/repos/%s/packages" % quote(reponame), params=params)
        ret = []
        for rpkg in resp.json():
            ret.append(PackageAPISection.package_from_response(rpkg))
        return ret

    def edit(self, reponame: str, comment: Optional[str] = None, default_distribution: Optional[str] = None,
             default_component: Optional[str] = None) -> Repo:
        if comment is None and default_component is None and default_distribution is None:
            raise AptlyAPIException("edit requires at least one of 'comment', 'default_distribution' or "
                                    "'default_component'.")

        body = {}
        if comment is not None:
            body["Comment"] = comment
        if default_distribution is not None:
            body["DefaultDistribution"] = default_distribution
        if default_component is not None:
            body["DefaultComponent"] = default_component

        resp = self.do_put("api/repos/%s" % quote(reponame), json=body)
        return self.repo_from_response(resp.json())

    def list(self) -> Sequence[Repo]:
        resp = self.do_get("api/repos")

        repos = []
        for rdesc in resp.json():
            repos.append(
                self.repo_from_response(rdesc)
            )
        return repos

    def delete(self, reponame: str, force: bool = False) -> None:
        self.do_delete("api/repos/%s" % quote(reponame), params={"force": "1" if force else "0"})

    def add_uploaded_file(self, reponame: str, dir: str, filename: Optional[str] = None,
                          remove_processed_files: bool = True, force_replace: bool = False) -> FileReport:
        params = {
            "noRemove": "0" if remove_processed_files else "1",
        }
        if force_replace:
            params["forceReplace"] = "1"

        if filename is None:
            resp = self.do_post("api/repos/%s/file/%s" % (quote(reponame), quote(dir),), params=params)
        else:
            resp = self.do_post("api/repos/%s/file/%s/%s" % (quote(reponame), quote(dir), quote(filename),),
                                params=params)

        return self.filereport_from_response(resp.json())

    def add_packages_by_key(self, reponame: str, *package_keys: str) -> Repo:
        resp = self.do_post("api/repos/%s/packages" % quote(reponame), json={
            "PackageRefs": package_keys,
        })
        return self.repo_from_response(resp.json())

    def delete_packages_by_key(self, reponame: str, *package_keys: str) -> Repo:
        resp = self.do_delete("api/repos/%s/packages" % quote(reponame), json={
            "PackageRefs": package_keys,
        })
        return self.repo_from_response(resp.json())
