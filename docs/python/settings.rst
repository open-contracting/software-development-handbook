Settings
========

.. seealso::

   :ref:`Django settings style guide<django-settings>`

All applications should read configuration from environment variables, like in the `Twelve-Factor App methodology <https://12factor.net>`__. 

In **development**, the default values should be appropriate as-is. The default values can be overridden in other environments with, for example, a `uWSGI INI file <https://github.com/open-contracting/deploy/blob/main/salt/uwsgi/files/django.ini>`__ or a `Docker Compose .env file <https://docs.docker.com/compose/environment-variables/>`__ in **production** or a GitHub Actions workflow in **testing**.

For :ref:`command-line interfaces<python-scripts>`, configure the environment variables in a ``.env`` file. Use `python-dotenv <https://pypi.org/project/python-dotenv/>`__ (not `django-environ <https://pypi.org/project/django-environ/>`__) to load the file: for example, `Kingfisher Summarize <https://github.com/open-contracting/kingfisher-summarize/blob/main/manage.py>`__.

Otherwise, read configuration from INI files using `configparser <https://docs.python.org/3/library/configparser.html>`__. Do not use: JSON (no comments), YAML (data typing, too many features, not in standard library), `TOML <https://github.com/madmurphy/libconfini/wiki/An-INI-critique-of-TOML>`__ (data typing, too many features, not in standard library), or XML (verbose, not in standard library).

Word choice
-----------

Use the following names for environment variables:

- ``LOG_LEVEL``

-  Local services

   -  ``DATABASE_URL``
   -  ``RABBIT_URL``
   -  ``RABBIT_EXCHANGE_NAME``

-  Third-party services

   -  ``FATHOM_ANALYTICS_DOMAIN``
   -  ``FATHOM_ANALYTICS_ID``
   -  ``SENTRY_DSN`` (not DNS!)
   -  ``SENTRY_SAMPLE_RATE``

Deployment
----------

Environment variables are configured in Pillar files in the `deploy repository <https://github.com/open-contracting/deploy>`__ (see `documentation <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/python.html>`__).
