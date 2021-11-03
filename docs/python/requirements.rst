Requirements
============

Requirements are managed by four files at the root of a repository:

-  ``requirements.in`` names all direct requirements needed in the production environment, i.e. all packages ``import``'ed by the application.

   -  If the application is incompatible with older or newer versions of a requirement, use the least specific `version specifier <https://www.python.org/dev/peps/pep-0440/#version-specifiers>`__ possible, for example:

      -  Newer versions: ``foo>=1.2``, not ``foo>=1.2.3``
      -  Older versions: ``foo<2``
      -  Versions range: ``foo>=1.2,<2``

-  ``requirements_dev.in`` names all direct requirements needed exclusively in the development environment, and not in the production environment, e.g. ``pytest`` or ``pip-tools`` itself.

   -  This file should include the direct requirements needed in the production environment, by having a first line of ``-r requirements.txt``.

-  ``requirements.txt`` names all direct and indirect requirements needed in the production environment, all locked to specific versions by `pip-tools <https://pypi.org/project/pip-tools/>`__.
-  ``requirements_dev.txt`` names all direct and indirect requirements needed in the development environment, all locked to specific versions by ``pip-tools``.

This ensures that:

-  All environments use the same versions of production requirements, to ensure consistent and replicable deployments and to avoid errors or surprises during or after deployment due to differences between versions (e.g. a new version of Django requires upgrading application code).
-  Different developers and continuous integration use the same versions of development requirements, to avoid test failures due to differences between versions (e.g. a new version of pytest requires upgrading test code, or a new version of flake8 has stricter linting rules).

Get started
-----------

.. code-block:: bash

   pip install pip-tools

Add a requirement
-----------------

.. note::

   For guidance on selecting a package, see :doc:`preferences`.

Add the requirement in alphabetical order to the appropriate ``.in`` file. Then, run:

.. code-block:: bash

   pip-compile
   pip-compile requirements_dev.in

.. note::

   To declare the dependencies of packages, see :doc:`packages`.

Install requirements
--------------------

In production:

.. code-block:: bash

   pip-sync

In development:

.. code-block:: bash

   pip-sync requirements_dev.txt

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
