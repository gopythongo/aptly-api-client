# -* encoding: utf-8 *-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import NamedTuple, Sequence, Dict

from aptly_api.base import BaseAPIClient


PublishEndpoint = NamedTuple('PublishEndpoint', [
    ('storage', str),
    ('prefix', str),
    ('distribution', str),
    ('source_kind', str),
    ('sources', Sequence[Dict[str, str]]),
    ('architectures', Sequence[str]),
    ('label', str),
    ('origin', str),
])


class PublishAPISection(BaseAPIClient):
    def list(self, prefix: str=None) -> Sequence[PublishEndpoint]:
        pass

    def publish(self, *, source_kind: str="local",
                sources: Sequence[Dict[str, str]],
                architectures: Sequence[str],
                prefix: str=None, distribution: str=None, label: str=None,
                origin: str=None, force_overwrite: bool=False,
                sign_skip: bool=False, sign_batch: bool=True, sign_gpgkey: str=None,
                sign_keyring: str=None, sign_secret_keyring: str=None,
                sign_passphrase: str=None, sign_passphrase_file: str=None):
        if not sign_skip and not sign_gpgkey:
            raise PublishAPIException("Publish needs a gpgkey to sign with if skip is False")
        pass

    def update(self, *, prefix: str, distribution: str,
               snapshots: Sequence[Dict[str, str]]=None, force_overwrite: bool=False,
               sign_skip: bool=False, sign_batch: bool=True, sign_gpgkey: str=None,
               sign_keyring: str=None, sign_secret_keyring: str=None,
               sign_passphrase: str=None, sign_passphrase_file: str=None) -> PublishEndpoint:
        pass

    def drop(self, *, prefix: str, distribution: str, force_delete: bool=False) -> None:
        pass
