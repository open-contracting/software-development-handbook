Linting
=======

All code should be checked as documented by `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Configuration
-------------

Repositories should not use ``setup.cfg``, ``pyproject.toml``, ``.editorconfig`` or tool-specific files to configure the behavior of tools, except to ignore generated files like database migrations.

.. note::

   If a project uses `Black <https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html?highlight=flake8>`__, it needs a ``setup.cfg`` file for `flake8 <https://github.com/PyCQA/flake8/issues/234>`__ and ``isort`` and a ``pyproject.toml`` file for `black <https://github.com/psf/black/issues/683>`__. Black is not used in all projects, because its `vertical style <https://github.com/open-contracting/standard-maintenance-scripts/issues/148#issuecomment-693556236>`__ is slower to scan.

Maintainers can find configuration files with:

.. code-block:: bash

   find . \( -name setup.cfg -or -name pyproject.toml -or -name .editorconfig -or -name .flake8 -or -name .isort.cfg -or -name .pylintrc -or -name pylintrc -or -name pytest.ini \) -not -path '*/node_modules/*' -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "4b679b931113f9a779bfea5e8c55cea40f8a5efe 1031acedc073ce860655c192071a0b0ad7653919" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   4b679b931113f9a779bfea5e8c55cea40f8a5efe minimal pyproject.toml file for Black
   1031acedc073ce860655c192071a0b0ad7653919 minimal setup.cfg file for Black

Allowing exceptions
-------------------

``isort:skip`` and ``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``. The errors that are allowed to be ignored are:

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

If the project uses Black, add:

.. code-block:: yaml

         - run: pip install black
         - run: black --check .

Unless the project is documentation only, add:

-  For an application:

   .. code-block:: yaml

            - run: pip install -r requirements_dev.txt
            - run: pytest /tmp/test_requirements.py

-  For a package:

   .. code-block:: yaml

            - run: pip install .[test]
            - run: pytest /tmp/test_requirements.py

If the project includes :doc:`shell scripts<../shell/index>`, add:

.. code-block:: yaml

         - run: sudo apt install shellcheck
         - run: sudo snap install shfmt
         - run: shellcheck $(shfmt -f .)
         - run: shfmt -d -i 4 -sr $(shfmt -f .)

If the project is a :doc:`package<packages>`, add:

.. code-block:: yaml

         - run: pip install --upgrade check-manifest setuptools
         - run: check-manifest

Finally, add any project-specific linting, like in `notebooks-ocds <https://github.com/open-contracting/notebooks-ocds/blob/f9f42cac48f91564eba0da3c2a79ebdf7c3c43ad/.github/workflows/lint.yml#L22-L24>`__

If the project contains JavaScript, you can create a ``.github/workflows/js.yml`` file, following :ref:`this template<javascript-ci>`.

Optional linting
----------------

.. note::

   This section is provided for reference.

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: bash

   flake8 . --max-line-length 119 --max-complexity 10

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: bash

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``.
