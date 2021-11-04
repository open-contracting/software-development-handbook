Continous integration
=====================

GitHub Actions is :doc:`preferred<../general/preferences>`.

.. seealso::

   :doc:`Linting guide<linting>`

**Setup:** Most repositories use a ``.github/workflows/ci.yml`` workflow to run automated tests.

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
