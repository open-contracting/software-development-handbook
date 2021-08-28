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

Reference
---------

-  `The Django admin site <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/>`__
