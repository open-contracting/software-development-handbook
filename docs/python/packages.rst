Packages
========

All our packages should be distributed on PyPi.

setup.py
--------

If the package is distributed on PyPi, use this template ``setup.py``, adding arguments like ``entry_points``, ``extras_require`` and ``namespace_packages`` as needed:

.. code-block:: python

   from setuptools import find_packages, setup

   with open('README.rst') as f:
       long_description = f.read()

   setup(
       name='NAME',
       version='0.0.0',
       author='Open Contracting Partnership',
       author_email='data@open-contracting.org',
       url='https://github.com/open-contracting/REPOSITORY',
       description='DESCRIPTION',
       license='BSD',
       packages=find_packages(exclude=['tests', 'tests.*']),
       long_description=long_description,
       install_requires=[
           'REQUIREMENT',
       ],
       classifiers=[
           'License :: OSI Approved :: BSD License',
           'Operating System :: POSIX :: Linux',
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
       ],
   )

If the package is tested on macOS, Windows and Ubuntu, you can use the ``'Operating System :: OS Independent'`` classifier, instead.

If the package isn’t distributed on PyPi, use this template ``setup.py``:

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

To change a readme from Markdown to reStructuredText, install ``pandoc`` and run:

.. code-block:: bash

   pandoc --from=markdown --to=rst --output=README.rst README.md

Requirements
------------

-  Use ``install_requires`` and ``extras_require`` in ``setup.py``
-  Do not use ``requirements.txt``
-  Sort requirements alphabetically

.. _packages-testing:

Automated testing
-----------------

A package can be tested with:

.. code-block:: shell

   pip install .[test]
   pytest

Release process
---------------

.. admonition:: One-time setup

   Copy this `GitHub Actions workflow <https://raw.githubusercontent.com/open-contracting/ocds-babel/main/.github/workflows/pypi.yml>`__ to the new package's repository, to publish tagged releases to PyPi. Ensure that ``check-manifest`` is run in a workflow.

   The *open-contracting* organization sets the ``PYPI_API_TOKEN`` `organization secret <https://github.com/organizations/open-contracting/settings/secrets/actions>`__ to the API token of the *opencontracting* `PyPi user <https://pypi.org/manage/account/#api-tokens>`__, and ``TEST_PYPI_API_TOKEN`` to that of the TestPyPi user.

   After publishing the first release to PyPi, :ref:`add additional owners <pypi-access>`.

#. Ensure that you are on the ``main`` branch:

   .. code-block:: shell

      git checkout main

#. Ensure that the package is ready for release:

   -  All tests pass on continuous integration
   -  The version number is correct in ``setup.py`` and ``docs/conf.py`` (if present)
   -  The changelog is up-to-date and dated

#. Tag the release, replacing ``x.y.z`` twice:

   .. code-block:: shell

      git tag -a x.y.z -m 'x.y.z release.'

#. Push the release:

   .. code-block:: shell

      git push --follow-tags

#. Announce on the `discussion group <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__ if relevant

Reference
---------

-  `Packaging and distributing projects <https://packaging.python.org/guides/distributing-packages-using-setuptools/>`__
-  `Publishing package distribution releases using GitHub Actions CI/CD workflows <https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>`__
