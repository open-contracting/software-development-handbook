Applications
============

Python applications are different from :doc:`packages` in that:

-  Applications are not declared as dependencies by other software, and therefore do not have a ``setup.py`` file
-  Applications are deployed to servers, and therefore freeze requirements in ``requirements.txt`` to have consistent deploys

The ``master`` branch of applications should always be deployable, which requires that:

-  Tests pass on continuous integration
-  Installation instructions are consistent with the ```deploy`` <https://github.com/open-contracting/deploy>`__ repository

If installation instructions change (e.g. if a new service like Redis is required), then the ``deploy`` repository must be updated.

Requirements
------------

Requirements are managed by four files at the root of a repository:

-  ``requirements.in`` names all direct requirements needed in the production environment, i.e. all packages ``import``'ed by the application.

   -  If the application is incompatible with older or newer versions of a requirement, use the least specific `version specifier <https://www.python.org/dev/peps/pep-0440/#version-specifiers>`__ possible, for example:

      -  requires newer versions: use ``foo>=1.2`` instead of ``foo>=1.2.3``
      -  requires older versions: use ``foo<2``
      -  requires versions range: use ``foo>=1.2,<2``

-  ``requirements_dev.in`` names all direct requirements needed exclusively in the development environment, and not in the production environment, e.g. ``pytest``.

   -  This file typically also includes the direct requirements needed in the production environment, by having a first line of ``-r requirements.txt``.

-  ``requirements.txt`` names all direct and indirect requirements needed in the production environment, all locked to specific versions.
-  ``requirements_dev.txt`` names all direct and indirect requirements needed in the development environment, all locked to specific versions.

The above ensures that:

-  Development and production environments use the same versions of production requirements, to avoid errors or surprises during or after deployment due to differences between versions (e.g. a new version of Django requires upgrading application code).
-  Different developers and continuous integration use the same versions of development requirements, to avoid unexpected test failures due to differences between versions (e.g. a new version of pytest requires upgrading test code, or a new version of flake8 has stricter linting rules).

The ``requirements*.txt`` files should be periodically updated, both for security updates and to better distribute the maintenance burden of upgrading versions over time. ``pip-tools`` is used to manage the ``requirements*.txt`` files (it is included in ``requirements_dev.*``).

To upgrade all dependencies:

.. code:: shell

   pip-compile --upgrade
   pip-compile --upgrade requirements_dev.in

To upgrade one dependency, run, for example:

.. code:: shell

   pip-compile -P requests
   pip-compile -P requests requirements_dev.in

After adding a dependency, run:

.. code:: shell

   pip-compile
   pip-compile requirements_dev.in
