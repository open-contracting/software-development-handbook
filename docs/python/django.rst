Django
======

General
-------

-  Delete empty, auto-generated files.

Layout
------

-  Maintain the distinction between app directories and the project directory.
-  Use ``core`` or the name of the repository as the project name.

.. seealso::

   :doc:`Directory layout guide<layout>`

Models
------

-  Use ``help_text`` and ``verbose_name`` to describe fields.
-  Use ``TextField``, not ``CharField``. There is `no performance difference <https://www.postgresql.org/docs/11/datatype-character.html>`__ in PostgreSQL.
-  Do not use ``null=True`` with ``TextField`` or ``CharField``, `as recommended by Django <https://docs.djangoproject.com/en/3.2/ref/models/fields/#null>`__.

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

-  In many cases, you can achieve the same outcome using either `context processors <https://docs.djangoproject.com/en/3.2/ref/templates/api/#writing-your-own-context-processors>`__ or `inclusion tags <https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags>`__. If the variables that the template uses are constant (e.g. from a Django settings file), use a context processor. Otherwise, use an inclusion tag.

.. _django-settings:

Settings
--------

To simplify the configuration of Django projects, use the :ref:`template below<django-template>` for the `settings file <https://docs.djangoproject.com/en/3.2/topics/settings/>`__.

In other modules, import settings from ``django.conf``, `as recommended <https://docs.djangoproject.com/en/3.2/topics/settings/#using-settings-in-python-code>`__:

.. code-block:: python

   from django.conf import settings

.. seealso::

   :doc:`Settings guide<settings>`, for the general approach to configuration

Environment variables
~~~~~~~~~~~~~~~~~~~~~

``DJANGO_ENV=production``
  Sets ``DEBUG = False``. Sets `HTTPS-related settings <https://docs.djangoproject.com/en/3.2/topics/security/#ssl-https>`__, if ``LOCAL_ACCESS`` is not set and ``ALLOWED_HOSTS`` is set.
``LOCAL_ACCESS``
  If set, HTTPS-related settings are not set.
``ALLOWED_HOSTS``
  Set to a comma-separated list of `host names <https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts>`__. Localhost connections are always allowed.
``SECRET_KEY``
  Set to:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

``DATABASE_URL``
  Set according to `dj-database-url's documentation <https://github.com/kennethreitz/dj-database-url#readme>`__.
``SECURE_HSTS_SECONDS``
  Set according to `Django's documentation <https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security>`__.
``SENTRY_DSN``
  Set to the project's client key (DSN) from Sentry.
``FATHOM_ANALYTICS_DOMAIN=kite.open-contracting.org``
  Remember to configure your project to render the embed code (`example <https://github.com/open-contracting/data-registry/pull/160/files>`__).
``FATHOM_ANALYTICS_ID``
  Set to the site's ID from Fathom Analytics.

Using the template
~~~~~~~~~~~~~~~~~~

`SECRET_KEY <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY>`__
  Replace ``{{ secret_key }}`` with:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

`INSTALLED_APPS <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-INSTALLED_APPS>`__
  Do not enable more applications than necessary. Among the `default applications <https://github.com/django/django/blob/main/django/conf/project_template/project_name/settings.py-tpl>`__:

  `django.contrib.admin <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/>`__ (`tutorial <https://docs.djangoproject.com/en/3.2/intro/tutorial02/>`__)
    Remove, unless using the Django admin (check for occurrences of ``admin``).
  `django.contrib.auth <https://docs.djangoproject.com/en/3.2/ref/contrib/auth/>`__ (`topic <https://docs.djangoproject.com/en/3.2/topics/auth/>`__)
    Remove, unless using ``django.contrib.admin`` or authenticated users (check for occurrences of ``auth`` or ``user``).
  `django.contrib.messages <https://docs.djangoproject.com/en/3.2/ref/contrib/messages/>`__
    Remove, unless using ``django.contrib.admin`` or one-time messages (check for occurrences of ``messages``).
  `django.contrib.contenttypes <https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/>`__
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth`` or otherwise dependent.
  django.contrib.sessions (`topic <https://docs.djangoproject.com/en/3.2/topics/http/sessions/>`__)
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth``, ``django.contrib.messages`` or anonymous sessions (check for occurrences of ``session``).
  `django.contrib.staticfiles <https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/>`__ (`how-to <https://docs.djangoproject.com/en/3.2/howto/static-files/>`__)
    Remove, unless the project contains static files.

  Then, make any corresponding changes to ``urls.py``, and ``MIDDLEWARE``, ``TEMPLATES``, ``STATIC_URL`` and ``AUTH_PASSWORD_VALIDATORS`` in ``settings.py``.
`DATABASES <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DATABASES>`__
  -  Replace ``{{ database_name }}`` and ``{{ app_name }}``.
  -  Remember to add `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ to your :doc:`requirements file<requirements>`.
`LOGGING <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-LOGGING>`__
  See :doc:`logging`.

Add additional settings for:

-  Django under ``# Project-specific Django configuration``
-  Dependencies under ``# Dependency configuration``
-  Your project under ``# Project configuration``

**AVOID** setting `LOCALE_PATHS <https://docs.djangoproject.com/en/3.2/ref/settings/#locale-paths>`__. Instead, allow Django to `discover translations <https://docs.djangoproject.com/en/3.2/topics/i18n/translation/#how-django-discovers-translations>`__ and to `write files <https://docs.djangoproject.com/en/3.2/topics/i18n/translation/#how-to-create-language-files>`__ with `manage.py makemessages <https://docs.djangoproject.com/en/3.2/ref/django-admin/#makemessages>`__ in the appropriate directories.

.. _django-template:

Template
~~~~~~~~

This template is based on the `default settings.py file <https://github.com/django/django/blob/stable/3.2.x/django/conf/project_template/project_name/settings.py-tpl>`__. You can also refer to the `default Django settings <https://github.com/django/django/blob/stable/3.2.x/django/conf/global_settings.py>`__. Replace ``{{ project_name }}`` with the project's module name:

.. literalinclude:: samples/settings.py
   :language: python

.. _django-performance:

Performance
-----------

-  Read `Performance and optimization <https://docs.djangoproject.com/en/3.2/topics/performance/>`__
-  Read `Database access optimization <https://docs.djangoproject.com/en/3.2/topics/db/optimization/>`__
-  Read `Performance optimizations <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#performance-optimizations>`__ in the Deployment checklist

Deployment
----------

**DO NOT** commit the files generated by `collectstatic <https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#collectstatic>`__ or `compilemessages <https://docs.djangoproject.com/en/3.2/ref/django-admin/#compilemessages>`__. These commands are either run during `deployment <https://ocdsdeploy.readthedocs.io/en/latest/>`__ or when :doc:`creating Docker images<../docker/index>`.

-  Use the `Deployment checklist <https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/>`__
-  Read `Deploying Django <https://docs.djangoproject.com/en/3.2/howto/deployment/>`__
