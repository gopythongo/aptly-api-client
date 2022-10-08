Python 3 Aptly API client
=========================

.. image:: https://coveralls.io/repos/github/gopythongo/aptly-api-client/badge.svg?branch=master
    :target: https://coveralls.io/github/gopythongo/aptly-api-client?branch=master

.. image:: https://github.com/gopythongo/aptly-api-client/actions/workflows/test.yml/badge.svg
    :target: https://github.com/gopythongo/aptly-api-client/actions/workflows/test.yml

This is a thin abstraction layer for interfacing with
`Aptly's HTTP API <https://www.aptly.info/doc/api/>`__. It's used by
`GoPythonGo <https://github.com/gopythongo/gopythongo/>`__, but can be used as
a standalone library from Pypi.

.. code-block:: shell

    pip install aptly-api-client


Usage
-----

The library provides a direct abstraction of the published Aptly API, mostly
using the same naming, only replacing it with pythonic naming where necessary.
All code has full `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`__
annotations, so if you're using a modern IDE, using this library should be
especially straight-forward.

Where appropriate, the library exposes the interface of the underlying
``requests`` library. This allows you to configure CA pinning, SSL client
certificates, HTTP Basic authentication etc.

.. code-block:: python

    # initialize a client
    from aptly_api import Client
    aptly = Client("http://aptly-endpoint.test/")

    # create a repository
    aptly.repos.create("myrepo", comment="a test repo",
                       default_distribution="mydist",
                       default_component="main")

    # upload a package
    aptly.files.upload("test_folder", "/tmp/mypkg_1.0_amd64.deb")

    # add the package to the repo
    aptly.repos.add_uploaded_file("myrepo", "test_folder")


Contributors
============

* @findmyname666 <findmyname666@users.noreply.github.com>
* Filip Křesťan <fkrestan@users.noreply.github.com>
* @mgusek <mgusek@users.noreply.github.com>
* Samuel Bachmann <samuelba@users.noreply.github.com>


License
=======

Copyright (c) 2016-2019, Jonas Maurus and Contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
