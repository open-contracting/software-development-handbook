Continous integration
=====================

GitHub Actions is :doc:`preferred<../general/preferences>`.

**Setup:** Most repositories use a ``.github/workflows/ci.yml`` workflow to run automated tests.

Code style
----------

**Setup:** Most repositories use a ``.github/workflows/lint.yml`` workflow to run style checks, as documented in `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

.. _common-checks:

Common checks
~~~~~~~~~~~~~

All code is checked as documented by `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Repositories should not use ``setup.cfg``, ``pyproject.toml``, ``.editorconfig`` or tool-specific files to configure the behavior of tools, except to ignore generated files like database migrations. Maintainers can find configuration files with:

.. code-block:: shell

   find . \( -name setup.cfg -or -name pyproject.toml -or -name .editorconfig -or -name .flake8 -or -name .isort.cfg -or -name .pylintrc -or -name pylintrc -or -name pytest.ini \) -not -path '*/node_modules/*' -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "4b679b931113f9a779bfea5e8c55cea40f8a5efe 1031acedc073ce860655c192071a0b0ad7653919" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   4b679b931113f9a779bfea5e8c55cea40f8a5efe minimal pyproject.toml file for Black
   1031acedc073ce860655c192071a0b0ad7653919 minimal setup.cfg file for Black

.. note::

   If a project uses `Black <https://black.readthedocs.io/en/stable/>`__, it needs a ``setup.cfg`` file for `flake8 <https://github.com/PyCQA/flake8/issues/234>`__ and ``isort`` and a ``pyproject.toml`` file for `black <https://github.com/psf/black/issues/683>`__. Otherwise, use only a ``setup.cfg`` file. Black is not used in all projects, because its `vertical style <https://github.com/open-contracting/standard-maintenance-scripts/issues/148#issuecomment-693556236>`__ is slower to scan.

``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``. The errors that are allowed to be ignored are:

-  ``E501 line too long`` for long strings, especially URLs
-  ``F401 module imported but unused`` in a library's top-level ``__init__.py`` file
-  ``W291 Trailing whitespace`` in tests relating to trailing whitespace
-  ``isort:skip`` if ``sys.path`` needs to be changed before an import

Maintainers can find unwanted ``noqa`` comments with this regular expression: ``# noqa(?!(: (E501|F401|W291)| isort:skip)\n)``

Otherwise, please refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

Optional checks
~~~~~~~~~~~~~~~

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: shell

   flake8 . --max-line-length 119 --max-complexity 10

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: shell

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``.

.. _code-coverage:

Code coverage
-------------

Coveralls is :doc:`preferred<preferences>`.

**Setup:** On Coveralls, add the repository. Then, append the following to ``.github/workflows/ci.yml``, commit and push:

.. code-block:: yaml

       - env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
         run: coveralls --service=github

.. note::

   If you're using `GitHub Actions' build matrix <https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategy>`__ and want to combine results from the multiple jobs, `follow this example <https://coveralls-python.readthedocs.io/en/latest/usage/configuration.html#github-actions-support>`__.

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

Packages should be tested on Ubuntu, macOS and Windows, on Python versions that aren't end-of-life, and on the latest version of PyPy. For example:

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

Branch protection
-----------------

See :ref:`branch-protection`.

**Setup:** A Rake task is used to protect default branches and to require automated tests and style checks to pass before merging on GitHub, as documented at :ref:`branch-protection`.
