Python
======

.. _python-license:

License
-------

Use the `BSD 3-clause license <https://choosealicense.com/licenses/bsd-3-clause/>`__.

Version
-------

Applications use the Python version in the `latest Ubuntu LTS version <https://packages.ubuntu.com>`__ (search for the "python3" package within the LTS suite), or a later version. Packages are written for non-end-of-life versions (`see the status of Python branches <https://devguide.python.org/versions/#versions>`__).

In applications, set the version in the ``.python-version`` file and in the ``requires-python`` key of the ``pyproject.toml`` file, which Ruff uses as its target version.

.. toctree::
   :caption: Contents
   :maxdepth: 2

   layout
   requirements
   preferences
   linting
   tests
   ci
   documentation
   settings
   logging
   django
   file_formats
   style_guide
   i18n
   a11y
   performance
   packages

Reference: `18F Python Development Guide <https://guides.18f.org/engineering/languages-runtimes/python/>`__
