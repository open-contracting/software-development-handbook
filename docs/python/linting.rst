Linting
=======

Before writing any code, set up formatters and linters.

In general, add all project configuration to ``pyproject.toml``. Do not use ``setup.cfg``, ``setup.py``, ``.editorconfig`` or tool-specific files like ``.coveragerc`` or ``pytest.ini``.

Configuration
-------------

New projects should use the `Ruff <https://docs.astral.sh/ruff/>`__ formatter and linter, with line lengths of 119 (the Django coding style until 4.0). A starting point, based on `script.sh in standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/tests/script.sh>`__:

.. literalinclude:: samples/pyproject-ruff.toml
   :language: toml

With this starting point, check which rules fail:

.. code-block:: bash

   ruff check . --statistics

And check individual failures, for example:

.. code-block:: bash

   ruff check . --select D400

As general guidance:

-  Fix failures, if possible.
-  Use a ``# noqa: RULE`` comment if the failure is rare (for example, an ``S`` rule), or if it should be fixed, given more time. Add a short comment to explain the failure. For example: ``# noqa: S104 # Docker``
-  Use ``per-file-ignores`` if the failures occur in a single (or a set of) files. For example: ``"*/__main__.py" = ["T201"]  # print``
-  Use ``ignore`` if the failures occur in disparate files and are expected to occur in new code. For example: ``"TRY003",  # errors``
-  Use `settings <https://docs.astral.sh/ruff/settings/>`__ where possible, instead of ignoring rules entirely. Notably, use:

   -  `builtins-ignorelist <https://docs.astral.sh/ruff/settings/#lint_flake8-builtins_builtins-ignorelist>`__, instead of A002
   -  `extend-immutable-calls <https://docs.astral.sh/ruff/settings/#lint_flake8-bugbear_extend-immutable-calls>`__, instead of B008
   -  `allowed-confusables <https://docs.astral.sh/ruff/settings/#lint_allowed-confusables>`__, instead of RUF001
   -  `extend-ignore-names <https://docs.astral.sh/ruff/settings/#lint_flake8-self_extend-ignore-names>`__, instead of SLF001

``isort:skip`` and ``type: ignore`` comments should be avoided, and should reference the specific error if used, to avoid shadowing another error: for example, ``# type: ignore[attr-defined]``.

.. admonition:: Complexity rules

   We ignore the ``C901`` and all ``PLR091`` rules.

   Complexity is best measured by the effort required to read and modify code. This cannot be measured using techniques like `cyclomatic complexity <https://en.wikipedia.org/wiki/Cyclomatic_complexity>`__. Reducing cyclomatic complexity typically means extracting single-caller methods and/or using object-oriented programming, which frequently *increases* cognitive complexity.

   See the note under :ref:`create-products-sustainably`.

..
   Maintainers can check if docs/ and tests/ rules are included in projects without those directories

   diff -u <(find . -type d -maxdepth 1 ! -name '*handbook' -exec test -f '{}'/pyproject.toml -a  -d '{}'/docs \; -print            | cut -d/ -f2 | sort) <(rg -c copyright */pyproject.toml | cut -d/ -f1 | sort)
   diff -u <(find . -type d -maxdepth 1 ! -name '*handbook' -exec test -f '{}'/pyproject.toml -a  -d '{}'/docs \; -print            | cut -d/ -f2 | sort) <(rg -c docs/ */pyproject.toml | cut -d/ -f1 | sort)
   diff -u <(find . -type d -maxdepth 1 -exec test -f '{}'/pyproject.toml -a \( -d '{}'/tests -o -d '{}'/backend/tests \) \; -print | cut -d/ -f2 | sort) <(rg -c tests/ */pyproject.toml | cut -d/ -f1 | sort)

.. _linting-pre-commit:

Pre-commit hooks
----------------

To avoid pushing commits that fail formatting or linting checks, new projects should use `pre-commit <https://pre-commit.com>`__. For example, if Ruff is configured as above, create a ``.pre-commit-config.yaml`` file:

.. tab-set::

   .. tab-item:: Application

      .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.pre-commit-config.yaml
         :language: yaml

   .. tab-item:: Package

      .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.pre-commit-config.yaml
         :language: yaml

.. note::

   Applications set the correct Python version in the  `default_language_version <https://pre-commit.com/#top_level-default_language_version>`__ section. Otherwise, pre-commit.ci (or the ``pre-commit`` command locally) can use the incorrect Python version for the ``pip-compile`` hook.

   pre-commit.ci `disallows network connections <https://github.com/pre-commit-ci/issues/issues/55>`__. As such, the ``pip-compile`` hook is configured to be skipped in the ``ci`` section, and is run by the :ref:`lint.yml workflow<linting-ci>`, instead.

.. note::

   `pre-commit/pre-commit-hooks <https://github.com/pre-commit/pre-commit-hooks>`__ is not used in the templates, as the errors it covers are rarely encountered.

.. tip::

   If you encounter an error like:

   .. code-block:: none

      RuntimeError: failed to find interpreter for Builtin discover of python_spec='python3.10'

   pre-commit uses `virtualenv <https://virtualenv.pypa.io/en/latest/>`__ to `discover Python interpreters <https://virtualenv.pypa.io/en/latest/user_guide.html#python-discovery>`__. On macOS, install the missing version with Homebrew, instead of uv:

   .. code-block:: bash

      brew install python@3.10

.. _linting-ci:

Continuous integration
----------------------

Create a ``.github/workflows/lint.yml`` file.

The :doc:`django` and :doc:`Pypackage<packages>` Cookiecutter templates contain default workflows.

.. seealso::

   - Workflow files for linting :ref:`shell scripts<shell-ci>` and :ref:`Javascript files<javascript-ci>`
   - `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__ to learn about the Bash scripts

.. _python-additional-linting:

Additional linting
------------------

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
