Docker
======

.. seealso::

   For deploying Docker, see the  `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/docker.html>`__. Do not put ``docker-compose.yaml`` or ``.env`` files in repositories.

Directory layout
----------------

To simplify the :ref:`GitHub Actions workflow<docker-registry>`, put the :ref:`dockerfile` and :ref:`dockerignore` files in the root of the repository.

.. _dockerfile:

Dockerfile
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

For reference, the default ``/etc/nginx/conf.d/default.conf`` file in the Nginx image is:

.. literalinclude:: samples/default.conf
   :language: nginx

..
   docker pull nginxinc/nginx-unprivileged
   docker run -it --entrypoint sh nginxinc/nginx-unprivileged
   $ cat /etc/nginx/conf.d/default.conf

System packages
~~~~~~~~~~~~~~~

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
~~~~~~~~~

.. note::

   If Dockerfiles are similar across projects, we can consider creating our own base images and using the `ONBUILD <https://docs.docker.com/engine/reference/builder/#onbuild>`__ instruction to copy source code.

Python
^^^^^^

.. literalinclude:: samples/Dockerfile_python
   :language: docker

.. _docker-django:

Django
^^^^^^

Add one Dockerfile for the Django project, replacing ``core.wsgi`` if needed and ``PROJECTNAME``, and another for static files.

.. warning::

   Remember to set the number of workers using a environment variable like ``GUNICORN_CMD_ARGS="--workers 3"``.

.. literalinclude:: samples/Dockerfile_django
   :language: docker
   :caption: Dockerfile_django

.. literalinclude:: samples/Dockerfile_static
   :language: docker
   :caption: Dockerfile_static

.. _gunicorn:

.. admonition:: Gunicorn

   Gunicorn's options require explanation.

   **Worker class**

   Gunicorn describes use cases where asynchronous workers `are preferred <https://docs.gunicorn.org/en/stable/design.html#choosing-a-worker-type>`__. In particular, check whether the application makes long blocking calls and is therefore `I/O bound <https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7>`__.

   .. note::

      If Gunicorn is deployed `behind a proxy server <https://docs.gunicorn.org/en/stable/deploy.html>`__, like Apache, then it isn't "serving requests directly to the internet." That said, check whether other applications running on the same server and sending requests behind the proxy server are likely to DOS the application if it were to use a synchronous worker.

   If not, then the synchronous `worker classes <https://docs.gunicorn.org/en/stable/settings.html#worker-class>`__ (``sync`` and ``gthreads``) are preferred.

   .. note::

      The ``gthreads`` worker class is synchronous, `despite <https://github.com/benoitc/gunicorn/issues/1493#issuecomment-321461614>`__ appearing under `AsyncIO Workers <https://docs.gunicorn.org/en/stable/design.html#asyncio-workers>`__.

   When using the ``sync`` worker class, the `--timeout option <https://docs.gunicorn.org/en/stable/settings.html#timeout>`__ `behaves like a request timeout <https://github.com/benoitc/gunicorn/issues/1493#issuecomment-321331753>`__, because it can only *either* handle the request or handle the heartbeat. When using the ``gthreads`` worker class, a main thread `handles the heartbeat <https://docs.gunicorn.org/en/stable/design.html#how-many-threads>`__. As such, we use the ``gthreads`` worker class, to not have to worry about request times.

   .. note::

      Setting the `--threads <https://docs.gunicorn.org/en/stable/settings.html#threads>`__ option to more than ``1`` automatically sets the worker class to ``gthreads``.

   **Number of threads**

   Check whether your code is thread safe. Notably, `psycopg2 cursors are not thread safe <https://www.psycopg.org/docs/cursor.html>`__, though this isn't a concern for typical usage of `Django <https://docs.djangoproject.com/en/3.2/ref/databases/>`__.

   `When using threads <https://docs.gunicorn.org/en/stable/design.html#how-many-threads>`__, the application is loaded by the worker and some memory is shared between its threads (thus also consuming less memory than additional workers would).

   Unless the server becomes memory-bound, use a minimum number of threads (``2``) and instead increase the number of workers, to lower the risk around thread safety.

   .. note::

      If the application is CPU-bound, additional threads don't help, due to `Python's GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__. Instead, add additional workers (up to twice the number of cores).

   **Concurrency**

   `cores * 2 + 1 <https://docs.gunicorn.org/en/stable/design.html#how-many-workers>`__ is the recommended number of workers plus threads. However, multiple applications on the same server need to share the same cores – plus, the server might not be dedicated to Gunicorn. At build time, the mix of applications is unknown.

   As such, we omit the ``--workers`` option (`highest level of precedence  <https://docs.gunicorn.org/en/stable/configure.html#configuration-overview>`__), and set a `WEB_CONCURRENCY <https://docs.gunicorn.org/en/stable/settings.html#workers>`__ environment variable (lowest level of precedence). Docker Compose can then set a `GUNICORN_CMD_ARGS="--workers 3" <https://docs.gunicorn.org/en/stable/settings.html>`__ environment variable to override the number of workers.

   ``WEB_CONCURRENCY`` is set to ``cores + 1``, where the `nproc <https://www.gnu.org/software/coreutils/manual/html_node/nproc-invocation.html>`__ command returns the number of processors. ``--threads 2`` is set as above, such that the total concurrency is ``cores * 2 + 2`` – one more than recommended.

   **Signals**

   The shell form, ``CMD command param1``, `runs the command as a subcommand <https://docs.docker.com/engine/reference/builder/#cmd>`__ of ``/bin/sh -c``, which `doesn't pass signals <https://docs.docker.com/engine/reference/builder/#entrypoint>`__. For Gunicorn to receive the ``SIGTERM`` signal and stop gracefully, the exec form is used.

   Reference: Gunicorn `signal handling <https://docs.gunicorn.org/en/stable/signals.html>`__

   **Other options**

   ``--bind 0.0.0.0:8000`` uses Docker's `default bind address for containers <https://docs.docker.com/network/iptables/#setting-the-default-bind-address-for-containers>`__ and Gunicorn's `default port <https://docs.gunicorn.org/en/stable/settings.html#bind>`__.

   ``--worker-tmp-dir /dev/shm`` avoids a `potential issue <https://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod>`__.

   ``--name PROJECTNAME`` helps to `distinguish processes <https://docs.gunicorn.org/en/stable/faq.html#how-can-i-name-processes>`__ of different applications on the same server.

   Additional options can be configured from Docker Compose using the `GUNICORN_CMD_ARGS <https://docs.gunicorn.org/en/stable/settings.html>`__ environment variable, though command-line arguments `take precedence <https://docs.gunicorn.org/en/stable/configure.html#configuration-overview>`__.

   **Troubleshooting**

   Idle workers are regularly killed. As such, it can be hard to debug what happened. See this `FAQ question <https://docs.gunicorn.org/en/stable/faq.html#why-are-workers-silently-killed>`__ for some guidance.

Node
^^^^

See:

-  `Dockerising a Node.js web app <https://nodejs.org/en/docs/guides/nodejs-docker-webapp/>`__
-  `Best Practices Guide <https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md>`__
-  `Node.js Language-specific guide <https://docs.docker.com/language/nodejs/>`__

.. _dockerignore:

.dockerignore
-------------

The `.dockerignore <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`__ file should only ignore tracked files (not files like ``.DS_Store`` or directories like ``__pycache__``), unless the build generates untracked files (like ``node_modules``).

.. literalinclude:: samples/dockerignore
   :language: none

To check the contents of the image, you can run, replacing ``IMAGE``:

.. code-block:: bash

   docker run -it --entrypoint sh IMAGE

.. _docker-registry:

Docker registry
---------------

In most cases, you can add the job below to an existing :doc:`.github/workflows/ci.yml<../python/ci>` file.

If you need to build multiple images, then for each image:

#. Include a ``docker/build-push-action`` step.
#. Set either:

   -  The path to the Dockerfile with the `file <https://github.com/docker/build-push-action#inputs>`__ key
   -  The path to the directory (`context <https://docs.docker.com/engine/context/working-with-contexts/>`__) with the ``context`` key

#. Add a suffix to the repository name under the ``tags`` key.

.. literalinclude:: samples/ci.yml
   :language: yaml

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
