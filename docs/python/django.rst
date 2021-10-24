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

To simplify the configuration of Django projects, use :ref:`the template below<django-template>` for the `Django settings file <https://docs.djangoproject.com/en/3.2/topics/settings/>`__. Some values can be overridden using environment variables.

In **development**, the default values are appropriate as-is. Override the default values in other environments with, for example, a `uWSGI INI file <https://github.com/open-contracting/deploy/blob/main/salt/uwsgi/files/django.ini>`__ or a `Docker Compose .env file <https://docs.docker.com/compose/environment-variables/>`__ in **production** or a GitHub Actions workflow in **testing**.

Environment variables
~~~~~~~~~~~~~~~~~~~~~

``DJANGO_ENV=production``
  Sets ``DEBUG = False``. Sets `HTTPS-related settings <https://docs.djangoproject.com/en/3.2/topics/security/#ssl-https>`__, unless ``LOCAL_ACCESS`` is set.
``ALLOWED_HOSTS=hostname1,hostname2``
  Localhost is allowed by default.
``SECRET_KEY``
  Set to:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

``DATABASE_URL``
  `See dj-database-url's documentation <https://github.com/kennethreitz/dj-database-url#readme>`__.
``SECURE_HSTS_SECONDS``
  `See Django's documentation <https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security>`__.
``SENTRY_DSN``
  Get the project's client key (DSN) from Sentry.
``FATHOM_ANALYTICS_DOMAIN=kite.open-contracting.org``
  Configure your project to render the embed code (`example <https://github.com/open-contracting/data-registry/pull/160/files>`__).
``FATHOM_ANALYTICS_ID``
  Get the site's ID from Fathom Analytics.

Using the template
~~~~~~~~~~~~~~~~~~

`SECRET_KEY <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY>`__
  Replace ``{{ secret_key }}`` with:

  .. code-block:: bash

     python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

`INSTALLED_APPS <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-INSTALLED_APPS>`__
  Do not enable more applications than necessary. Among the `default applications <https://github.com/django/django/blob/main/django/conf/project_template/project_name/settings.py-tpl>`__:

  `django.contrib.admin <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/>`__ (`tutorial <https://docs.djangoproject.com/en/3.2/intro/tutorial02/>`__)
    Remove, unless using the Django admin (check for occurrences of ``admin``)
  `django.contrib.auth <https://docs.djangoproject.com/en/3.2/ref/contrib/auth/>`__ (`topic <https://docs.djangoproject.com/en/3.2/topics/auth/>`__)
    Remove, unless using ``django.contrib.admin`` or authenticated users (check for occurrences of ``auth`` or ``user``)
  `django.contrib.messages <https://docs.djangoproject.com/en/3.2/ref/contrib/messages/>`__
    Remove, unless using ``django.contrib.admin`` or one-time messages (check for occurrences of ``messages``)
  `django.contrib.contenttypes <https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/>`__
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth`` or otherwise dependent
  django.contrib.sessions (`topic <https://docs.djangoproject.com/en/3.2/topics/http/sessions/>`__)
    Remove, unless using ``django.contrib.admin``, ``django.contrib.auth``, ``django.contrib.messages`` or anonymous sessions (check for occurrences of ``session``)
  `django.contrib.staticfiles <https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/>`__ (`how-to <https://docs.djangoproject.com/en/3.2/howto/static-files/>`__)
    Remove, unless the project contains static files

  Then, make any corresponding changes to ``urls.py``, and ``MIDDLEWARE``, ``TEMPLATES``, ``STATIC_URL`` and ``AUTH_PASSWORD_VALIDATORS`` in ``settings.py``.
`DATABASES <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DATABASES>`__
  
  -  Add `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ to your :ref:`requirements file<application-requirements>`.
  -  Replace ``{{ database_name }}`` and ``{{ app_name }}``.

`LOGGING <https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-LOGGING>`__
  See :doc:`logging`.

Add additional settings for:

-  Django under ``# Project-specific Django configuration``
-  Dependencies under ``# Dependency configuration``
-  Your project under ``# Project configuration``

.. _django-template:

Template
~~~~~~~~

This template is based on the `default settings.py file <https://github.com/django/django/blob/stable/3.2.x/django/conf/project_template/project_name/settings.py-tpl>`__. You can also refer to the `default Django settings <https://github.com/django/django/blob/stable/3.2.x/django/conf/global_settings.py>`__.

Replace ``{{ project_name }}`` with the project's module name:

.. code-block:: python

   """
   Django settings for the project.

   Generated by 'django-admin startproject' using Django 3.2.8.

   For more information on this file, see
   https://docs.djangoproject.com/en/3.2/topics/settings/

   For the full list of settings and their values, see
   https://docs.djangoproject.com/en/3.2/ref/settings/
   """

   import os
   from pathlib import Path

   import dj_database_url
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   from sentry_sdk.integrations.logging import ignore_logger

   production = os.getenv('DJANGO_ENV') == 'production'
   local_access = os.getenv('LOCAL_ACCESS')

   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent


   # Quick-start development settings - unsuitable for production
   # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = os.getenv('SECRET_KEY', '{{ secret_key }}')

   # SECURITY WARNING: don't run with debug turned on in production!
   DEBUG = not production

   ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
   if 'ALLOWED_HOSTS' in os.environ:
       ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))


   # Application definition

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       "django.middleware.locale.LocaleMiddleware",
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

   ROOT_URLCONF = '{{ project_name }}.urls'

   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.template.context_processors.i18n',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]

   WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


   # Database
   # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

   DATABASES = {
       'default': dj_database_url.config(default="postgresql:///{{ database_name }}?application_name={{ app_name }}")
   }


   # Password validation
   # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

   AUTH_PASSWORD_VALIDATORS = [
       {
           'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
       },
   ]


   # Internationalization
   # https://docs.djangoproject.com/en/3.2/topics/i18n/

   LANGUAGE_CODE = 'en-us'

   TIME_ZONE = 'UTC'

   USE_I18N = True

   USE_L10N = True

   USE_TZ = True


   # Static files (CSS, JavaScript, Images)
   # https://docs.djangoproject.com/en/3.2/howto/static-files/

   STATIC_URL = '/static/'

   # Default primary key field type
   # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


   # Project-specific Django configuration

   # https://docs.djangoproject.com/en/3.2/topics/logging/#django-security
   LOGGING = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "console": {
               "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
           },
       },
       "handlers": {
           "console": {
               "class": "logging.StreamHandler",
               "formatter": "console",
           },
           "null": {
               "class": "logging.NullHandler",
           },
       },
       "loggers": {
           "": {
               "handlers": ["console"],
               "level": "INFO",
           },
           "django.security.DisallowedHost": {
               "handlers": ["null"],
               "propagate": False,
           },
       },
   }

   # https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
   if production and not local_access:
       # Run: env DJANGO_ENV=production SECURE_HSTS_SECONDS=1 ./manage.py check --deploy
       CSRF_COOKIE_SECURE = True
       SESSION_COOKIE_SECURE = True
       SECURE_SSL_REDIRECT = True
       SECURE_REFERRER_POLICY = "same-origin"  # default in Django >= 3.1

       # https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security
       if "SECURE_HSTS_SECONDS" in os.environ:
           SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS"))
           SECURE_HSTS_INCLUDE_SUBDOMAINS = True
           SECURE_HSTS_PRELOAD = True


   # Dependency configuration

   if "SENTRY_DSN" in os.environ:
       # https://docs.sentry.io/platforms/python/logging/#ignoring-a-logger
       ignore_logger("django.security.DisallowedHost")
       sentry_sdk.init(
           dsn=os.getenv("SENTRY_DSN"),
           integrations=[DjangoIntegration()],
           traces_sample_rate=0,  # The Sentry plan does not include Performance.
       )


   # Project configuration

   FATHOM = {
       "domain": os.getenv("FATHOM_ANALYTICS_DOMAIN") or "cdn.usefathom.com",
       "id": os.getenv("FATHOM_ANALYTICS_ID"),
   }

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

-  `Deploying Django <https://docs.djangoproject.com/en/3.2/howto/deployment/>`__
