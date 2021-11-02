Docker
======

.. seealso::

   For deploying Docker, see the  `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/docker.html>`__.

To simplify the :ref:`GitHub Actions workflow<docker-registry>`, put the :ref:`dockerfile` and :ref:`dockerignore` files in the root of the repository.

.. _dockerfile:

Dockerfile
----------

To increase consistency across projects:

-  Set the `non-root user <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user>`__ to ``runner``

   .. code-block:: none

      RUN groupadd -r runner && useradd --no-log-init -r -g runner runner

-  Set `WORKDIR <https://docs.docker.com/engine/reference/builder/#workdir>`__ to ``/workdir``

   .. code-block:: none

      WORKDIR /workdir

Instruction order
~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~

For Python, use the default image, `as recommended <https://hub.docker.com/_/python>`__, of the minor version, to ensure predictable behavior. Do not use the ``-slim`` or ``-alpine`` versions.

For Node, use the default image, `as recommended <https://hub.docker.com/_/node/>`__, of the major version. Do not use the ``-slim`` or ``-alpine`` versions.

For a web server, use the `nginxinc/nginx-unprivileged:latest <https://hub.docker.com/r/nginxinc/nginx-unprivileged>`__ image. Note that the default port is changed to 8080 (instead of 80).

System packages
~~~~~~~~~~~~~~~

Before installing a system package, check whether it's included in a base image. For example, the ``psycopg2`` Python package `requires <https://www.psycopg.org/install/>`__ the ``libpq-dev`` system package. To check whether it's included, when using the `python:3.8 image <https://hub.docker.com/_/python>`__:

#. Find the tag on the DockerHub page of the base image (the ``3.8`` tag is under *Shared Tags*)
#. Click the link to view the Dockerfile
#. Check the ``apt-get install`` commands
#. Look for ``FROM`` instructions
#. Repeat steps 1-3 for the ``FROM`` image(s)

In this example, we find that the `buildpack-deps:bullseye image <https://github.com/docker-library/buildpack-deps/blob/master/debian/bullseye/Dockerfile>`__ installs the ``libpq-dev`` system package.

If it's not included, install it following `best practices <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#apt-get>`__:

.. code-block:: none

   RUN apt-get update && apt-get install -y --no-install-recommends \
         package-a \
         package-b \
         package-c \
      && rm -rf /var/lib/apt/lists/*

Templates
~~~~~~~~~

Python
^^^^^^

.. literalinclude:: samples/Dockerfile_python
   :language: none

Node
^^^^

See:

-  `Dockerising a Node.js web app <https://nodejs.org/en/docs/guides/nodejs-docker-webapp/>`__
-  `Best Practices Guide <https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md>`__

.. _dockerignore:

.dockerignore
-------------

The `.dockerignore <https://docs.docker.com/engine/reference/builder/#dockerignore-file> file`__ should only ignore tracked files (not files like ``.DS_Store`` or directories like ``__pycache__``), unless the build generates untracked files (like ``node_modules``).

.. literalinclude:: samples/dockerignore
   :language: none

.. _docker-registry:

Docker registry
---------------

In most cases, you can add the job below to an existing :ref:`.github/workflows/ci.yml<continuous-integration>` file. If you need to build multiple images, then for each image:

#. Include a ``docker/build-push-action`` step.
#. Set either the path to the Dockerfile with the `file <https://github.com/docker/build-push-action#inputs>`__ key or the path to the directory (`context <https://docs.docker.com/engine/context/working-with-contexts/>`__) with the ``context`` key.
#. Add a suffix to the repository name under the ``tags`` key.

.. literalinclude:: samples/ci.yml
   :language: none

.. note::

   The `docker/build-push-action <https://github.com/docker/build-push-action>`__ step uses `BuildKit <https://docs.docker.com/engine/reference/builder/#buildkit>`__ by default.

..

   The following would simplify the workflow somewhat. However, it would not work when building multiple images, producing an inconsistent approach across repositories.

      # https://github.com/docker/metadata-action#usage
      - uses: docker/metadata-action@v3
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=tag
      # https://github.com/docker/build-push-action#usage
      - uses: docker/build-push-action@v2
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

    Note: The docker/metadata-action step with ``type=ref,event=tag`` automatically generates the `latest <https://github.com/docker/metadata-action#latest-tag>`__ tag.

Reference
~~~~~~~~~

-  `Publishing a package using an action <https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions>`__
-  `Troubleshooting <https://github.com/docker/build-push-action/blob/master/TROUBLESHOOTING.md>`__ ``docker/build-push-action`` step
