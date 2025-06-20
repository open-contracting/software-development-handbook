Packages
========

All our packages should be distributed on PyPI.

Use the Pypackage Cookiecutter template, and `add the repository to pre-commit.ci <https://github.com/organizations/open-contracting/settings/installations/20658712>`__:

.. code-block:: bash

   uv tool install cookiecutter
   cookiecutter gh:open-contracting/software-development-handbook --directory cookiecutter-pypackage

   uv venv -p 3.9
   uv pip install -e .[test]

   uv tool install pre-commit
   pre-commit install

.. seealso::

   Package-rated content in :ref:`Directory layout<layout-packages>`, :ref:`Testing<automated-testing>` and :ref:`Linting<linting-ci>`

Metadata
--------

If the package is distributed on PyPI, use this template for the ``pyproject.toml`` file, adding options like ``entry-points`` as needed, and removing the Jinja syntax if not using the Cookiecutter template:

.. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/pyproject.toml
   :language: jinja

If the package isn’t distributed on PyPI, use this template ``pyproject.toml``:

.. code-block:: python

   [project]
   name = "NAME"
   version = "0.0.0"

   [tool.setuptools.packages.find]
   exclude = ["tests", "tests.*"]

Reference: `Packaging and distributing projects <https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/>`__

Requirements
~~~~~~~~~~~~

-  Use ``dependencies`` and ``optional-dependencies`` in the ``pyproject.toml`` file
-  Do not use a ``requirements.txt`` file
-  Sort requirements alphabetically

.. seealso::

   :doc:`preferences`

Classifiers
~~~~~~~~~~~

``"Operating System :: OS Independent"``
  The package is tested on macOS, Windows and Ubuntu.
``"Operating System :: POSIX :: Linux"``
  The package is tested on Ubuntu only.
``"Programming Language :: Python :: Implementation :: PyPy"``
  The package is tested on PyPy.

Documentation
-------------

The template reads the documentation from a ``README.rst`` file. To convert a ``README.md`` file, install ``pandoc`` and run:

.. code-block:: bash

   pandoc --from=markdown --to=rst --output=README.rst README.md

.. seealso::

   :doc:`Python documentation guide<documentation>`

Publish releases
----------------

.. _pypi-ci:

Continuous integration
~~~~~~~~~~~~~~~~~~~~~~

To publish tagged releases to PyPI, create a ``.github/workflows/pypi.yml`` file:

.. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.github/workflows/pypi.yml
   :language: yaml

The *open-contracting* organization sets the ``PYPI_API_TOKEN`` `organization secret <https://github.com/organizations/open-contracting/settings/secrets/actions>`__ to the API token of the *opencontracting* `PyPI user <https://pypi.org/manage/account/#api-tokens>`__, and ``TEST_PYPI_API_TOKEN`` to that of the *opencontracting* Test PyPI user.

After publishing the first release to PyPI, :ref:`transfer the project to the opencontracting organization <pypi-access>`.

Release process
~~~~~~~~~~~~~~~

#. Ensure that you are on an up-to-date ``main`` branch:

   .. code-block:: bash

      git checkout main
      git pull --rebase

#. Ensure that the package is ready for release:

   -  All tests pass on continuous integration
   -  The version number is correct in ``pyproject.toml`` and ``docs/conf.py`` (if present)
   -  The changelog is up-to-date and dated

#. Tag the release, replacing ``x.y.z`` twice:

   .. code-block:: bash

      git tag -a x.y.z -m 'x.y.z release.'

#. Push the release:

   .. code-block:: bash

      git push --follow-tags

#. Announce on the `discussion group <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__ if relevant

Reference: `Publishing package distribution releases using GitHub Actions CI/CD workflows <https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>`__
