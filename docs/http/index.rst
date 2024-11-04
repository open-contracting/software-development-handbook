HTTP
====

In order of preference, set these headers in:

-  project code
-  ``default.conf`` file, if the project includes a `Docker image running nginx <https://ocp-software-handbook.readthedocs.io/en/latest/docker/dockerfile.html#base-images>`__
-  `deploy <https://github.com/open-contracting/deploy>`__ repository, if the project runs third-party code, like WordPress

X-Content-Type-Options
----------------------

If not already set (like via `SECURE_CONTENT_TYPE_NOSNIFF <https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECURE_CONTENT_TYPE_NOSNIFF>`__ in Django), set the header to:

.. code-block:: none

   nosniff

Strict-Transport-Security (HSTS)
--------------------------------

If not already set (like via :ref:`SECURE_HSTS_SECONDS<django-env>` in Django), set the header to:

.. code-block:: none

   max-age=31536000; includeSubdomains; preload
