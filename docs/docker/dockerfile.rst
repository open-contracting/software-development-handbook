Dockerfile
==========

Code style
----------

To increase consistency across projects:

-  Use the name ``runner`` for the `non-root user <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user>`__:

   .. code-block:: docker

      RUN groupadd -r runner && useradd --no-log-init -r -g runner runner

-  Use the ``user:group`` form for the `USER <https://docs.docker.com/engine/reference/builder/#user>`__ instruction, unless you want the group to be ``root``
-  Set `WORKDIR <https://docs.docker.com/engine/reference/builder/#workdir>`__ to ``/workdir``:

   .. code-block:: docker

      WORKDIR /workdir

-  Use a leading ``/`` with the ``WORKDIR`` instruction
-  Use the ``--chown=user:group`` option with the `COPY <https://docs.docker.com/engine/reference/builder/#copy>`__ instruction, unless you want the ownership of the files to be ``root:root``
-  Prefer the ``COPY`` instruction to the `ADD <https://docs.docker.com/engine/reference/builder/#add>`__ instruction, `as recommended <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy>`__

Reference:

-  `Dockerfile reference <https://docs.docker.com/engine/reference/builder/>`__
-  Best practices for `Dockerfile instructions <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#dockerfile-instructions>`__

Instruction order
-----------------

To `leverage the build cache <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache>`__, order the instructions from least-to-most likely to change over time. In general, the order is:

#. Declare the base image
#. Install system packages
#. Copy requirements files
#. Install project dependencies
#. Create a non-root user †
#. Set the working directory †
#. Switch to the non-root user †
#. Copy project files

† For different languages, the instructions about the non-root user and working directory might appear in a different order.

Base images
-----------

For Python, use the default image, `as recommended <https://hub.docker.com/_/python>`__, of the minor version, to ensure predictable behavior. Do not use the ``-slim`` or ``-alpine`` versions.

For Node, use the default image, `as recommended <https://hub.docker.com/_/node/>`__, of the major version. Do not use the ``-slim`` or ``-alpine`` versions.

For a web server, use the `nginxinc/nginx-unprivileged:latest <https://hub.docker.com/r/nginxinc/nginx-unprivileged>`__ image. Note that the default port is changed to 8080 (instead of 80).

For reference, the default ``/etc/nginx/conf.d/default.conf`` file in the Nginx image is:

.. literalinclude:: samples/default.conf
   :language: nginx

..
   docker pull nginxinc/nginx-unprivileged
   docker run -it --entrypoint sh nginxinc/nginx-unprivileged
   $ cat /etc/nginx/conf.d/default.conf

System packages
---------------

Before installing a system package, check whether it's included in a base image. For example, the ``psycopg2`` Python package `requires <https://www.psycopg.org/install/>`__ the ``libpq-dev`` system package. To check whether it's included, when using the `python:3.8 image <https://hub.docker.com/_/python>`__:

#. Find the tag on the DockerHub page of the base image (the ``3.8`` tag is under *Shared Tags*)
#. Click the link to view the Dockerfile
#. Check the ``apt-get install`` commands for the package name
#. If not found, look for ``FROM`` instructions
#. Repeat from step 1 for the ``FROM`` image(s)

We find that the `buildpack-deps:bullseye image <https://github.com/docker-library/buildpack-deps/blob/master/debian/bullseye/Dockerfile>`__ installs the ``libpq-dev`` system package.

If it's not included, install it following `best practices <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#apt-get>`__:

.. code-block:: docker

   RUN apt-get update && apt-get install -y --no-install-recommends \
         package-a \
         package-b \
         package-c \
      && rm -rf /var/lib/apt/lists/*

Templates
---------

.. note::

   If Dockerfiles are similar across projects, we can consider creating our own base images and using the `ONBUILD <https://docs.docker.com/engine/reference/builder/#onbuild>`__ instruction to copy source code.

Python
~~~~~~

.. literalinclude:: samples/Dockerfile_python
   :language: docker

.. seealso::

   :doc:`django`

Node
~~~~

See:

-  `Dockerising a Node.js web app <https://nodejs.org/en/docs/guides/nodejs-docker-webapp/>`__
-  `Best Practices Guide <https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md>`__
-  `Node.js Language-specific guide <https://docs.docker.com/language/nodejs/>`__
