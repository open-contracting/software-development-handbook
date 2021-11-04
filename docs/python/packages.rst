Packages
========

All our packages should be distributed on PyPI.

.. seealso::

   Package-rated content in :ref:`Directory layout<layout-packages>`, :ref:`Testing<automated-testing>` and :ref:`Linting<linting-ci>`

Metadata
--------

If the package is distributed on PyPI, use this template for the ``setup.py`` file, adding arguments like ``entry_points``, ``extras_require`` and ``namespace_packages`` as needed:

.. literalinclude:: samples/setup.py
   :language: python

If the package isn’t distributed on PyPI, use this template ``setup.py``:

.. code-block:: python

   from setuptools import find_packages, setup

   setup(
       name='NAME',
       version='0.0.0',
       packages=find_packages(),
       install_requires=[
           'REQUIREMENT',
       ],
   )

.. note::

   We don't use ``pyproject.toml`` or ``setup.cfg`` for packaging, preferring a single ``setup.py`` file.

Reference: `Packaging and distributing projects <https://packaging.python.org/guides/distributing-packages-using-setuptools/>`__

Requirements
~~~~~~~~~~~~

-  Use ``install_requires`` and ``extras_require`` in the ``setup.py`` file
-  Do not use a ``requirements.txt`` file
-  Sort requirements alphabetically

.. seealso::

   :doc:`preferences`

Classifiers
~~~~~~~~~~~

-  If the package is tested on macOS, Windows and Ubuntu, use the ``'Operating System :: OS Independent'`` classifier, instead.
-  If the package is tested on PyPy, add the ``'Programming Language :: Python :: Implementation :: PyPy'`` classifier.

Documentation
-------------

The template reads the documentation from a ``README.rst`` file. To convert a ``README.md`` file, install ``pandoc`` and run:

.. code-block:: bash

   pandoc --from=markdown --to=rst --output=README.rst README.md

.. seealso::

   :doc:`Python documentation guide<documentation>`

.. _python-package-release-process:

Release process
---------------

.. admonition:: One-time setup

   Copy this `GitHub Actions workflow <https://raw.githubusercontent.com/open-contracting/ocds-babel/main/.github/workflows/pypi.yml>`__ to the new package's repository, to publish tagged releases to PyPI. Ensure that ``check-manifest`` is run in a workflow.

   The *open-contracting* organization sets the ``PYPI_API_TOKEN`` `organization secret <https://github.com/organizations/open-contracting/settings/secrets/actions>`__ to the API token of the *opencontracting* `PyPI user <https://pypi.org/manage/account/#api-tokens>`__, and ``TEST_PYPI_API_TOKEN`` to that of the TestPyPI user.

   After publishing the first release to PyPI, :ref:`add additional owners <pypi-access>`.

#. Ensure that you are on the ``main`` branch:

   .. code-block:: bash

      git checkout main

#. Ensure that the package is ready for release:

   -  All tests pass on continuous integration
   -  The version number is correct in ``setup.py`` and ``docs/conf.py`` (if present)
   -  The changelog is up-to-date and dated

#. Tag the release, replacing ``x.y.z`` twice:

   .. code-block:: bash

      git tag -a x.y.z -m 'x.y.z release.'

#. Push the release:

   .. code-block:: bash

      git push --follow-tags

#. Announce on the `discussion group <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__ if relevant

Maintainers can find and compare PyPI workflow files with:

.. code-block:: bash

   find . -name pypi.yml -exec bash -c 'echo $(shasum {} | cut -d" " -f1) {}' \;

Reference: `Publishing package distribution releases using GitHub Actions CI/CD workflows <https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>`__
