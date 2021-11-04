Continous integration
=====================

.. seealso::

   Workflows for linting :doc:`Python<linting>`, :ref:`JavaScript<javascript-ci>` and :ref:`shell scripts<shell-ci>` and for :ref:`releasing packages<python-package-release-process>`

Automated tests
---------------

Packages
~~~~~~~~

Create a ``.github/workflows/ci.yml`` file. As a base, use:

-  If using `tox <http://tox.readthedocs.org>`__:

   .. literalinclude:: samples/ci-package-tox.yml
      :language: yaml

-  Otherwise, replacing ``PACKAGENAME``:

   .. literalinclude:: samples/ci-package.yml
      :language: yaml

If the package has optional support for `orjson <https://pypi.org/project/orjson/>`__, to test on PyPy, replace the ``pytest`` step with the following steps, replacing ``PACKAGENAME``: 

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

i18n coverage
-------------

Repositories that support multiple locales should test that translations are complete.

This test is run on `pull request <https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request>`__ events, not `push <https://docs.github.com/en/actions/reference/events-that-trigger-workflows#push>`__ events, to allow developers to see test results on feature branches, before creating a pull request.

For example, `cove-ocds <https://github.com/open-contracting/cove-ocds/blob/main/.github/workflows/ci.yml>`__ runs:

.. code-block:: yaml

   - run: sudo apt install gettext translate-toolkit
   - run: python manage.py makemessages -l es
   - run: "[ \"$GITHUB_EVENT_NAME\" != \"pull_request\" ] || [ \"`pocount --incomplete cove_ocds/locale/es/LC_MESSAGES/django.po`\" = \"\" ]"

In other words, either the event isn't a pull request, or the ``pocount`` command's output is empty.

Test matrix
-----------

:doc:`packages` should be tested on Ubuntu, macOS and Windows, on Python versions that aren't end-of-life, and on the latest version of PyPy. For example:

.. code-block:: yaml

   name: CI
   on: [push, pull_request]
   jobs:
     build:
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           os: [macos-latest, windows-latest, ubuntu-latest]
           python-version: [3.6, 3.7, 3.8, 3.9, pypy-3.7]
       steps:
       - uses: actions/checkout@v2
       - uses: actions/setup-python@v2
         with:
           python-version: ${{ matrix.python-version }}

.. note::

   If a package requires `service containers <https://docs.github.com/en/actions/guides/about-service-containers>`__, you must use an Ubuntu runner.

Maintenance
-----------

Find unexpected workflows:

.. code-block:: bash

   find . -path '*/workflows/*' -not -name ci.yml -not -name lint.yml -not -name js.yml -not -name shell.yml -not -name pypi.yml -not -path '*/node_modules/*' -not -path '*/vendor/*'

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

   find . -name setup.py -not -path '*/node_modules/*' -exec bash -c 'if grep long_description {} > /dev/null && [[ -z $(find $(echo {} | cut -d/ -f2) -name pypi.yml) ]]; then echo {}; fi' \;
