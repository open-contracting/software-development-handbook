Packages
========

All our packages should be distributed on PyPi.

setup.py
--------

If the package is distributed on PyPi, use this template ``setup.py``, adding arguments like ``entry_points``, ``extras_require`` and ``namespace_packages`` as needed:

.. code:: python

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
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
       ],
   )

If the package is tested on macOS, Windows and Ubuntu, you can add the ``'Operating System :: OS Independent'`` classifier.

If the package isn’t distributed on PyPi, use this template ``setup.py``:

.. code:: python

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

::

   pandoc --from=markdown --to=rst --output=README.rst README.md

Requirements
------------

-  Use ``install_requires`` and ``extras_require`` in ``setup.py``
-  Do not use ``requirements.txt``
-  Sort requirements alphabetically

Release process
---------------

#. Ensure all tests pass on continuous integration
#. Ensure the version number is correct in ``setup.py`` and ``docs/conf.py`` (if present)
#. Ensure the changelog is up-to-date and dated
#. Run ``check-manifest`` (``pip install check-manifest`` if not yet installed)
#. Tag the release: ``git tag -a x.y.z -m 'x.y.z release.'; git push --tags``
#. Remove old builds: ``rm -rf dist/``
#. Build the package: ``python setup.py sdist``
#. Upload to PyPI: ``twine upload dist/*`` (``pip install twine`` if not yet installed)
#. Announce on the `discussion group <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__ if relevant
