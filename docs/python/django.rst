Django style guide
==================

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
