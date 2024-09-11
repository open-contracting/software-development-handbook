Continuous integration
======================

.. seealso::

   Workflows for:

   -  Linting :doc:`Python<linting>`, :ref:`JavaScript<javascript-ci>` and :ref:`shell scripts<shell-ci>`
   - :ref:`Releasing packages<python-package-release-process>`
   - :ref:`Checking translations<i18n-ci>`
   - :ref:`Checking accessibility<a11y-ci>`

.. tip::

   If a workflow has:

   .. code-block:: yaml

      on:
        schedule:
          - cron: "..."

   Add a ``workflow_dispatch`` event, to be able to test the workflow by triggering it manually:

   .. code-block:: yaml
      :emphasize-lines: 2

      on:
        workflow_dispatch:
        schedule:
          - cron: "..."

Automated tests
---------------

Create a ``.github/workflows/ci.yml`` file, and use or adapt one of the :ref:`templates<python-ci-templates>` below.

-  Workflows should have a single responsibility: running tests, linting Python, checking translations, deploying, etc. To connect workflows, read `Events that trigger workflows <https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows>`__ and `Running a workflow based on the conclusion of another workflow <https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#running-a-workflow-based-on-the-conclusion-of-another-workflow>`__, in particular.
-  If the project is only used with a specific version of the OS or Python, set ``runs-on:`` and ``python-version:`` appropriately.
-  If a ``run:`` step uses an ``env:`` key, put ``env:`` before ``run:``, so that the reader is more likely to see the command with its environment.
-  If a ``run:`` step is a single line, omit the ``name:`` key.
-  Put commands that form logical units in the same ``run:`` step. For example:

   .. code-block:: yaml

      - name: Install gettext
        run: |
          sudo apt update
          sudo apt install gettext

   Not:

   .. code-block:: yaml

      - run: sudo apt update # WRONG
      - run: sudo apt install gettext # WRONG

Reference: `Customizing GitHub-hosted runners <https://docs.github.com/en/actions/using-github-hosted-runners/customizing-github-hosted-runners>`__

Python warnings
~~~~~~~~~~~~~~~

The step that runs tests should either the ``-W`` option or the ``PYTHONWARNINGS`` environment variable to ``error``.

.. tip::

   The Python documentation describes `warning filter specifications <https://docs.python.org/3/library/warnings.html#the-warnings-filter>`__ as using regular expressions. However, this is only true when using the ``warnings`` module. If set using ``-W`` or ``PYTHONWARNINGS``, the message and module parts are escaped using ``re.escape``, and the module part is suffixed with a ``\Z`` anchor.

..
   warnoptions is created in https://github.com/python/cpython/blob/3.10/Python/initconfig.c and processed in https://github.com/python/cpython/blob/3.10/Lib/warnings.py

Code coverage
~~~~~~~~~~~~~

All the :ref:`templates<python-ci-templates>` below use Coveralls, :ref:`as preferred<devops>`.

.. _service-containers:

Service containers
~~~~~~~~~~~~~~~~~~

If the workflow requires `service containers <https://docs.github.com/en/actions/using-containerized-services/about-service-containers>`__, add the ``services:`` key after the ``steps:`` key, so that files are easier to compare visually.

.. note::

   Service containers are `only available on Ubuntu runners <https://docs.github.com/en/actions/using-containerized-services/about-service-containers#about-service-containers>`__.

Mock APIs
^^^^^^^^^

Use the `mccutchen/go-httpbin image <https://hub.docker.com/r/mccutchen/go-httpbin>`__ to mock APIs. For example:

.. code-block:: yaml

       steps:
         # ...
         - env:
             TEST_URL: http://localhost:${{ job.services.httpbin.ports[8080] }}
           run: coverage run --source=MODULENAME -m pytest -W error
       services:
         httpbin:
           image: mccutchen/go-httpbin:latest
           ports:
             - 8080/tcp

.. code-block:: python

   import requests

   TEST_URL = os.getenv("TEST_URL", "http://httpbingo.org")


   def test_200():
       assert requests.get(f"{TEST_URL}/status/200").status_code == 200

.. note::

   Services to mock APIs include `httpbin <https://httpbingo.org>`__, `RequestBin <https://requestbin.com/docs/>`__, `Postman Echo <https://learning.postman.com/docs/developer/echo-api/>`__, `PostBin <https://www.toptal.com/developers/postbin/>`__, etc.

PostgreSQL
^^^^^^^^^^

Set the image tag to the version used in production.

.. code-block:: yaml

       services:
         postgres:
           image: postgres:15
           env:
             POSTGRES_PASSWORD: postgres
           options: >-
             --health-cmd pg_isready
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 5432/tcp

This connection string can be used in ``psql`` commands or in environment variables to setup the database or configure the application:

.. code-block:: none

   postgresql://postgres:postgres@localhost:${{ job.services.postgres.ports[5432] }}/postgres

.. tip::

   If you are running out of connections, use the ``cyberboss/postgres-max-connections`` image, which is a `fork <https://github.com/tgstation/tgstation-server/blob/a64be6d9819b8923231ffbe54e37f5d92ebd0f17/.github/workflows/ci-suite.yml#L271>`__ of ``postgres:latest`` with ``max_connections=500``.

Reference: `Creating PostgreSQL service containers <https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers>`__

RabbitMQ
^^^^^^^^

.. code-block:: yaml

       services:
         rabbitmq:
           image: rabbitmq:latest
           options: >-
             --health-cmd "rabbitmqctl node_health_check"
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 5672/tcp

This connection string can be used:

.. code-block:: none

   amqp://127.0.0.1:${{ job.services.rabbitmq.ports[5672] }}

Elasticsearch
^^^^^^^^^^^^^

Set the image tag to the version used in production.

.. code-block:: yaml

       services:
         elasticsearch:
           image: docker.elastic.co/elasticsearch/elasticsearch:7.10.0
           env:
             discovery.type: single-node
           options: >-
             --health-cmd "curl localhost:9200/_cluster/health"
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 9200/tcp

.. _python-ci-templates:

Templates
~~~~~~~~~

Applications
^^^^^^^^^^^^

Set the Ubuntu version and Python version to those used in production.

If using :doc:`django`, use this template, replacing ``core`` if needed and adding app directories as comma-separated values after ``--source``:

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.github/workflows/ci.yml
   :language: yaml

.. note::

   Remember to add ``__init__.py`` files to the ``management`` and ``management/commands`` directories within app directories. Otherwise, their coverage won't be calculated.

Otherwise, use this template, replacing ``APPNAME1``:

.. literalinclude:: samples/ci/app.yml
   :language: yaml

Packages
^^^^^^^^

If using `tox <https://tox.wiki/en/latest/>`__:

.. literalinclude:: samples/ci/package-tox.yml
   :language: yaml

.. note::

   Do not use ``tox`` to test multiple Python versions. Use the `matrix <https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix>`__ in GitHub Actions, instead. This makes it easier to install version-specific dependencies (like ``libxml2-dev`` for PyPy), and it makes exclusions more visible (like pypy-3.10 on Windows).

If not using ``tox``, use this template, replacing ``{{ cookiecutter.package_name }}`` and removing the Jinja syntax if not using the :doc:`Cookiecutter template<packages>`:

.. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.github/workflows/ci.yml
   :language: yaml+jinja

Test :doc:`packages<packages>` on Python versions that aren't end-of-life, and on the latest version of PyPy. Test on Ubuntu, macOS and Windows (though :ref:`only Ubuntu<service-containers>` if a service container is needed).

If the package has optional support for `orjson <https://pypi.org/project/orjson/>`__, to test on PyPy, replace the ``pytest`` step with the following steps, replacing ``PACKAGENAME``:

.. code-block:: yaml

         # "orjson does not support PyPy" and fails to install. https://pypi.org/project/orjson/
         - if: matrix.python-version != 'pypy-3.10'
           name: Test
           shell: bash
           run: |
             coverage run --source=PACKAGENAME --append -m pytest
             pip install orjson
             coverage run --source=PACKAGENAME --append -m pytest
             pip uninstall -y orjson
         - if: matrix.python-version == 'pypy-3.10'
           name: Test
           run: coverage run --source=PACKAGENAME -m pytest

Static files
^^^^^^^^^^^^

For example, the `Extension Registry <https://github.com/open-contracting/extension_registry>`__ mainly contains static files. Tests are used to validate the files.

.. literalinclude:: samples/ci/static.yml
   :language: yaml

Dependabot
----------

Keep GitHub Actions up-to-date with:

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.github/dependabot.yml
   :language: yaml
   :caption: .github/dependabot.yml

Reference: `Configuration options for dependency updates <https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file>`__

Maintenance
-----------

.. seealso::

   -  :ref:`JavaScript CI maintenance<javascript-ci>`
   -  :ref:`Shell scripts CI maintenance<shell-ci>`

Find unexpected workflows:

.. code-block:: bash

   find . -path '*/workflows/*' ! -name automerge.yml ! -name ci.yml ! -name lint.yml ! -name mypy.yml ! -name js.yml ! -name shell.yml ! -name spellcheck.yml ! -name i18n.yml ! -name pypi.yml ! -name docker.yml ! -path '*/node_modules/*' ! -path '*/vendor/*'

Find ``ci.yml`` files without ``lint.yml`` files, and vice versa:

.. code-block:: bash

   find . \( -name lint.yml \) -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name ci.yml) ]]; then echo {}; fi' \;
   find . \( -name ci.yml \) ! -path '*/node_modules/*' -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name lint.yml) ]]; then echo {}; fi' \;

Find and compare ``lint.yml`` files:

.. code-block:: bash

   find . -name lint.yml -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "9773a893d136df0dc82deddedd8af8563969c04a 9222eac95ab63f3c2d983ba3cf4629caea53a72e fc3eff616a7e72f41c96e48214d244c9058dbc83 953ef7f0815d49226fd2d05db8df516fff2e3fdb dfe1c0d1fbdb18bb1e2b3bcfb1f0c10fe6b06bc4" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

Find and compare ``pypi.yml`` files:

.. code-block:: bash

   find . -name pypi.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Find repositories for Python packages but without ``pypi.yml`` files:

.. code-block:: bash

   find . -name setup.cfg ! -path '*/node_modules/*' -exec bash -c 'if grep long_description {} > /dev/null && [[ -z $(find $(echo {} | cut -d/ -f2) -name pypi.yml) ]]; then echo {}; fi' \;

Find and compare ``i18n.yml`` files:

.. code-block:: bash

   find . -name i18n.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Find repositories with ``LC_MESSAGES`` directories but without ``i18n.yml`` files:

.. code-block:: bash

   find . -name LC_MESSAGES ! -path '*/en/*' -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name i18n.yml) ]]; then echo {}; fi' \;

Reference
---------

The following prevents GitHub Actions from running a workflow twice when pushing to the branch of a pull request:

.. code-block:: yaml

   if: github.event_name == 'push' || github.event.pull_request.head.repo.full_name != github.repository

.. note::

   A common configuration for GitHub Actions is:

   .. code-block:: yaml

      on:
        push:
          branches: [main, master]
        pull_request:
          branches: [main, master]

   However, this means the workflow won't run for a push to a non-PR branch. Some developers only open a PR when ready for review, rather than as soon as they push the branch. In such cases, it's important for the developer to receive feedback from the workflow.

   This also means the workflow won't run for a pull request whose base branch isn't a default branch. Sometimes, we create PRs on non-default branches, like when doing a rewrite, like the ``django`` branch of Kingfisher Process.

   To correct for both scenarios, we use ``on: [push, pull_request]``, and then use the above condition to avoid duplicate runs.

   Note that, in standards repositories, we have many protected branches (like ``1.0`` and ``1.0-dev``) that are not "main" or "master". The above setup avoids accidentally excluding relevant branches.
