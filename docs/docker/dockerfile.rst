Dockerfile
==========

Dockerfile instructions
-----------------------

Reference: `Dockerfile reference <https://docs.docker.com/engine/reference/builder/>`__, Best practices for `Dockerfile instructions <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#dockerfile-instructions>`__

USER
~~~~

-  Use the ``user:group`` form for the `USER <https://docs.docker.com/engine/reference/builder/#user>`__ instruction, unless you want the group to be ``root``.
-  Use the name ``runner`` for the `non-root user <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user>`__:

   .. code-block:: docker

      RUN groupadd -r runner && useradd --no-log-init -r -g runner runner

WORKDIR
~~~~~~~

-  Use a leading ``/`` with the ``WORKDIR`` instruction.
-  Set `WORKDIR <https://docs.docker.com/engine/reference/builder/#workdir>`__ to ``/workdir``:

   .. code-block:: docker

      WORKDIR /workdir

COPY
~~~~

-  Use the ``--chown=user:group`` option with the `COPY <https://docs.docker.com/engine/reference/builder/#copy>`__ instruction, unless you want the ownership of the files to be ``root:root``.
-  Prefer the ``COPY`` instruction to the `ADD <https://docs.docker.com/engine/reference/builder/#add>`__ instruction, `as recommended <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy>`__.

Layer order
-----------

To `leverage the build cache <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache>`__, order the instructions from least-to-most likely to change over time. In general, the order is:

#. Declare the base image
#. Install system packages
#. Create a non-root user
#. Copy requirements files
#. Install project dependencies
#. Set the working directory
#. Switch to the non-root user
#. Copy project files

.. note::

   For Node, set the working directory before copying requirements files.

.. important::

   For Node, install project dependencies safely with:

   .. code-block:: docker

      RUN npm ci --ignore-scripts

Base images
-----------

For Python, use the default image, `as recommended <https://hub.docker.com/_/python>`__, of the minor version, to ensure predictable behavior. Do not use the ``-slim`` or ``-alpine`` versions.

For Node, use the default image, `as recommended <https://hub.docker.com/_/node/>`__, of the major version. Do not use the ``-slim`` or ``-alpine`` versions.

For a web server, use the `nginxinc/nginx-unprivileged:latest <https://hub.docker.com/r/nginxinc/nginx-unprivileged>`__ image. Note that the default port is changed to 8080 (instead of 80).

Set ``server_tokens off;`` to prevent false positives from penetration tests (Ubuntu backports security patches, without changing version numbers).

.. note::

   For reference, the default ``/etc/nginx/conf.d/default.conf`` file in the Nginx image is:

   .. literalinclude:: samples/default.conf
      :language: nginx

   ..
      To update the samples/default.conf file:

      docker pull nginxinc/nginx-unprivileged
      docker run -it --entrypoint sh nginxinc/nginx-unprivileged
      $ cat /etc/nginx/conf.d/default.conf

.. seealso::

   `nginx playground <https://nginx-playground.wizardzines.com>`__

System packages
---------------

Before installing a system package, check whether it's included in a base image. For example, the ``psycopg2`` Python package `requires <https://www.psycopg.org/install/>`__ the ``libpq-dev`` system package. To check whether it's included, when using the `python:3.10 image <https://hub.docker.com/_/python>`__:

#. Find the tag on the DockerHub page of the base image (the ``3.10`` tag is under *Shared Tags*)
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

Bind mounts
-----------

.. note::

   In general, do not use absolute paths on the host's filesystem as an API between projects, because the projects might not share the same filesystem, like in the case of Docker containers. Instead, use paths relative to a configurable setting.

If a project needs to read or write data to the filesystem:

#. Add a setting with a default value. For example, for a :ref:`Django project<django-settings>`:

   .. code-block:: python
      :caption: settings.py

      KINGFISHER_COLLECT_FILES_STORE = os.getenv(
          "KINGFISHER_COLLECT_FILES_STORE", "/data" if production else BASE_DIR / "data"
      )

#. Create the directory using the default value in the Dockerfile. For example:

   .. code-block:: docker
      :caption: Dockerfile

      # Must match the settings.KINGFISHER_COLLECT_FILES_STORE default value.
      RUN mkdir -p /data

#. `Mount <https://docs.docker.com/storage/bind-mounts/>`__ the host's directory to the default value in the Docker Compose file. For example:

   .. code-block:: yaml
      :caption: docker-compose.yaml

      services:
        django:
          volumes:
            - /data/storage/kingfisher-collect:/data

If a project needs to read or write data to multiple directories, set the default values to subdirectories of the ``/data`` directory.

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
