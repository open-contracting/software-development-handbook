Library and Web API
===================

.. note::

   This page is a stub.

Library API
-----------

Take a documentation-driven development approach. That is, write the public documentation first, then write the code. In doing so, you can surface complexities that can be simplified, and otherwise work through many design issues.

Web API
-------

Follow best practices for authoring APIs. Some tips:

-  Use hyphens as separators in paths.
-  Use status codes. Do not return JSON responses like ``{"status": "ok", "data": {...}}``. See `Choosing an HTTP Status Code — Stop Making It Hard <https://www.codetinkerer.com/2015/12/04/choosing-an-http-status-code.html>`__.

.. seealso::

   OCDS documentation `API access <https://standard.open-contracting.org/latest/en/guidance/build/hosting/#api-access>`__ guidance

Endpoint names
~~~~~~~~~~~~~~

Use lowercase letters and separate words with hyphens or underscores.

   Example: GET /users or GET /users/all

If the endpoint retrieves a specific resource, use the resource name in its singular form.

   Example: GET /user/{id} or PUT /user/{id}

For endpoints that return collections of resources, use plural nouns.

   Example: GET /users or POST /users

Use sub-resources to represent relationships between resources.

   Example: GET /users/{id}/orders or GET /users/{id}/invoices

For actions or operations that do not fit into the RESTful resource model, consider using verbs or descriptive phrases.

   Example: POST /users/{id}/reset-password or PUT /users/{id}/activate

Avoid using abbreviations or acronyms unless they are widely understood and agreed upon within your development team or industry.

Ensure that the endpoint names are self-explanatory and reflect the purpose of the API operation.
