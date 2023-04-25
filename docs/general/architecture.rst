Architecture
============

.. note::

   This page is a stub.

Monoliths
---------

At present:

-  Each of our services can run on a single server.
-  Each service has at most two repositories: backend and frontend, excluding non-service dependencies.
-  Each service's codebase has at most 3000 relevant lines, according to `Coveralls <https://coveralls.io>`__.
-  Each service's Docker Compose file defines the containers for the backend, frontend and workers (if any).

When using :doc:`../python/django`, the workers are written as Django `management commands <https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/>`__. In other cases, the workers are written as Click commands, sharing code with other commands.

In other words, **nothing is a microservice**, where a `microservice <https://en.wikipedia.org/wiki/Microservices>`__ means a sub-service that is developed and deployed *independently* of others, as part of a service.

Instead, we achieve loose coupling and proper encapsulation by other means: dividing program logic by UI responsibility (e.g. :ref`model-template-view`); organizing a set of features into an `application <https://docs.djangoproject.com/en/4.2/ref/applications/#projects-and-applications>`__, when using Django; and otherwise organizing code carefully.
