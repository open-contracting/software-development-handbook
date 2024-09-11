Linting
=======

Before writing any code, set up formatters and linters.

Configuration
-------------

New projects should use the `Ruff <https://docs.astral.sh/ruff/>`__ formatter and linter, with line lengths of 119 (the Django coding style until 4.0), configured as follows:

.. tab-set::

   .. tab-item:: Python

      .. code-block:: yaml
         :caption: pyproject.toml

         [tool.ruff]
         line-length = 119
         target-version = "py311"

         [tool.ruff.lint]
         select = ["E", "C4", "F", "I", "W"]

   .. tab-item:: Package

      .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/pyproject.toml
         :language: yaml
         :caption: pyproject.toml

   .. tab-item:: Django

      .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/pyproject.toml
         :language: yaml
         :caption: pyproject.toml

Do not use ``setup.cfg``, ``setup.py``, ``.editorconfig`` or tool-specific files like ``.coveragerc``.

.. _linting-pre-commit:

Pre-commit hooks
----------------

To avoid pushing commits that fail formatting/linting checks, new projects should use `pre-commit <https://pre-commit.com>`__. For example, if Ruff is configured as above, create a ``.pre-commit-config.yaml`` file:

.. tab-set::

   .. tab-item:: Application

      .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.pre-commit-config.yaml
         :language: yaml

   .. tab-item:: Package

      .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.pre-commit-config.yaml
         :language: yaml

.. note::

   `pre-commit/pre-commit-hooks <https://github.com/pre-commit/pre-commit-hooks>`__ is not used in the templates, as the errors it covers are rarely encountered.

Skipping linting
----------------

``noqa``, ``isort:skip`` and ``type: ignore`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501`` or ``# type: ignore[attr-defined]``.

The errors that are allowed to be ignored per line are:

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

Create a ``.github/workflows/lint.yml`` file. The :doc:`django` and :doc:`Pypackage<packages>` Cookiecutter templates contain default workflows.

.. seealso::

   - Workflow files for linting :ref:`shell scripts<shell-ci>` and :ref:`Javascript files<javascript-ci>`
   - `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__ to learn about the Bash scripts

.. _python-optional-linting:

Optional linting
----------------

`codespell <https://pypi.org/project/codespell/>`__ finds typographical errors. It is especially useful in repositories with lengthy documentation. Otherwise, all repositories can be periodically checked with:

.. code-block:: bash

   codespell -S '.git,.pytest_cache,cassettes,fixtures,_build,build,dist,target,locale,locales,vendor,node_modules,docson,htmlcov,schemaspy,*.csv,*.json,*.jsonl,*.map,*.po,european-union-support'

..
   Skip:

   -  version control directories (.git)
   -  cache directories (.pytest_cache)
   -  test fixture directories (cassettes, fixtures)
   -  built directories (_build, build, dist, htmlcov, target)
   -  non-English directories (locale, locales)
   -  generic third-party code (vendor, node_modules)
   -  specific third-party code (docson, htmlcov, schemaspy)
   -  non-code and non-documentation files
   -  codespell-covered repositories (european-union-support)

.. admonition:: Complexity rules

   Complexity is best measured by the effort required to read and modify code. This cannot be measured using techniques like `cyclomatic complexity <https://en.wikipedia.org/wiki/Cyclomatic_complexity>`__. Reducing cyclomatic complexity typically means extracting single-caller methods and/or using object-oriented programming, which frequently *increases* cognitive complexity. See the note under :ref:`create-products-sustainably`.
