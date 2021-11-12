Linting
=======

Before writing any code, set up formatters and linters.

Configuration
-------------

New projects should use `Black <https://black.readthedocs.io/en/stable/>`__. All projects must use `flake8 <https://flake8.pycqa.org/en/latest/>`__ and `isort <https://pycqa.github.io/isort/>`__ with line lengths of 119 (the Django standard). If using Black, `configure it <https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html>`__ as follows:

.. code-block:: toml
   :caption: pyproject.toml

   [tool.black]
   line-length = 119

   [tool.isort]
   profile = 'black'
   line_length = 119

.. code-block:: ini
   :caption: setup.cfg

   [flake8]
   max-line-length = 119
   extend-ignore = E203

Repositories should not modify or otherwise use ``setup.cfg``, ``pyproject.toml``, ``.editorconfig`` or tool-specific files, except to ignore generated files like database migrations.

Maintainers can find and compare configuration files with:

.. code-block:: bash

   find . \( -name setup.cfg -or -name pyproject.toml -or -name .editorconfig -or -name .flake8 -or -name .isort.cfg -or -name .pylintrc -or -name pylintrc -or -name pytest.ini \) -not -path '*/node_modules/*' -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "45342d1e1c767ae5900edbcbde5c030adb30a753 ed723d5329bb74ab24e978c6b0ba6d2095e8fa1e 29418dd6acf27bb182036cf072790cb640f34c9c" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   45342d1e1c767ae5900edbcbde5c030adb30a753 pyproject.toml as above
   ed723d5329bb74ab24e978c6b0ba6d2095e8fa1e setup.cfg as above
   29418dd6acf27bb182036cf072790cb640f34c9c pytest.ini with doctests

Pre-commit hooks
----------------

To avoid pushing commits that fail formatting/linting checks, new projects should use `pre-commit <https://pre-commit.com>`__ (add ``pre-commit`` to the :doc:`requirements_dev.in file<requirements>`. For example, if Black is configured as above:

.. code-block:: yaml
   :caption: .pre-commit-config.yaml

   repos:
     - repo: https://github.com/psf/black
       rev: 21.5b2
       hooks:
         - id: black
     - repo: https://github.com/pycqa/flake8
       rev: 3.9.2
       hooks:
         - id: flake8
     - repo: https://github.com/pycqa/isort
       rev: 5.8.0
       hooks:
         - id: isort
     - repo: https://github.com/jazzband/pip-tools
       rev: 6.4.0
       hooks:
         - id: pip-compile
           name: pip-compile requirements.in
           files: ^requirements\.(in|txt)$
         - id: pip-compile
           name: pip-compile requirements_dev.in
           files: ^requirements(_dev)?\.(in|txt)$
           args: [requirements_dev.in]

To ignore generated files, you can add, for example, ``exclude: /migrations/`` to the end of the file.

Skipping linting
----------------

``isort:skip`` and ``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``.

The errors that are allowed to be ignored are:

-  ``E501 line too long`` for long strings, especially URLs
-  ``F401 module imported but unused`` in a library's top-level ``__init__.py`` file
-  ``W291 Trailing whitespace`` in tests relating to trailing whitespace
-  ``isort:skip`` if ``sys.path`` needs to be changed before an import

Maintainers can find unwanted comments with this regular expression:

.. code-block:: none

   # noqa(?!(: (E501|F401|W291)| isort:skip)\n)

.. _linting-ci:

Continuous integration
----------------------

Create a ``.github/workflows/lint.yml`` file. As a base, use:

.. literalinclude:: samples/lint.yml
   :language: yaml

See the `documentation <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__ to learn about the Bash scripts.

If the project uses pre-commit, `pre-commit.ci <https://pre-commit.ci>`__ checks and fixes any linting issues.

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

         - run: pip install --upgrade check-manifest setuptools
         - run: check-manifest

Finally, add any project-specific linting, like in `notebooks-ocds <https://github.com/open-contracting/notebooks-ocds/blob/f9f42cac48f91564eba0da3c2a79ebdf7c3c43ad/.github/workflows/lint.yml#L22-L24>`__.

.. seealso::

   Workflow files for linting :ref:`shell scripts<shell-ci>` and :ref:`Javascript files<javascript-ci>`

Optional linting
----------------

.. note::

   This section is provided for reference. In general, these are not worth the effort.

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: bash

   flake8 . --max-line-length 119 --max-complexity 10

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: bash

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``.
