Django
======

1. Use the Django Cookiecutter template:

.. code-block:: bash

   uv tool install cookiecutter
   cookiecutter gh:open-contracting/software-development-handbook --directory cookiecutter-django

   uv venv
   uv pip sync requirements_dev.txt

   uv tool install pre-commit
   pre-commit install

1. `Add the repository to pre-commit.ci <https://github.com/organizations/open-contracting/settings/installations/20658712>`__
1. Add the repository to the `Robots <https://github.com/orgs/open-contracting/teams/robots/repositories>`__ team, and set the *Permission level* to "Admin" (for the ``stefanzweifel/git-auto-commit-action`` action in the :ref:`lint workflow<linting-ci>`).

.. _django-layout:

Directory layout
----------------

-  Maintain the distinction between app directories and the project directory.
-  Organize apps into logical units. Don't mix everything into one app.
-  Do not nest app directories within the project directory. (While this avoids errors due to app names colliding with package names, it tends to produce a worse separation of concerns.)
-  Delete empty files auto-generated by ``python manage.py startapp``.

.. seealso::

   :doc:`Directory layout guide<layout>`

Filename conventions
~~~~~~~~~~~~~~~~~~~~

-  Use ``core`` as the project name.
-  Use *either* nouns (like ``exporter``) or verbs (like ``export``) for apps. Don't use both.

.. cookiecutter-django uses ``config`` as the project name, but a ``config.settings`` module is mind-bending.

.. _model-template-view:

Model Template View
-------------------

The view should interact with the :ref:`models<django-models>` and return a context for the :ref:`template<django-templates>`, based on the request.

-  A view is concerned with fulfilling the request. Add new methods to models for complex or repeated processing, instead of putting that logic in the view.
-  A template is concerned with formatting the context provided by the view. Use `custom template tags and filters <https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/>`__ for complex or repeated formatting, instead of putting that logic in the view.
-  A template should not perform user-based logic, like filtering which model instances to display. Instead, use a `custom manager <https://docs.djangoproject.com/en/4.2/topics/db/managers/>`__ (or `custom queryset <https://docs.djangoproject.com/en/4.2/topics/db/managers/#creating-a-manager-with-queryset-methods>`__).
-  A model should not concern itself with other models' objects or with the filesystem.

URLs
----

-  Use hyphens as separators in paths.
-  Use hyphens as separators in `named URL patterns <https://docs.djangoproject.com/en/4.2/topics/http/urls/#naming-url-patterns>`__.
-  Use `Django REST Framework <https://www.django-rest-framework.org>`__, instead of writing endpoints by hand. (See :doc:`preferences`.)

.. _django-sitemap:

Sitemap
~~~~~~~

Public sites should serve a ``sitemap.xml`` file.

-  Do not set ``changefreq`` or ``priority``. (`"Google ignores priority and changefreq values." <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap>`__)
-  Do not use ``django.contrib.sitemaps.ping_google()``. (`"Sitemaps ping endpoint is going away." <https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping>`__)

.. _django-models:

Models
------

-  Use ``from django.db import models``, `per convention <https://docs.djangoproject.com/en/4.2/ref/models/fields/>`__.
-  Use ``help_text`` and ``verbose_name`` to describe fields.
-  Use ``TextField``, not ``CharField``. There is `no performance difference <https://www.postgresql.org/docs/current/datatype-character.html>`__ in PostgreSQL.
-  Do not use ``JSONField``, unless the field is intended to store:

   -  JSON text from another application (like data from an OCDS publication).
   -  Configuration values for another application (to avoid migrations caused by changes in other applications).

-  Do not use ``null=True`` with ``TextField`` or ``CharField``, `as recommended <https://docs.djangoproject.com/en/4.2/ref/models/fields/#null>`__.
-  Do not use ``null=True`` with ``JSONField``, if possible. Instead, use ``default=dict``, ``default=list`` or  ``default=""``.
-  Use ``Meta.indexes``, not ``db_index=True``, with ``ForeignKey``, `as recommended <https://docs.djangoproject.com/en/4.2/ref/models/fields/#db-index>`__.
-  Use the `pk property <https://docs.djangoproject.com/en/4.2/ref/models/instances/#the-pk-property>`__ and the `pk lookup shortcut <https://docs.djangoproject.com/en/4.2/topics/db/queries/#the-pk-lookup-shortcut>`__ instead of ``id``.
-  The table related to a ``ManyToManyField`` field is not visible to the Django ORM. If you need to operate on it, create an explicit model with foreign keys to the other models, instead of operating on it via the other models.

.. seealso::

   -  `Model field reference <https://docs.djangoproject.com/en/4.2/ref/models/fields/>`__
   -  `Model instance reference <https://docs.djangoproject.com/en/4.2/ref/models/instances/>`__
   -  `Model index reference <https://docs.djangoproject.com/en/4.2/ref/models/indexes/>`__
   -  `Constraints reference <https://docs.djangoproject.com/en/4.2/ref/models/constraints/>`__

Forms
-----

-  Use ``help_text`` and ``label`` to describe fields.

Views
-----

-  Avoid setting cookies and using sessions, where possible.

   - Set the user's language in the URL path, using the `i18n_patterns function <https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns>`__.
   - Edit the `set_language <https://github.com/open-contracting/data-registry/blob/main/data_registry/i18n.py>`__ view to not use `CSRF protection <https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.csrf_exempt>`__.

.. _django-templates:

Templates
---------

.. seealso::

   :doc:`../htmlcss/index`

-  If an `inclusion tag <https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/#inclusion-tags>`__ contains no logic other than returning a context, use an `include tag <https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#include>`__ instead.
-  In many cases, you can achieve the same outcome using either `context processors <https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors>`__ or `inclusion tags <https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/#inclusion-tags>`__. If the variables that the template uses are constant (e.g. from a Django settings file), use a context processor. Otherwise, use an inclusion tag.

Admin
-----

-  Configure list views for easy of use using ``list_display``, ``list_editable``, ``list_filter``
-  Configure ``fieldsets`` (or ``fields`` if there are only a few) to group and order fields logically
-  Configure ``readonly_fields``, so that the administrator knows whether to edit a field

Management commands
-------------------

-  Use ``self.stdout`` and ``self.stderr`` to `write output <https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/>`__ for the user.

   .. note::

      If implementing a worker (i.e. daemon), use Python logging, instead.

-  Remember to add ``__init__.py`` files to the ``management`` and ``management/commands`` directories within app directories. Otherwise, their coverage won't be calculated.

.. _django-settings:

Settings
--------

To simplify the configuration of Django projects, use the :ref:`template below<django-template>` for the `settings file <https://docs.djangoproject.com/en/4.2/topics/settings/>`__.

In other modules, import settings from ``django.conf``, `as recommended <https://docs.djangoproject.com/en/4.2/topics/settings/#using-settings-in-python-code>`__:

.. code-block:: python

   from django.conf import settings

.. seealso::

   :doc:`Settings guide<settings>`, for the general approach to configuration

.. _django-env:

Environment variables
~~~~~~~~~~~~~~~~~~~~~

``DJANGO_ENV=production``
  Sets ``DEBUG = False``. Sets `HTTPS-related settings <https://docs.djangoproject.com/en/4.2/topics/security/#ssl-https>`__, if ``LOCAL_ACCESS`` is not set and ``ALLOWED_HOSTS`` is set. If using the Django Cookiecutter template, the :doc:`Dockerfile<../docker/django>` sets it.
``LOCAL_ACCESS``
  If set, HTTPS-related settings are not set.
``DJANGO_PROXY``
  If set, proxy-related settings are set. This requires the web server to be properly configured (see the warning about `SECURE_PROXY_SSL_HEADER <https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header>`__). For example:

  .. code-block:: apache

     RequestHeader unset X-Forwarded-Proto
     RequestHeader set X-Forwarded-Proto https env=HTTPS

     ProxyPass / http://127.0.0.1:8000/
     ProxyPassReverse / http://127.0.0.1:8000/

``ALLOWED_HOSTS``
  Set to a comma-separated list of `host names <https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts>`__. Localhost connections are always allowed.
``SECRET_KEY``
  Set to:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

``DATABASE_URL``
  Set according to `dj-database-url's documentation <https://github.com/kennethreitz/dj-database-url#readme>`__.
``SECURE_HSTS_SECONDS``
  Set according to `Django's documentation <https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security>`__.
``SENTRY_DSN``
  Set to the project's client key (DSN) from Sentry.
``FATHOM_ANALYTICS_ID`` (and ``FATHOM_ANALYTICS_DOMAIN``)
  Set to the site's ID (and custom domain) from Fathom Analytics. Remember to configure your project to render the embed code (`example <https://github.com/open-contracting/data-registry/pull/160/files>`__).

Using the settings template
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`SECRET_KEY <https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-SECRET_KEY>`__
  Replace ``!!!SECRET_KEY!!!`` with:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

`INSTALLED_APPS <https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-INSTALLED_APPS>`__
  Do not enable more applications than necessary. Among the `default applications <https://github.com/django/django/blob/main/django/conf/project_template/project_name/settings.py-tpl>`__:

  `django.contrib.admin <https://docs.djangoproject.com/en/4.2/ref/contrib/admin/>`__ (`tutorial <https://docs.djangoproject.com/en/4.2/intro/tutorial02/>`__)
    Remove, unless using the Django admin (check for occurrences of ``admin``).
  `django.contrib.auth <https://docs.djangoproject.com/en/4.2/ref/contrib/auth/>`__ (`topic <https://docs.djangoproject.com/en/4.2/topics/auth/>`__)
    Remove, unless using ``django.contrib.admin`` or authenticated users (check for occurrences of ``auth`` or ``user``).
  `django.contrib.messages <https://docs.djangoproject.com/en/4.2/ref/contrib/messages/>`__
    Remove, unless using ``django.contrib.admin`` or one-time messages (check for occurrences of ``messages``).
  `django.contrib.contenttypes <https://docs.djangoproject.com/en/4.2/ref/contrib/contenttypes/>`__
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth`` or otherwise dependent.
  django.contrib.sessions (`topic <https://docs.djangoproject.com/en/4.2/topics/http/sessions/>`__)
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth``, ``django.contrib.messages`` or anonymous sessions (check for occurrences of ``session``).
  `django.contrib.staticfiles <https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/>`__ (`how-to <https://docs.djangoproject.com/en/4.2/howto/static-files/>`__)
    Remove, unless the project contains static files.
  `django.contrib.sitemaps <https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/>`__
    Remove, if the application is private. (Added by the Cookiecutter template.)

  Then, make any corresponding changes to ``urls.py``, and ``MIDDLEWARE``, ``TEMPLATES``, ``STATIC_URL`` and ``AUTH_PASSWORD_VALIDATORS`` in ``settings.py``.
`DATABASES <https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-DATABASES>`__
  -  Replace ``{{ cookiecutter.database_name }}`` and ``{{ cookiecutter.application_name }}``.
  -  Remember to add `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ to your :doc:`requirements file<requirements>`.
`LOGGING <https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-LOGGING>`__
  See :doc:`logging`.

Add additional settings for:

-  Django under ``# Project-specific Django configuration``
-  Dependencies under ``# Dependency configuration``
-  Your project under ``# Project configuration``

.. _django-template:

Settings template
~~~~~~~~~~~~~~~~~

This template is based on the `default settings.py file <https://github.com/django/django/blob/stable/3.2.x/django/conf/project_template/project_name/settings.py-tpl>`__. You can also refer to the `default Django settings <https://github.com/django/django/blob/stable/3.2.x/django/conf/global_settings.py>`__. Replace ``core`` with the project's module name and remove the Jinja syntax if not using the Cookiecutter template:

.. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/core/settings.py
   :language: python

.. seealso::

   The ``LANGUAGE_CODE`` is ``en-us``. See :doc:`i18n` for details.

.. _django-performance:

Performance
-----------

In order of importance:

-  Reduce the number of SQL queries (avoid `N+1 queries <https://docs.sentry.io/product/issues/issue-details/performance-issues/n-one-queries/>`__):

   -  Avoid queries inside a loop. For ``SELECT``, perform a single query before the loop (or do the work in batches). For ``INSERT`` and ``UPDATE``, use the `bulk_create <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create>`__ and `bulk_update <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.bulk_update>`__ methods after the loop (or do the work in batches).

      .. warning::

         Read the caveats for the ``bulk_*`` methods in the Django documentation.

   -  Use `select_related <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-related>`__ to reduce the number of queries on ``ForeignKey`` or ``OneToOneField`` relations.
   -  Use `prefetch_related <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#prefetch-related>`__ to reduce the number of queries on ``ManyToManyField`` and reverse ``ForeignKey`` relations.
   -  Use `count <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#count>`__ if you only need to count. However, if you also need to use the result of the queryset, use ``len()``.
   -  Use `assertNumQueries <https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries>`__ in tests.
   -  Set the ``django`` logger's level to ``DEBUG`` in development to add SQL queries to the ``runserver`` output.

-  Cache results:

   -  Use `Django's cache framework <https://docs.djangoproject.com/en/4.2/topics/cache/>`__, and be sure to invalidate the cache when appropriate.

-  Optimize queries:

   -  Add indexes to fields that are frequently used for filtering. To find slow queries, you can use the PostgreSQL log in production or the SQL panel of `Django Debug Toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`__ in development.
   -  Use the `update_fields argument <https://docs.djangoproject.com/en/4.2/ref/models/instances/#ref-models-update-fields>`__ to the ``save()`` method for frequent operations.

-  Minimize memory usage:

   -  Use `iterator <https://docs.djangoproject.com/en/4.2/ref/models/querysets/#iterator>`__ when iterating over a queryset whose result is only accessed this once.

Read:

-  `Performance and optimization <https://docs.djangoproject.com/en/4.2/topics/performance/>`__
-  `Database access optimization <https://docs.djangoproject.com/en/4.2/topics/db/optimization/>`__
-  `Performance optimizations <https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/#performance-optimizations>`__ in the Deployment checklist

Deployment
----------

To perform deployment checks locally, run:

.. code-block:: bash

   env DJANGO_ENV=production ALLOWED_HOSTS=example.com SECURE_HSTS_SECONDS=1 ./manage.py check --deploy --fail-level WARNING

-  Use the `Deployment checklist <https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/>`__
-  Read `Deploying Django <https://docs.djangoproject.com/en/4.2/howto/deployment/>`__

.. seealso::

  :doc:`../docker/django`

Static files
~~~~~~~~~~~~

**DO NOT** commit the files generated by `collectstatic <https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#collectstatic>`__. These commands are either run during `deployment <https://ocdsdeploy.readthedocs.io/en/latest/>`__ or when :doc:`creating Docker images<../docker/index>`.

Use `ManifestStaticFilesStorage <https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage>`__ for cache-busting.

Generated files
~~~~~~~~~~~~~~~

**DO NOT** commit the files generated by `compilemessages <https://docs.djangoproject.com/en/4.2/ref/django-admin/#compilemessages>`__. These commands are either run during `deployment <https://ocdsdeploy.readthedocs.io/en/latest/>`__ or when :doc:`creating Docker images<../docker/index>`.

Development
-----------

Troubleshooting
~~~~~~~~~~~~~~~

.. seealso::

   `pdb — The Python Debugger <https://docs.python.org/3/library/pdb.html>`__

To access a Python shell with Django configured:

.. code-block:: shell

   ./manage.py shell

To access the default database:

.. code-block:: shell

   ./manage.py dbshell

.. seealso::

   -  `django-admin and manage.py <https://docs.djangoproject.com/en/4.2/ref/django-admin/>`__

To `log SQL statements <https://docs.djangoproject.com/en/4.2/ref/logging/#django-db-backends>`__, add this under ``"loggers"`` in ``settings.py``:

.. code-block:: python

           "django.db.backends": {
               "handlers": ["console"],
               "level": "DEBUG",
               "propagate": False,
           },

.. _django-learn:

Learning
~~~~~~~~

-  `Tutorials <https://docs.djangoproject.com/en/4.2/intro/>`__
-  `Topics <https://docs.djangoproject.com/en/4.2/topics/>`__
-  `How-to <https://docs.djangoproject.com/en/4.2/howto/>`__, for example: `Writing custom django-admin commands <https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/>`__.
