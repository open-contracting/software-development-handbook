Linting
=======

Before writing any code, set up formatters and linters.

Configuration
-------------

New projects should use `Black <https://black.readthedocs.io/en/stable/>`__. All projects must use `flake8 <https://flake8.pycqa.org/en/latest/>`__ and `isort <https://pycqa.github.io/isort/>`__ with line lengths of 119 (the Django standard). If using Black, `configure it <https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html>`__ as follows:

.. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/pyproject.toml
   :language: yaml
   :caption: pyproject.toml

.. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/setup.cfg
   :language: ini
   :caption: setup.cfg

Repositories should not modify or otherwise use ``pyproject.toml``, ``setup.cfg``, ``.editorconfig`` or tool-specific files, except to ignore generated files like database migrations. ``pyproject.toml`` is preferred to tool-specific files; if it's not supported, ``setup.cfg`` is preferred – like for `Flake8 <https://github.com/PyCQA/flake8/issues/234>`__ and `Babel <https://github.com/python-babel/babel/issues/777>`__.

Maintainers can find and compare configuration files with:

.. code-block:: bash

   find . \( -name pyproject.toml -or -name setup.cfg -or -name .editorconfig -or -name .coveragerc -or -name .flake8 -or -name .isort.cfg -or -name .pylintrc -or -name pylintrc -or -name pytest.ini \) -not -path '*/node_modules/*' -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "45342d1e1c767ae5900edbcbde5c030adb30a753 ed723d5329bb74ab24e978c6b0ba6d2095e8fa1e 29418dd6acf27bb182036cf072790cb640f34c9c" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   45342d1e1c767ae5900edbcbde5c030adb30a753 pyproject.toml as above
   ed723d5329bb74ab24e978c6b0ba6d2095e8fa1e setup.cfg as above
   29418dd6acf27bb182036cf072790cb640f34c9c pytest.ini with doctests

.. _linting-pre-commit:

Pre-commit hooks
----------------

To avoid pushing commits that fail formatting/linting checks, new projects should use `pre-commit <https://pre-commit.com>`__ (add ``pre-commit`` to the :doc:`requirements_dev.in file<requirements>`. For example, if Black is configured as above, create a ``.pre-commit-config.yaml`` file:

-  For an application:

   .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.pre-commit-config.yaml
      :language: yaml
      :end-before: migrations

-  For a package:

   .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.pre-commit-config.yaml
      :language: yaml

To ignore generated files, you can add, for example, ``exclude: /migrations/`` to the end of the file.

.. note::

   `pre-commit/pre-commit-hooks <https://github.com/pre-commit/pre-commit-hooks>`__ is not used in the templates, as the errors it covers are rarely encountered.

Skipping linting
----------------

``isort:skip`` and ``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``.

The errors that are allowed to be ignored are:

-  ``E501 line too long`` for long strings, especially URLs
-  ``F401 module imported but unused`` in a library's top-level ``__init__.py`` file
-  ``E402 module level import not at top of file`` in a Django project's ``asgi.py`` file
-  ``W291 Trailing whitespace`` in tests relating to trailing whitespace
-  ``isort:skip`` if ``sys.path`` needs to be changed before an import

Maintainers can find unwanted comments with this regular expression:

.. code-block:: none

   # noqa(?!(: (E501|F401|E402|W291)| isort:skip)\n)

.. _linting-ci:

Continuous integration
----------------------

Create a ``.github/workflows/lint.yml`` file. As a base, use:

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.github/workflows/lint.yml
   :language: yaml
   :end-before: requirements_dev.txt

.. note::

   If a repository – like an OCDS extension – has no dependency file, the ``actions/cache`` action must be used instead of the ``cache`` input:

   .. code-block:: yaml

      - uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip

See the `documentation <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__ to learn about the Bash scripts.

If the project uses pre-commit, `add the repository to pre-commit.ci <https://github.com/organizations/open-contracting/settings/installations/20658712>`__ to check and fix any issues.

Otherwise, if the project uses Black, add:

.. code-block:: yaml

         - run: pip install black
         - run: black --check .

Unless the project is documentation only (like a handbook or a standard):

-  For an application, change the ``python-version`` to match the version used to compile the :doc:`requirements_dev.txt file<requirements>`, and add:

   .. code-block:: yaml

            - run: pip install -r requirements_dev.txt
            - run: pytest /tmp/test_requirements.py

-  For a package, add:

   .. code-block:: yaml

            - run: pip install .[test]
            - run: pytest /tmp/test_requirements.py

If the project is a :doc:`package<packages>`, add:

.. code-block:: yaml

         - run: pip install --upgrade check-manifest
         - run: check-manifest

Finally, add any project-specific linting, like in `notebooks-ocds <https://github.com/open-contracting/notebooks-ocds/blob/f9f42cac48f91564eba0da3c2a79ebdf7c3c43ad/.github/workflows/lint.yml#L22-L24>`__.

.. seealso::

   Workflow files for linting :ref:`shell scripts<shell-ci>` and :ref:`Javascript files<javascript-ci>`

.. _python-optional-linting:

Optional linting
----------------

.. note::

   This section is provided for reference.

`codespell <https://pypi.org/project/codespell/>`__ finds typographical errors. It is especially useful in repositories with lengthy documentation. Otherwise, all repositories can be periodically checked with:

.. code-block:: bash

   codespell -S '.git,.pytest_cache,cassettes,fixtures,_build,build,dist,target,locale,locales,vendor,node_modules,docson,htmlcov,redmine,schemaspy,*.csv,*.json,*.jsonl,*.map,*.po,european-union-support'

..
   Skip:

   -  version control directories (.git)
   -  cache directories (.pytest_cache)
   -  test fixture directories (cassettes, fixtures)
   -  built directories (_build, build, dist, htmlcov, target)
   -  non-English directories (locale, locales)
   -  generic third-party code (vendor, node_modules)
   -  specific third-party code (docson, redmine, schemaspy)
   -  non-code and non-documentation files
   -  codespell-covered repositories (european-union-support)

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: bash

   flake8 . --max-line-length 119 --max-complexity 10

.. note::

   Complexity is best measured by the effort required to read and modify code. This cannot be measured using techniques like cyclomatic complexity. Reducing cyclomatic complexity typically means extracting single-caller methods and/or using object-oriented programming, which frequently *increase* cognitive complexity. See the note under :ref:`create-products-sustainably`.

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: bash

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``.
