Applications
============

Python applications are different from :doc:`packages` in that:

-  Applications are not declared as dependencies by other software, and therefore do not have a ``setup.py`` file
-  Applications are deployed to servers, and therefore freeze requirements in ``requirements.txt`` to have consistent deploys

The default branch of applications should always be deployable, which requires that:

-  Tests pass on continuous integration
-  Installation instructions are consistent with the `deploy <https://github.com/open-contracting/deploy>`__ repository

If installation instructions change (e.g. if a new service like Redis is required), then the ``deploy`` repository must be updated.

Requirements
------------

Requirements are managed by four files at the root of a repository:

-  ``requirements.in`` names all direct requirements needed in the production environment, i.e. all packages ``import``'ed by the application.

   -  If the application is incompatible with older or newer versions of a requirement, use the least specific `version specifier <https://www.python.org/dev/peps/pep-0440/#version-specifiers>`__ possible, for example:

      -  requires newer versions: use ``foo>=1.2`` instead of ``foo>=1.2.3``
      -  requires older versions: use ``foo<2``
      -  requires versions range: use ``foo>=1.2,<2``

-  ``requirements_dev.in`` names all direct requirements needed exclusively in the development environment, and not in the production environment, e.g. ``pytest``.

   -  This file typically also includes the direct requirements needed in the production environment, by having a first line of ``-r requirements.txt``.

-  ``requirements.txt`` names all direct and indirect requirements needed in the production environment, all locked to specific versions.
-  ``requirements_dev.txt`` names all direct and indirect requirements needed in the development environment, all locked to specific versions.

The above ensures that:

-  Development and production environments use the same versions of production requirements, to avoid errors or surprises during or after deployment due to differences between versions (e.g. a new version of Django requires upgrading application code).
-  Different developers and continuous integration use the same versions of development requirements, to avoid test failures due to differences between versions (e.g. a new version of pytest requires upgrading test code, or a new version of flake8 has stricter linting rules).

The ``requirements*.txt`` files should be periodically updated, both for security updates and to better distribute the maintenance burden of upgrading versions over time. ``pip-tools`` is used to manage the ``requirements*.txt`` files (it is included in ``requirements_dev.*``).

To upgrade all dependencies:

.. code-block:: shell

   pip-compile --upgrade
   pip-compile --upgrade requirements_dev.in

To upgrade one dependency, run, for example:

.. code-block:: shell

   pip-compile -P requests
   pip-compile -P requests requirements_dev.in

After adding a dependency, run:

.. code-block:: shell

   pip-compile
   pip-compile requirements_dev.in

Configuration
-------------

All application interfaces should read configuration from environment variables, like in the `Twelve-Factor App methodology <https://12factor.net>`__. Environment variables are configured in the `deploy repository <https://github.com/open-contracting/deploy>`__.

Web context
  For a `Django application <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/python.html>`__, configure the environment variables in its Pillar file. The configuration is deployed via a `uWSGI INI file <https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html>`__.
:ref:`Command-line interface<python-scripts>` context
  Configure the environment variables in a ``.env`` file, and deploy the file. In the application, use `python-dotenv <https://pypi.org/project/python-dotenv/>`__ (not `django-environ <https://pypi.org/project/django-environ/>`__) to load the file: for example, `kingfisher-archive <https://github.com/open-contracting/kingfisher-archive/blob/main/manage.py>`__.

Otherwise, read configuration from INI files using `configparser <https://docs.python.org/3/library/configparser.html>`__. Do not use: JSON (no comments), YAML (data typing, too many features, not in standard library), `TOML <https://github.com/madmurphy/libconfini/wiki/An-INI-critique-of-TOML>`__ (data typing, too many features, not in standard library), or XML (verbose, not in standard library).
