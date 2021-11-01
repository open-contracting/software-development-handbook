Docker
======

.. seealso::

   For deploying Docker, see the  `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/docker.html>`__.

Dockerfile
----------

To increase consistency across projects:

-  Set the `non-root user <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user>`__ to ``builder``
-  Set `WORKDIR <https://docs.docker.com/engine/reference/builder/#workdir>`__ to ``/workdir``

Reference: `Dockerfile best practices <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`__

Base images
~~~~~~~~~~~

For Python, use the default image, `as recommended <https://hub.docker.com/_/python>`__, of the minor version, to ensure predictable behavior. Do not use the ``-slim`` version.

System packages
~~~~~~~~~~~~~~~

Before installing a system package, check whether it's included in a base image. For example, the ``psycopg2`` Python package `requires <https://www.psycopg.org/install/>`__ the ``libpq-dev`` system package. To check whether it's included, when using the `python:3.8 image <https://hub.docker.com/_/python>`__:

#. Find the tag on the DockerHub page of the base image (the ``3.8`` tag is under *Shared Tags*)
#. Click the link to view the Dockerfile
#. Check the ``apt-get install`` commands
#. Look for ``FROM`` instructions
#. Repeat steps 1-3 for the ``FROM`` image(s)

In this example, we find that the `buildpack-deps:bullseye image <https://github.com/docker-library/buildpack-deps/blob/master/debian/bullseye/Dockerfile>`__ installs the ``libpq-dev`` system package.

If it's not included, install iit following `best practices <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`__:

.. code-block:: none

   RUN apt-get update && apt-get install -y --no-install-recommends \
         package-a \
         package-b \
         package-c \
      && rm -rf /var/lib/apt/lists/*

Templates
~~~~~~~~~

For Python projects, adapt this Dockerfile:

.. literalinclude:: samples/Dockerfile_python
   :language: none

.dockerignore
-------------

The `.dockerignore <https://docs.docker.com/engine/reference/builder/#dockerignore-file> file`__ should only ignore tracked files (not files like ``.DS_Store`` or directories like ``__pycache__``), unless the build generates untracked files (like ``node_modules``).

.. literalinclude:: samples/dockerignore
   :language: none
