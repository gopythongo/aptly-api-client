# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import NamedTuple, Sequence, Dict, Union, List, cast, Optional
from urllib.parse import quote

from aptly_api.base import BaseAPIClient, AptlyAPIException

PublishEndpoint = NamedTuple('PublishEndpoint', [
    ('storage', str),
    ('prefix', str),
    ('distribution', str),
    ('source_kind', str),
    ('sources', Sequence[Dict[str, str]]),
    ('architectures', Sequence[str]),
    ('label', str),
    ('origin', str),
    ('acquire_by_hash', bool),
])


T_BodyDict = Dict[str, Union[str, bool, Sequence[Dict[str, str]], Sequence[str], Dict[str, Union[bool, str]]]]


class PublishAPISection(BaseAPIClient):
    @staticmethod
    def endpoint_from_response(api_response: Union[Dict[str, str], Dict[str, List[str]],
                                                   Dict[str, List[Dict[str, str]]]]) -> PublishEndpoint:
        return PublishEndpoint(
            storage=cast(str, api_response["Storage"]),
            prefix=cast(str, api_response["Prefix"]),
            distribution=cast(str, api_response["Distribution"]),
            source_kind=cast(str, api_response["SourceKind"]),
            sources=cast(List[Dict[str, str]], api_response["Sources"]),
            architectures=cast(List[str], api_response["Architectures"]),
            label=cast(str, api_response["Label"]),
            origin=cast(str, api_response["Origin"]),
            acquire_by_hash=cast(bool, api_response["AcquireByHash"]),
        )

    @staticmethod
    def escape_prefix(prefix: str) -> str:
        if prefix == ".":
            return ":."
        if "/" in prefix:
            # prefix has not yet been quoted as described at
            # https://www.aptly.info/doc/api/publish/
            if "_" in prefix:
                prefix = prefix.replace("_", "__")
            prefix = prefix.replace("/", "_")
        return prefix

    def list(self) -> Sequence[PublishEndpoint]:
        resp = self.do_get("api/publish")
        ret = []
        for rpe in resp.json():
            ret.append(self.endpoint_from_response(rpe))
        return ret

    def publish(self, *, source_kind: str = "local",
                sources: Sequence[Dict[str, str]],
                architectures: Sequence[str],
                prefix: Optional[str] = None, distribution: Optional[str] = None, label: Optional[str] = None,
                origin: Optional[str] = None, force_overwrite: bool = False,
                sign_skip: bool = False, sign_batch: bool = True, sign_gpgkey: Optional[str] = None,
                sign_keyring: Optional[str] = None, sign_secret_keyring: Optional[str] = None,
                sign_passphrase: Optional[str] = None, sign_passphrase_file: Optional[str] = None,
                acquire_by_hash: Optional[bool] = None) -> PublishEndpoint:
        """
        Example:

        .. code-block:: python
            p.publish(
                sources=[{'Name': 'aptly-repo'}], architectures=['amd64'],
                prefix='s3:myendpoint:test/a_1', distribution='test', sign_batch=True,
                sign_gpgkey='A16BE921', sign_passphrase='*********'
            )
        """
        if sign_passphrase is not None and sign_passphrase_file is not None:
            raise AptlyAPIException("Can't use sign_passphrase and sign_passphrase_file at the same time")

        for source in sources:
            if "name" not in source and "Name" not in source:
                raise AptlyAPIException("Each source in publish() must contain the 'name' attribute")

        url = "api/publish"
        if prefix is not None and prefix != "":
            url = "api/publish/%s" % quote(self.escape_prefix(prefix))

        body = {
            "SourceKind": source_kind,
            "Sources": sources,
        }  # type: T_BodyDict

        if architectures is not None:
            body["Architectures"] = architectures
        if distribution is not None:
            body["Distribution"] = distribution
        if label is not None:
            body["Label"] = label
        if origin is not None:
            body["Origin"] = origin
        if force_overwrite:
            body["ForceOverwrite"] = True
        if acquire_by_hash is not None:
            body["AcquireByHash"] = acquire_by_hash

        sign_dict = {}  # type: Dict[str, Union[bool,str]]
        if sign_skip:
            sign_dict["Skip"] = True
        else:
            sign_dict["Batch"] = sign_batch
            if sign_gpgkey is not None:
                sign_dict["GpgKey"] = sign_gpgkey
            if sign_keyring is not None:
                sign_dict["Keyring"] = sign_keyring
            if sign_secret_keyring is not None:
                sign_dict["SecretKeyring"] = sign_secret_keyring
            if sign_passphrase is not None:
                sign_dict["Passphrase"] = sign_passphrase
            if sign_passphrase_file is not None:
                sign_dict["PassphraseFile"] = sign_passphrase_file
        body["Signing"] = sign_dict

        resp = self.do_post(url, json=body)
        return self.endpoint_from_response(resp.json())

    def update(self, *, prefix: str, distribution: str,
               snapshots: Optional[Sequence[Dict[str, str]]] = None, force_overwrite: bool = False,
               sign_skip: bool = False, sign_batch: bool = True, sign_gpgkey: Optional[str] = None,
               sign_keyring: Optional[str] = None, sign_secret_keyring: Optional[str] = None,
               sign_passphrase: Optional[str] = None, sign_passphrase_file: Optional[str] = None,
               skip_cleanup: Optional[bool] = False) -> PublishEndpoint:
        """
        Example:

        .. code-block:: python
            p.update(
                prefix="s3:maurusnet:nightly/stretch", distribution="mn-nightly",
                sign_batch=True, sign_gpgkey='A16BE921', sign_passphrase='***********'
            )
        """
        if sign_passphrase is not None and sign_passphrase_file is not None:
            raise AptlyAPIException("Can't use sign_passphrase and sign_passphrase_file at the same time")

        body = {}  # type: T_BodyDict

        if snapshots is not None:
            for source in snapshots:
                if "name" not in source and "Name" not in source:
                    raise AptlyAPIException("Each source in update() must contain the 'name' attribute")
            body["Snapshots"] = snapshots

        if force_overwrite:
            body["ForceOverwrite"] = True
        if skip_cleanup:
            body["SkipCleanup"] = True

        sign_dict = {}  # type: Dict[str, Union[bool,str]]
        if sign_skip:
            sign_dict["Skip"] = True
        else:
            sign_dict["Batch"] = sign_batch
            if sign_gpgkey is not None:
                sign_dict["GpgKey"] = sign_gpgkey
            if sign_keyring is not None:
                sign_dict["Keyring"] = sign_keyring
            if sign_secret_keyring is not None:
                sign_dict["SecretKeyring"] = sign_secret_keyring
            if sign_passphrase is not None:
                sign_dict["Passphrase"] = sign_passphrase
            if sign_passphrase_file is not None:
                sign_dict["PassphraseFile"] = sign_passphrase_file
        body["Signing"] = sign_dict

        resp = self.do_put("api/publish/%s/%s" %
                           (quote(self.escape_prefix(prefix)), quote(distribution),), json=body)
        return self.endpoint_from_response(resp.json())

    def drop(self, *, prefix: str, distribution: str, force_delete: bool = False) -> None:
        params = {}
        if force_delete:
            params["force"] = "1"
        self.do_delete("api/publish/%s/%s" %
                       (quote(self.escape_prefix(prefix)), quote(distribution),), params=params)
