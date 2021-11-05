Continous integration
=====================

.. seealso::

   Workflows for linting :doc:`Python<linting>`, :ref:`JavaScript<javascript-ci>` and :ref:`shell scripts<shell-ci>`, for :ref:`releasing packages<python-package-release-process>` and for :ref:`internationalization<i18n-ci>`

Automated tests
---------------

Create a ``.github/workflows/ci.yml`` file, and use one of the base templates below.

-  If the project is only used with a specific version of the OS or Python, set ``runs-on:`` and ``python-version:`` appropriately.
-  If a ``run:`` step is a single line, omit the ``name:`` key.
-  If a ``run:`` step uses an ``env:`` key, put ``env:`` before ``run:``, so that the reader is more likely to see the command with its environment.
-  Put commands that form logical units in the same ``run:`` step. For example:

   .. code-block:: yaml

      - name: Install gettext
        run: |
          sudo apt update
          sudo apt install gettext

   .. code-block:: yaml

      - run: sudo apt update # WRONG
      - run: sudo apt install gettext # WRONG

Reference:

-  `Customizing GitHub-hosted runners <https://docs.github.com/en/actions/using-github-hosted-runners/customizing-github-hosted-runners>`__
-  `Events that trigger workflows <https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows>`__

Service containers
~~~~~~~~~~~~~~~~~~

If the workflow requires `service containers <https://docs.github.com/en/actions/using-containerized-services/about-service-containers>`__, add the ``services:`` key after the ``steps:`` key, so that files are easier to compare visually.

.. note::

   Service containers are `only available on Ubuntu runners <https://docs.github.com/en/actions/using-containerized-services/about-service-containers#about-service-containers>`__.

PostgreSQL
^^^^^^^^^^

Set the image tag to the version used in production.

``postgresql://postgres:postgres@localhost:${{ job.services.postgres.ports[5432] }}/postgres`` can be used in ``psql`` commands or in environment variables to setup the database or configure the application.

.. code-block:: yaml

         postgres:
           image: postgres:13
           env:
             POSTGRES_PASSWORD: postgres
           options: >-
             --health-cmd pg_isready
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 5432/tcp

.. tip::

   If you are running out of connections, use the ``cyberboss/postgres-max-connections`` image, which is a `fork <https://github.com/tgstation/tgstation-server/blob/a64be6d9819b8923231ffbe54e37f5d92ebd0f17/.github/workflows/ci-suite.yml#L271>`__ of ``postgres:latest`` with ``max_connections=500``.

RabbitMQ
^^^^^^^^

.. code-block:: yaml

         rabbitmq:
           image: rabbitmq:latest
           options: >-
             --health-cmd "rabbitmqctl node_health_check"
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5
           ports:
             - 5672/tcp

Elasticsearch
^^^^^^^^^^^^^

Set the image tag to the version used in production.

.. code-block:: yaml

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

Applications
~~~~~~~~~~~~

Set the Ubuntu version and Python version to those used in production.

.. literalinclude:: samples/ci-app.yml
   :language: yaml

Packages
~~~~~~~~

If using `tox <http://tox.readthedocs.org>`__:

.. literalinclude:: samples/ci-package-tox.yml
   :language: yaml

Otherwise, replacing ``PACKAGENAME``:

.. literalinclude:: samples/ci-package.yml
   :language: yaml

:doc:`packages` should be tested on Python versions that aren't end-of-life, and on the latest version of PyPy. They should be tested on Ubuntu, macOS and Windows, unless service containers are needed, in which case an Ubuntu runner is required.

If the package has optional support for `orjson <https://pypi.org/project/orjson/>`__, to test on PyPy, replace the ``pytest`` step with the following steps, replacing ``PACKAGENAME``: 

.. code-block:: yaml

         # "orjson does not support PyPy" and fails to install. https://pypi.org/project/orjson/
         - if: matrix.python-version != 'pypy-3.7'
           name: Test
           run: |
             coverage run --append --source=PACKAGENAME -m pytest
             pip install orjson
             coverage run --append --source=PACKAGENAME -m pytest
             pip uninstall -y orjson
         - if: matrix.python-version == 'pypy-3.7'
           name: Test
           run: pytest --cov PACKAGENAME

Reference: `Using pip to get cache location <https://github.com/actions/cache/blob/main/examples.md#using-pip-to-get-cache-location>`__

Static files
~~~~~~~~~~~~

For example, the `Extension Registry <https://github.com/open-contracting/extension_registry>`__ mainly contains static files. Tests are used to validate the files.

.. literalinclude:: samples/ci-static.yml
   :language: yaml

.. _code-coverage:

Code coverage
-------------

#. Add the repository on Coveralls, the :doc:`preferred service<preferences>`
#. Append the following to ``.github/workflows/ci.yml``, commit and push:

   .. code-block:: yaml

          - env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            run: coveralls --service=github

If you're using `GitHub Actions' build matrix <https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategy>`__ and want to combine results from multiple jobs, see `this example <https://coveralls-python.readthedocs.io/en/latest/usage/configuration.html#github-actions-support>`__.

Maintenance
-----------

Find unexpected workflows:

.. code-block:: bash

   find . -path '*/workflows/*' -not -name ci.yml -not -name lint.yml -not -name js.yml -not -name shell.yml -not -name pypi.yml -not -name i18n.yml -not -path '*/node_modules/*' -not -path '*/vendor/*'

Find ``ci.yml`` files without ``lint.yml`` files, and vice versa:

.. code-block:: bash

   find . \( -name lint.yml \) -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name ci.yml) ]]; then echo {}; fi' \;
   find . \( -name ci.yml \) -not -path '*/node_modules/*' -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name lint.yml) ]]; then echo {}; fi' \;

Find and compare ``lint.yml`` files:

.. code-block:: bash

   find . -name lint.yml -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "9773a893d136df0dc82deddedd8af8563969c04a 9222eac95ab63f3c2d983ba3cf4629caea53a72e fc3eff616a7e72f41c96e48214d244c9058dbc83 953ef7f0815d49226fd2d05db8df516fff2e3fdb dfe1c0d1fbdb18bb1e2b3bcfb1f0c10fe6b06bc4" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   9773a893d136df0dc82deddedd8af8563969c04a basic
   9222eac95ab63f3c2d983ba3cf4629caea53a72e application
   fc3eff616a7e72f41c96e48214d244c9058dbc83 package
   953ef7f0815d49226fd2d05db8df516fff2e3fdb black + application
   dfe1c0d1fbdb18bb1e2b3bcfb1f0c10fe6b06bc4 black + package

Find and compare ``js.yml`` files:

.. code-block:: bash

   find . -name js.yml -exec bash -c 'echo $(tail -r {} | tail +2 | tail -r | shasum - | cut -d" " -f1) {}' \;

Find and compare ``shell.yml`` files:

.. code-block:: bash

   find . -name shell.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Find repositories with shell scripts but without ``shell.yml`` files:

.. code-block:: bash

   find . \( -path '*/script/*' -o -name '*.sh' \) -not -path '*/node_modules/*' -not -path '*/vendor/*' -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name shell.yml) ]]; then echo {}; fi' \;

Find and compare ``pypi.yml`` files:

.. code-block:: bash

   find . -name pypi.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Find repositories for Python packages but without ``pypi.yml`` files:

.. code-block:: bash

   find . -name setup.py -not -path '*/node_modules/*' -exec bash -c 'if grep long_description {} > /dev/null && [[ -z $(find $(echo {} | cut -d/ -f2) -name pypi.yml) ]]; then echo {}; fi' \;

Find and compare ``i18n.yml`` files:

.. code-block:: bash

   find . -name i18n.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Find repositories with ``LC_MESSAGES`` directories but without ``i18n.yml`` files:

.. code-block:: bash

   find . -name LC_MESSAGES -not -path '*/en/*' -exec bash -c 'if [[ -z $(find $(echo {} | cut -d/ -f2) -name i18n.yml) ]]; then echo {}; fi' \;

Reference
---------

The following prevents GitHub Actions from running a workflow twice when pushing to the branch of a pull request:

.. code-block:: yaml

   if: github.event_name == 'push' || github.event.pull_request.head.repo.full_name != github.repository
