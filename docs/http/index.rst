HTTP
====

In order of preference, set these headers in:

-  project code
-  ``default.conf`` file, if the project includes a `Docker image running nginx <https://ocp-software-handbook.readthedocs.io/en/latest/docker/dockerfile.html#base-images>`__
-  `_headers <https://developers.cloudflare.com/pages/configuration/headers/>`__ file, if hosting a static site on :ref:`Cloudflare Pages<cloudflare>`
-  `deploy <https://github.com/open-contracting/deploy>`__ repository, if the project runs third-party code, like WordPress

Strict-Transport-Security (HSTS)
--------------------------------

If not already set (like via :ref:`SECURE_HSTS_SECONDS<django-env>` in Django), set the header to:

.. code-block:: none

   max-age=31536000; includeSubdomains; preload

X-Content-Type-Options
----------------------

If not already set (like via `SECURE_CONTENT_TYPE_NOSNIFF <https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECURE_CONTENT_TYPE_NOSNIFF>`__ in Django), set the header to:

.. code-block:: none

   nosniff

Content Security Policy (CSP)
-----------------------------

.. admonition:: One-time setup

   Install the `Content Security Policy (CSP) Generator <https://chromewebstore.google.com/detail/content-security-policy-c/ahlnecfloencbkpfnpljbojmjkfgnmdc>`__ Chrome extension.

-  Generate a policy:

   -  Visit the website in Chrome
   -  Open the extension, and click the *Start Building Policy* button
   -  Navigate to every page of the website with unique assets
   -  Click two *Next* buttons, and copy the *Content-Security-Policy-Report-Only* textbox

-  Edit the policy:

   -  Delete all ``'report-sample'`` values
   -  Delete all directives whose policy is ``'self'`` only, except for the ``default-src`` directive
   -  Add a ``frame-ancestors 'none'`` directive

   .. list-table::
      :header-rows: 1

      * - Directive
        - Minimum
        - Typical
      * - ``script-src``
        - ``'self' https:``
        - ``'self' 'unsafe-inline' https:`` if using inline scripts
      * - ``style-src``
        - ``'self' 'unsafe-inline'``
        - ``'self' 'unsafe-inline'``, plus any external sources like ``https://use.fontawesome.com``
      * - ``img-src``
        - ``'self' https:``
        - ``'self' data: https:`` if using data URLs, plus external sources
      * - ``font-src``
        - Omit
        - ``'self' data:`` if using data URLs, plus any external sources like ``https://use.fontawesome.com``
      * - ``frame-src``
        - Omit
        - Add any external embeds, like Power BI, Google Docs or YouTube
      * - ``connect-src``
        - Omit
        - Add any external connections, like Google Analytics, other APIs or JSON files
      * - ``object-src``
        - ``'none'``
        -
      * - ``worker-src``
        - ``'none'``
        -
      * - ``frame-ancestors``
        - ``'none'``
        -

-  Deploy and test the policy.

   For example, the `extensionlist <https://sphinxcontrib-opencontracting.readthedocs.io/en/latest/#extensionlist>`__ Sphinx directive `breaks <https://github.com/open-contracting/standard/issues/741#issuecomment-1786217489>`__ if the ``connect-src`` CSP directive isn't `configured <https://github.com/open-contracting/deploy/commit/b11732cbbfe83c43e2f65cde27cb177eb838f8e3>`__ correctly.

A minimalist ``Content-Security-Policy`` header is:

.. code-block:: none

   default-src 'self';
   script-src 'self' https:;
   style-src 'self' 'unsafe-inline';
   img-src 'self' https:;
   object-src 'none';
   worker-src 'none';
   frame-ancestors 'none'

.. note::

   Django 6.0 adds `CSP support <https://github.com/django/django/pull/19393>`__ and is expected December 2025. Django 6.2 LTS is expected April 2027.

Reference: `Content Security Policy Reference <https://content-security-policy.com>`__
