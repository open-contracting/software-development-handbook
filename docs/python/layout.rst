Directory layout
================

The first step of a new project is to define its directory layout.

Applications
------------

Applications should follow the layout of the framework used, like `Django <https://docs.djangoproject.com/en/3.2/intro/tutorial01/>`__ or `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#default-structure-of-scrapy-projects>`__, and should use its command for generating the layout, like `django-admin startproject <https://docs.djangoproject.com/en/3.2/ref/django-admin/#startproject>`__ and `django-admin startapp <https://docs.djangoproject.com/en/3.2/ref/django-admin/#startapp>`__. If no framework is used, prefer a smaller number of directories, like in `Kingfisher Summarize <https://github.com/open-contracting/kingfisher-summarize>`__ or `Pelican backend <https://github.com/open-contracting/pelican-backend>`__. For example:

.. code-block:: none

   ├── PROJECTNAME
   │   ├── migrations
   │   └── static
   ├── COMPONENT1
   ├── COMPONENT2
   ├── docs
   └── tests
       └── fixtures

Components should be logically distinct units, like `apps <https://docs.djangoproject.com/en/3.2/ref/applications/>`__ in Django.

.. _layout-packages:

Packages
--------

:doc:`packages` should follow this layout, where ``PACKAGENAME`` is the name of the package:

.. code-block:: none

   ├── PACKAGENAME
   │   └── static
   ├── docs
   └── tests
       └── fixtures

.. note::

   We don't use the `src/ layout <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure>`__. Although a `single blog post <https://blog.ionelmc.ro/2015/02/24/the-problem-with-packaging-in-python/>`__ and a few passionate developers have popularized the idea, in practice, we rarely encounter the problems it solves, and our use of :ref:`check-manifest<python-package-release-process>` and `test_requirements.py <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/tests/test_requirements.py>`__ guard against those problems.

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
-  Use verbs for commands (like ``add_files.py``).
-  Use nouns for workers (like ``checker.py``).

   .. note::

      Verbs may be used for workers if they aren't mixed with commands.
