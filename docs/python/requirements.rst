Requirements
============

Now that you have a :doc:`directory layout<layout>`, you can declare the project's requirements.

The requirements of *applications* (not :doc:`packages<packages>`) are managed by four files:

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

A common starter ``requirements.in`` for :doc:`django` is:

.. code-block:: none

   dj-database-url
   django
   psycopg2
   sentry-sdk

A common starter ``requirements_dev.in`` for linting is:

.. code-block:: none

   -r requirements.txt
   black
   coveralls
   flake8
   isort
   pip-tools
   pre-commit

If using Django, add:

.. code-block:: none

   coverage

Otherwise, add:

.. code-block:: none

   pytest
   pytest-cov

Add a requirement
-----------------

Add the requirement in alphabetical order to the appropriate ``.in`` file. Then, run:

.. code-block:: bash

   pip-compile
   pip-compile requirements_dev.in

If running ``pip-compile`` introduces unexpected differences, upgrade ``pip-tools`` to the latest version, and check that you are using the same version of Python as for other runs.

.. seealso::

   :doc:`preferences`

.. _requirements-psycopg2:

psycopg2
~~~~~~~~

``psycopg2`` is `recommended <https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary>`__ for production. However, installing ``psycopg2`` for development can be difficult on operating systems like macOS. In that case, you can:

-  Put ``psycopg2`` in ``requirements.in``
-  Put ``psycopg2-binary`` in ``requirements_dev.in``
-  Run: ``pip install psycopg2-binary``

.. note::

   You **must** keep the locked versions of psycopg2 and psycopg2-binary in sync.

Install requirements
--------------------

In development:

.. code-block:: bash

   pip-sync requirements_dev.txt

In production:

.. code-block:: bash

   pip-sync -q --pip-args "--exists-action w"

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
