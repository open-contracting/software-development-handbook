Django
======

General
-------

-  Delete empty, auto-generated files.

Models
------

-  Use ``help_text`` and ``verbose_name`` to describe fields.
-  Use ``TextField``, not ``CharField``. There is `no performance difference <https://www.postgresql.org/docs/11/datatype-character.html>`__ in PostgreSQL.
-  Do not use ``null=True`` with ``TextField`` or ``CharField``, as `recommended by Django <https://docs.djangoproject.com/en/3.2/ref/models/fields/#null>`__. 

Forms
-----

-  Use ``help_text`` and ``label`` to describe fields.

Admin
-----

-  Configure list views for easy of use using ``list_display``, ``list_editable``, ``list_filter``
-  Configure ``fieldsets`` (or ``fields`` if there are only a few) to group and order fields logically
-  Configure ``readonly_fields``, so that the administrator knows whether to edit a field

Templates
---------

In many cases, you can achieve the same outcome using either `context processors <https://docs.djangoproject.com/en/3.2/ref/templates/api/#writing-your-own-context-processors>`__ or `inclusion tags <https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags>`__. If the variables that the template uses are constant (e.g. from a Django settings file), use a context processor. Otherwise, use an inclusion tag.

Settings
--------

Use a single `Django settings file <https://docs.djangoproject.com/en/3.2/topics/settings/>`__, in which values are read from environment variables, and in which the default values are appropriate for all developers. In production, a `uWSGI INI file <https://github.com/open-contracting/deploy/blob/main/salt/uwsgi/files/django.ini>`__ or a `Docker Compose .env file <https://docs.docker.com/compose/environment-variables/>`__ can override these values. In testing, a GitHub Actions workflow can override these values.

Use this template:

.. code-block:: python

   TODO

Generate a default ``SECRET_KEY`` value:

.. code-block:: bash

   python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

Add `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ to your :ref:`requirements file<application-requirements>`, and refer to its documentation.

Deployment
----------

-  Use the `Deployment checklist <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/>`__

.. _django-performance:

Performance
-----------

-  `Performance and optimization <https://docs.djangoproject.com/en/3.2/topics/performance/>`__
-  `Database access optimization <https://docs.djangoproject.com/en/3.2/topics/db/optimization/>`__
-  Deployment checklist: `Performance optimizations <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#performance-optimizations>`__

Reference
---------

-  `The Django admin site <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/>`__
-  `Deploying Django <https://docs.djangoproject.com/en/3.2/howto/deployment/>`__
