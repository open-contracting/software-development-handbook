Directory layout
================

A first step of a new project is to define its directory layout.

Applications
------------

Applications should follow the layout of the framework, like `Django <https://docs.djangoproject.com/en/4.2/intro/tutorial01/>`__, `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#default-structure-of-scrapy-projects>`__ or `FastAPI <https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure>`__, and should use its command for generating the layout, like `django-admin startproject <https://docs.djangoproject.com/en/4.2/ref/django-admin/#startproject>`__ and `django-admin startapp <https://docs.djangoproject.com/en/4.2/ref/django-admin/#startapp>`__.

.. tip::

   Commit the generated files before making changes, so that the changes appear in the history.

If no framework is used, prefer a smaller number of directories, like in `Kingfisher Summarize <https://github.com/open-contracting/kingfisher-summarize>`__ or `Pelican backend <https://github.com/open-contracting/pelican-backend>`__. Components should be logically distinct units, like `apps <https://docs.djangoproject.com/en/4.2/ref/applications/>`__ in Django. For example:

.. code-block:: none

   ├── PROJECTNAME
   │   ├── migrations
   │   └── static
   ├── COMPONENT1
   ├── COMPONENT2
   ├── docs
   └── tests
       └── fixtures

If the frontend is a single-page application (SPA), add it as a ``frontend/`` directory. Do not create a separate repository unless the frontend and backend are decoupled.

.. seealso::

   :ref:`Django directory layout guide<django-layout>`

.. _layout-packages:

Packages
--------

:doc:`packages` should follow this layout, where ``PACKAGENAME`` is the name of the package:

.. code-block:: none

   ├── PACKAGENAME
   │   ├── __init__.py
   │   ├── __main__.py
   │   ├── commands
   │   └── static
   ├── docs
   └── tests
       └── fixtures

.. note::

   ``__main__.py`` is `executed <https://docs.python.org/3/library/__main__.html#main-py-in-python-packages>`__ when the package is invoked directly from the command line using the ``-m`` flag. For example:

   .. code-block:: bash

      python -m ocdskit

.. note::

   We don't use the `src/ layout <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure>`__ (`more <https://blog.ionelmc.ro/2015/02/24/the-problem-with-packaging-in-python/>`__). In practice, we rarely encounter the problems it solves, and our use of :ref:`check-manifest<python-package-release-process>` and `test_requirements.py <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/tests/test_requirements.py>`__ guard against those problems.

Modules
-------

-  Use a single module for all models.
-  If a module defines names that are imported by only one other module, merge the modules unless:

   - It is a convention of a framework (for example, the files created by Django's `startapp <https://docs.djangoproject.com/en/4.2/intro/tutorial01/#creating-the-polls-app>`__ command).
   - There is a divide in terms of responsibility (for example, model and view).

-  Don't split a module only to reduce its length.

.. seealso::

   -  :ref:`fat-models`
   -  `FastAPI documentation <https://sqlmodel.tiangolo.com/tutorial/code-structure/#single-module-for-models>`__

.. _layout-tests:

Test files
----------

-  Put `tests outside application code <https://docs.pytest.org/en/latest/explanation/goodpractices.html#choosing-a-test-layout-import-rules>`__. Do not add ``tests`` directories inside application code.
-  Prefix filenames with ``test_``. Do not suffix basenames with ``_test``.

Static files
------------

-  Don't mix static files with Python files in the same directory.

Filename conventions
--------------------

-  ``util`` for a generic module of helper functions, not ``utils``, ``tools`` or ``helper``.
-  ``exceptions`` for a generic module of exception classes, not ``errors``.
-  Use verbs for commands (like ``add_files.py``).
-  Use nouns for workers (like ``checker.py``).

   .. note::

      Verbs may be used for workers if they aren't mixed with commands.
