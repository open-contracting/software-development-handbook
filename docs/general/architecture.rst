Architecture
============

.. note::

   This page is a stub.

Monoliths
---------

At present:

-  Each of our services can run on a single server.
-  A service has at most 2 repositories: backend and frontend, excluding non-service dependencies.
-  A service's codebase has at most 3000 relevant lines, according to `Coveralls <https://coveralls.io>`__.
-  A service's Docker Compose file defines the containers for the backend, frontend and any workers.

When using :doc:`../python/django`, the workers are written as Django `management commands <https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/>`__. In other cases, the workers are written as Click commands, sharing code with other commands.

In other words, **nothing is a microservice**, where a `microservice <https://en.wikipedia.org/wiki/Microservices>`__ means a sub-service that is developed and deployed *independently* of others, as part of a service.

Instead, we achieve loose coupling and proper encapsulation by other means: dividing program logic by UI responsibility (e.g. :ref:`model-template-view`); organizing a set of features into an `application <https://docs.djangoproject.com/en/4.2/ref/applications/#projects-and-applications>`__, when using Django; and otherwise organizing code carefully.

.. _fat-models:

Fat models
----------

If a function performs `CRUD operations <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`__ and accepts only a database session and instance values as arguments, add this function as a method on the model's class.

`Code smells <https://en.wikipedia.org/wiki/Code_smell>`__ for skinny models:

-  Calling database session methods outside a model's class (for example, ``COMMIT``)
