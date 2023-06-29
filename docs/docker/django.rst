Dockerfile for Django
=====================

Add one Dockerfile for the Django project, replacing ``core.wsgi`` if needed and ``{{ cookiecutter.project_slug }}``, and another for static files.

.. warning::

   When deploying Docker, remember to set the number of workers using a environment variable like ``GUNICORN_CMD_ARGS="--workers 3"``.

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/Dockerfile_django
   :language: docker
   :caption: Dockerfile_django

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/Dockerfile_static
   :language: docker
   :caption: Dockerfile_static

.. _gunicorn:

Gunicorn
--------

Worker class
~~~~~~~~~~~~

Gunicorn describes use cases where asynchronous workers `are preferred <https://docs.gunicorn.org/en/stable/design.html#choosing-a-worker-type>`__. In particular, check whether the application makes long blocking calls and is therefore `I/O bound <https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7>`__.

.. note::

   If Gunicorn is deployed `behind a proxy server <https://docs.gunicorn.org/en/stable/deploy.html>`__, like Apache, then it isn't "serving requests directly to the internet." That said, check whether other applications that send requests behind the proxy server are likely to DOS the application (if it were to use a synchronous worker).

If not, then the synchronous `worker classes <https://docs.gunicorn.org/en/stable/settings.html#worker-class>`__ (``sync`` and ``gthreads``) are preferred.

.. note::

   The ``gthreads`` worker class is synchronous, `despite <https://github.com/benoitc/gunicorn/issues/1493#issuecomment-321461614>`__ appearing under `AsyncIO Workers <https://docs.gunicorn.org/en/stable/design.html#asyncio-workers>`__.

When using the ``sync`` worker class, the `\--timeout option <https://docs.gunicorn.org/en/stable/settings.html#timeout>`__ `behaves like a request timeout <https://github.com/benoitc/gunicorn/issues/1493#issuecomment-321331753>`__, because the worker can only *either* handle the request or handle the heartbeat. (Gunicorn otherwise has no option like uWSGI's `harakiri <https://uwsgi-docs.readthedocs.io/en/latest/Glossary.html#term-harakiri>`__ for `request timeouts <https://github.com/benoitc/gunicorn/issues/1658>`__.)

When using the ``gthreads`` worker class, a main thread `handles the heartbeat <https://docs.gunicorn.org/en/stable/design.html#how-many-threads>`__. As such, we use the ``gthreads`` worker class, to not have to worry about request timeouts.

.. note::

   Setting the `\--threads <https://docs.gunicorn.org/en/stable/settings.html#threads>`__ option to more than ``1`` automatically sets the worker class to ``gthreads``.

Number of threads
~~~~~~~~~~~~~~~~~

Ensure your code is thread safe. Notably, `psycopg2 cursors are not thread safe <https://www.psycopg.org/docs/cursor.html>`__, though this isn't a concern for typical usage of `Django <https://docs.djangoproject.com/en/4.2/ref/databases/>`__.

`When using threads <https://docs.gunicorn.org/en/stable/design.html#how-many-threads>`__, the application is loaded by the worker and some memory is shared between its threads (thus consuming less memory than additional workers would).

Unless the server becomes memory-bound, use a minimum number of threads (``2``) and instead increase the number of workers, to lower the risk around thread safety.

.. note::

   If the application is CPU-bound, additional threads don't help, due to `Python's GIL <https://wiki.python.org/moin/GlobalInterpreterLock>`__. Instead, add additional workers (up to twice the number of cores).

Concurrency
~~~~~~~~~~~

`cores * 2 + 1 <https://docs.gunicorn.org/en/stable/design.html#how-many-workers>`__ is the recommended number of `workers + threads <https://github.com/benoitc/gunicorn/issues/1045#issuecomment-269575459>`__. However, multiple applications on the same server need to share the same cores – plus, the server might not be dedicated to Gunicorn.

At build time, the mix of applications and number of cores are unknown. As such, we omit the ``--workers`` option (`highest level of precedence  <https://docs.gunicorn.org/en/stable/configure.html#configuration-overview>`__), and set a `WEB_CONCURRENCY <https://docs.gunicorn.org/en/stable/settings.html#workers>`__ environment variable (lowest level). Docker Compose can then set a `GUNICORN_CMD_ARGS="\--workers 3" <https://docs.gunicorn.org/en/stable/settings.html>`__ environment variable to override the number of workers.

The template sets ``WEB_CONCURRENCY=2`` and ``--threads 2`` (as described in the previous section), such that the total concurrency is 4 – one more than ``cores * 2 + 1`` for a single core.

Signals
~~~~~~~

The shell form, ``CMD command param1``, `runs the command as a subcommand <https://docs.docker.com/engine/reference/builder/#cmd>`__ of ``/bin/sh -c``, which `doesn't pass signals <https://docs.docker.com/engine/reference/builder/#entrypoint>`__. For Gunicorn to receive the ``SIGTERM`` signal and stop gracefully, the exec form, ``CMD ["command", "param1"]``, is used.

Reference: `Signal Handling <https://docs.gunicorn.org/en/stable/signals.html>`__

Other options
~~~~~~~~~~~~~

``--bind 0.0.0.0:8000`` uses Docker's `default bind address for containers <https://docs.docker.com/network/packet-filtering-firewalls/#setting-the-default-bind-address-for-containers>`__ and Gunicorn's `default port <https://docs.gunicorn.org/en/stable/settings.html#bind>`__.

``--worker-tmp-dir /dev/shm`` avoids a `potential issue <https://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod>`__.

``--name PROJECTNAME`` helps to `distinguish processes <https://docs.gunicorn.org/en/stable/faq.html#how-can-i-name-processes>`__ of different applications on the same server.

Additional options can be configured from Docker Compose using the `GUNICORN_CMD_ARGS <https://docs.gunicorn.org/en/stable/settings.html>`__ environment variable, though command-line arguments `take precedence <https://docs.gunicorn.org/en/stable/configure.html#configuration-overview>`__.

Troubleshooting
~~~~~~~~~~~~~~~

Idle workers are regularly killed. As such, it can be hard to debug what happened. See this `FAQ question <https://docs.gunicorn.org/en/stable/faq.html#why-are-workers-silently-killed>`__ for some guidance.
