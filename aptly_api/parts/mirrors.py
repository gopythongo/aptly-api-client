# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import NamedTuple, Sequence, Dict, cast, Optional, List, Union
from urllib.parse import quote

from aptly_api.base import BaseAPIClient
from aptly_api.parts.packages import Package, PackageAPISection


Mirror = NamedTuple('Mirror', [
    ('uuid', Optional[str]),
    ('name', str),
    ('archiveurl', str),
    ('distribution', Optional[str]),
    ('components', Optional[Sequence[str]]),
    ('architectures', Optional[Sequence[str]]),
    ('meta', Optional[Sequence[Dict[str, str]]]),
    ('downloaddate', Optional[str]),
    ('filter', Optional[str]),
    ('status', Optional[int]),
    ('worker_pid', Optional[int]),
    ('filter_with_deps', bool),
    ('skip_component_check', bool),
    ('skip_architecture_check', bool),
    ('download_sources', bool),
    ('download_udebs', bool),
    ('download_installer', bool)
])

T_BodyDict = Dict[str, Union[str, bool, Sequence[Dict[str, str]],
                             Sequence[str], Dict[str, Union[bool, str]]]]


class MirrorsAPISection(BaseAPIClient):
    @staticmethod
    def mirror_from_response(api_response: Dict[str, str]) -> Mirror:
        return Mirror(
            uuid=cast(str, api_response["UUID"]) if "UUID" in api_response else None,
            name=cast(str, api_response["Name"]),
            archiveurl=cast(str, api_response["ArchiveRoot"]),
            distribution=cast(str, api_response["Distribution"]) if "Distribution" in api_response else None,
            components=cast(List[str], api_response["Components"]) if "Components" in api_response else None,
            architectures=cast(List[str], api_response["Architectures"]) if "Architectures" in api_response else None,
            meta=cast(List[Dict[str, str]], api_response["Meta"]) if "Meta" in api_response else None,
            downloaddate=cast(str, api_response["LastDownloadDate"]) if "LastDownloadDate" in api_response else None,
            filter=cast(str, api_response["Filter"]) if "Filter" in api_response else None,
            status=cast(int, api_response["Status"]) if "Status" in api_response else None,
            worker_pid=cast(int, api_response["WorkerPID"]) if "WorkerPID" in api_response else None,
            filter_with_deps=cast(bool, api_response["FilterWithDeps"]) if "FilterWithDeps" in api_response else False,
            skip_component_check=cast(bool, api_response["SkipComponentCheck"]
                                      ) if "SkipComponentCheck" in api_response else False,
            skip_architecture_check=cast(bool, api_response["SkipArchitectureCheck"]
                                         ) if "SkipArchitectureCheck" in api_response else False,
            download_sources=cast(bool, api_response["DownloadSources"]
                                  ) if "DownloadSources" in api_response else False,
            download_udebs=cast(bool, api_response["DownloadUdebs"]
                                ) if "DownloadUdebs" in api_response else False,
            download_installer=cast(bool, api_response["DownloadInstaller"]
                                    ) if "DownloadInstaller" in api_response else False,
        )

    def list(self) -> Sequence[Mirror]:
        resp = self.do_get("api/mirrors")

        mirrors = []
        for mirr in resp.json():
            mirrors.append(self.mirror_from_response(mirr))
        return mirrors

    def update(self, name: str, ignore_signatures: bool = False) -> None:
        body = {}
        if ignore_signatures:
            body["IgnoreSignatures"] = ignore_signatures
        self.do_put("api/mirrors/%s" % (quote(name)), json=body)

    def edit(self, name: str, newname: Optional[str] = None, archiveurl: Optional[str] = None,
             filter: Optional[str] = None, architectures: Optional[List[str]] = None,
             components: Optional[List[str]] = None, keyrings: Optional[List[str]] = None,
             filter_with_deps: bool = False, skip_existing_packages: bool = False,
             download_sources: bool = False, download_udebs: bool = False,
             skip_component_check: bool = False, ignore_checksums: bool = False,
             ignore_signatures: bool = False, force_update: bool = False) -> None:

        body = {}  # type: T_BodyDict
        if newname:
            body["Name"] = newname
        if archiveurl:
            body["ArchiveURL"] = archiveurl
        if filter:
            body["Filter"] = filter
        if architectures:
            body["Architectures"] = architectures
        if components:
            body["Components"] = components
        if keyrings:
            body["Keyrings"] = keyrings
        if filter_with_deps:
            body["FilterWithDeps"] = filter_with_deps
        if download_sources:
            body["DownloadSources"] = download_sources
        if download_udebs:
            body["DownloadUdebs"] = download_udebs
        if skip_component_check:
            body["SkipComponentCheck"] = skip_component_check
        if ignore_checksums:
            body["IgnoreChecksums"] = ignore_checksums
        if ignore_signatures:
            body["IgnoreSignatures"] = ignore_signatures
        if skip_existing_packages:
            body["SkipExistingPackages"] = skip_existing_packages
        if force_update:
            body["ForceUpdate"] = force_update

        self.do_put("api/mirrors/%s" % (quote(name)), json=body)

    def show(self, name: str) -> Mirror:
        resp = self.do_get("api/mirrors/%s" % (quote(name)))
        return self.mirror_from_response(resp.json())

    def list_packages(self, name: str, query: Optional[str] = None, with_deps: bool = False,
                      detailed: bool = False) -> Sequence[Package]:
        params = {}
        if query is not None:
            params["q"] = query
        if with_deps:
            params["withDeps"] = "1"
        if detailed:
            params["format"] = "details"

        resp = self.do_get("api/mirrors/%s/packages" %
                           quote(name), params=params)
        ret = []
        for rpkg in resp.json():
            ret.append(PackageAPISection.package_from_response(rpkg))
        return ret

    def delete(self, name: str) -> None:
        self.do_delete("api/mirrors/%s" % quote(name))

    def create(self, name: str, archiveurl: str, distribution: Optional[str] = None,
               filter: Optional[str] = None, components: Optional[List[str]] = None,
               architectures: Optional[List[str]] = None, keyrings: Optional[List[str]] = None,
               download_sources: bool = False, download_udebs: bool = False,
               download_installer: bool = False, filter_with_deps: bool = False,
               skip_component_check: bool = False, skip_architecture_check: bool = False,
               ignore_signatures: bool = False) -> Mirror:
        data = {
            "Name": name,
            "ArchiveURL": archiveurl
        }  # type: T_BodyDict

        if distribution:
            data["Distribution"] = distribution
        if filter:
            data["Filter"] = filter
        if components:
            data["Components"] = components
        if architectures:
            data["Architectures"] = architectures
        if keyrings:
            data["Keyrings"] = keyrings
        if download_sources:
            data["DownloadSources"] = download_sources
        if download_udebs:
            data["DownloadUdebs"] = download_udebs
        if download_installer:
            data["DownloadInstaller"] = download_installer
        if filter_with_deps:
            data["FilterWithDeps"] = filter_with_deps
        if skip_component_check:
            data["SkipComponentCheck"] = skip_component_check
        if skip_architecture_check:
            data["SkipArchitectureCheck"] = skip_architecture_check
        if ignore_signatures:
            data["IgnoreSignatures"] = ignore_signatures

        resp = self.do_post("api/mirrors", json=data)

        return self.mirror_from_response(resp.json())
