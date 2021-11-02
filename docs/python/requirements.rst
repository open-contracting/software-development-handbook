Requirements
============

.. note::

   To declare the dependencies of packages, see :doc:`packages`.

`pip-tools <https://pypi.org/project/pip-tools/>`__ manages the requirement files ending in ``.txt``. Developers manage the requirement files ending in ``.in``. See :ref:`requirements-organization` to learn more.

.. code-block:: bash

   pip install pip-tools

Install requirements
--------------------

In production:

.. code-block:: bash

   pip-sync

In development:

.. code-block:: bash

   pip-sync requirements_dev.txt

Add requirements
----------------

After adding a requirement to a ``requirements*.in`` file, run:

.. code-block:: bash

   pip-compile
   pip-compile requirements_dev.in

Upgrade requirements
--------------------

Requirements should be periodically updated, both for security updates and to better distribute the maintenance burden of upgrading versions over time.

Upgrade one requirement, for example:

.. code-block:: bash

   pip-compile -P requests
   pip-compile -P requests requirements_dev.in

Upgrade all requirements:

.. code-block:: bash

   pip-compile --upgrade
   pip-compile --upgrade requirements_dev.in

.. _requirements-organization:

What goes in which file
-----------------------

Applications are not declared as dependencies by other software, and therefore do not have a ``setup.py`` file in which to list requirements. Instead, requirements are managed by four files at the root of a repository:

-  ``requirements.in`` names all direct requirements needed in the production environment, i.e. all packages ``import``'ed by the application.

   -  If the application is incompatible with older or newer versions of a requirement, use the least specific `version specifier <https://www.python.org/dev/peps/pep-0440/#version-specifiers>`__ possible, for example:

      -  requires newer versions: use ``foo>=1.2`` instead of ``foo>=1.2.3``
      -  requires older versions: use ``foo<2``
      -  requires versions range: use ``foo>=1.2,<2``

-  ``requirements_dev.in`` names all direct requirements needed exclusively in the development environment, and not in the production environment, e.g. ``pytest`` or ``pip-tools`` itself.

   -  This file typically also includes the direct requirements needed in the production environment, by having a first line of ``-r requirements.txt``.

-  ``requirements.txt`` names all direct and indirect requirements needed in the production environment, all locked to specific versions.
-  ``requirements_dev.txt`` names all direct and indirect requirements needed in the development environment, all locked to specific versions.

The above ensures that:

-  All environments use the same versions of production requirements, to ensure consistent and replicable deployments and to avoid errors or surprises during or after deployment due to differences between versions (e.g. a new version of Django requires upgrading application code).
-  Different developers and continuous integration use the same versions of development requirements, to avoid test failures due to differences between versions (e.g. a new version of pytest requires upgrading test code, or a new version of flake8 has stricter linting rules).

For easier reference, sort the lines in the ``requirements*.in`` files alphabetically.
