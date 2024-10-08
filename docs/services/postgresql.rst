PostgreSQL
==========

.. note::

   The `Deploy <https://ocdsdeploy.readthedocs.io/en/latest/>`__ documentation covers many topics relating to PostgreSQL, including: `configuration <https://ocdsdeploy.readthedocs.io/en/latest/develop/update/postgres.html>`__, `maintenance <https://ocdsdeploy.readthedocs.io/en/latest/maintain/databases.html>`__, and `usage by clients <https://ocdsdeploy.readthedocs.io/en/latest/use/databases.html>`__. This page addresses topics relating to software development.

Connect to a database
---------------------

Connect to the database using a connection string stored in the ``DATABASE_URL`` environment variable.

In Python, connect to the database using `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ if using :doc:`Django<../python/django>`, or `psycopg2 <https://www.psycopg.org/docs/module.html#psycopg2.connect>`__ otherwise.

To set the search path for a PostgreSQL connection, append to the connection string:

.. code-block:: none
   :caption: psycopg2

   ?options=-csearch_path%3Dmyschema,public

.. code-block:: none
   :caption: dj-database-url

   ?currentSchema=myschema,public

Identify the client
-------------------

Database administrators need to identify the sources of queries, in order to notify developers of inefficient queries or alert users whose queries will be interrupted by maintenance. For example:

-  Django applications set the `application_name <https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME>`__ query string parameter in the PostgreSQL `connection URI <https://www.postgresql.org/docs/current/libpq-connect.html#id-1.7.3.8.3.6>`__, or use a service-specific user
-  Kingfisher Summarize uses the `psycopg2 <https://www.psycopg.org/docs/>`__ package, and adds ``/* kingfisher-summarize {identifier} */`` as a comment to expensive queries
-  Kingfisher Colab uses the `ipython-sql <https://pypi.org/project/ipython-sql/>`__ package, and adds the Google Colaboratory notebook URL as a comment to all queries

Define tables
-------------

-  In PostgreSQL, use ``TEXT`` instead of other character types, as there is `no performance difference <https://www.postgresql.org/docs/current/datatype-character.html>`__.
-  Use ``NOT NULL`` with character types, `as recommended by Django <https://docs.djangoproject.com/en/4.2/ref/models/fields/#null>`__.
-  Use ``NOT NULL`` with JSON types, and set the default to an empty object, array or string.
-  In Python, do not set default values to ``{}`` or ``[]``. In Django, use ``default=dict`` and ``default=list``. In Pydantic (including SQLModel), use ``default_factory=dict`` and ``default_factory=list``.
-  JSON data often exceeds 2kb, and is therefore `TOASTed <https://www.postgresql.org/docs/current/storage-toast.html#STORAGE-TOAST-ONDISK>`__. If the application needs to SELECT a value from the JSON data, it is faster to extract that value to a column: for example, ``release_date``.

.. seealso::

   :ref:`Django models<django-models>`

Name conventions
~~~~~~~~~~~~~~~~

-  Timestamp columns: ``created_at``, ``updated_at`` and ``deleted_at``. (Some projects use ``created`` and ``modified``.)

Define indexes
--------------

-  Add an index for every foreign key with a corresponding ``JOIN`` query. If the ``JOIN`` and/or ``WHERE`` clauses use multiple columns of the same table, create a multi-column index, with the most used column as the index's first column.
-  Use `EXPLAIN <https://wiki.postgresql.org/wiki/Using_EXPLAIN>`__ to figure out why a query is slow. It could be due to a missing index (sequential scan), an unused index, or a slower plan (for example, using index scan instead of bitmap index scan)

   .. note::

      When using a tool like `Dalibo <https://explain.dalibo.com>`__ or `pgMustard <https://www.pgmustard.com>`__, follow these `instructions <https://www.pgmustard.com/getting-a-query-plan>`__ to get the query plan. Otherwise, if you don't know how slow the query is, omit the ``ANALYZE`` and ``BUFFERS`` options, to only plan and not execute the query.

Load (or dump) data
-------------------

Use the `\copy <https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMANDS-COPY>`__ meta-command instead of the `COPY <https://www.postgresql.org/docs/current/sql-copy.html>`__ command, so that file accessibility and privileges are those of the user, not the server – such that no SQL superuser privileges are required.

.. _sql-statements:

Construct SQL statements
------------------------

Follow `best practices <https://www.psycopg.org/docs/usage.html#sql-injection>`__ to avoid accidental errors and `SQL injection <https://en.wikipedia.org/wiki/SQL_injection>`__. The code samples below use the psycopg2 Python package.

-  `Pass parameters to SQL queries <https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries>`__, using the second argument to the ``execute`` method. This adapts the Python value's type (like ``bool``, ``int``, ``str``) to the correct SQL representation:

   .. code-block:: python

      cur.execute("SELECT * FROM release WHERE release_date > %(date)s", {'date': '2020-01-01'})

   **DO NOT** use string interpolation (``%``):

   .. code-block:: python

      cur.execute("SELECT * FROM release WHERE release_date > '%(date)s'" % {'date': '2020-01-01'})  # WRONG

   **DO NOT** use string concatenation (``+``):

   .. code-block:: python

      cur.execute("SELECT * FROM release WHERE release_date > '" + '2020-01-01' + "'")  # WRONG

   **AVOID** using literal values:

   .. code-block:: python

      cur.execute("SELECT * FROM release WHERE release_date > '2020-01-01'")  # AVOID

   For example, if you forget that dates are represented as strings in SQL, you might do the following, which evaluates ``2020-12-31`` to ``1977``, which will match everything in the database:

   .. code-block:: python

      cur.execute("SELECT * FROM release WHERE release_date > 2020-12-31")  # BROKEN

-  Use named placeholders like ``%(collection_id)s``. This allows you to use the same placeholder multiple times in the query, while only having to pass a single parameter, and to edit and re-order your query without re-ordering your parameters.

   .. code-block:: python

      cur.execute("""
          SELECT * FROM release WHERE collection_id = %(collection_id)s
          UNION
          SELECT * FROM record WHERE collection_id = %(collection_id)s AND ocid = %(ocid)s
      """, {'collection_id': 1, 'ocid': 'ocds-213czf-1'})

   **AVOID** use anonymous placeholders (``%s``):

   .. code-block:: python

      cur.execute("""
          SELECT * FROM release WHERE collection_id = %s
          UNION
          SELECT * FROM record WHERE collection_id = %s AND ocid = %s
      """, (1, 1, 'ocds-213czf-1'))  # AVOID

-  If you are writing a query template in which you want to substitute column names or table names, use the ``format`` method and the ``SQL`` and ``Identifier`` classes (`documentation <https://www.psycopg.org/docs/sql.html>`__):

   .. code-block:: python

      from psycopg2.sql import SQL, Identifier

      cur.execute(SQL("SELECT * FROM {table}").format(table=Identifier('collection')))

   You can use this together with passing parameters:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {table} WHERE id = %(id)s").format(
          table=Identifier('collection')), {'id': 1})

   Remember to format the ``SQL()`` object. **DO NOT** format the string itself:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {table} WHERE id = %(id)s".format(
          table='collection'), {'id': 1})  # WRONG

   **DO NOT** use string interpolation (``%``):

   .. code-block:: python

      cur.execute("SELECT * FROM %s" % 'collection')  # WRONG

   **DO NOT** use string concatenation (``+``):

   .. code-block:: python

      cur.execute("SELECT * FROM " + 'collection')  # WRONG

   **AVOID** using anonymous placeholders:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {}".format('collection'))  # AVOID

Paginate rows
~~~~~~~~~~~~~

Do not use ``LIMIT`` with ``OFFSET``. ``OFFSET`` becomes more inefficient as its value increases. Instead, filter on the table's primary key, which has near-constant performance. For example:

.. code-block:: sql

   SELECT id, mycolumn
   FROM mytable
   WHERE
       id > %s
       AND myfilter = %s
   ORDER BY id
   LIMIT 1000

Format code
-----------

Format SQL files with `pg_format <https://github.com/darold/pgFormatter>`__, which has web and command-line interfaces.

Web
~~~

#. Open https://sqlformat.darold.net
#. Paste your SQL text
#. Set *Functions* to *Lower case*
#. Click *Format my code*

CLI
~~~

On macOS, using `Homebrew <https://brew.sh>`__, install it with:

.. code-block:: bash

   brew install pgformatter

Then, change into the project's directory and run, for example:

.. code-block:: bash

   find . -name '*.sql' -exec pg_format -f 1 -o {} {} \;

.. _postgresql-erd:

Generate entity relationship diagram
------------------------------------

#. Install `SchemaSpy <https://schemaspy.readthedocs.io/en/latest/installation.html>`__
#. Download the `PostgreSQL JDBC Driver <https://jdbc.postgresql.org/>`__
#. Rename the JAR files to ``schemaspy.jar`` and ``postgresql.jar``
#. Move the JAR files to a preferred location

Run SchemaSpy, using appropriate values for the ``-db`` (database name), ``-s`` (schema, optional), ``-u`` (user) and ``-p`` (password, optional) arguments:

.. code-block:: bash

   java -jar schemaspy.jar -t pgsql -dp postgresql.jar -host localhost -db DATABASE -s SCHEMA -u USER -p PASSWORD -o schemaspy -norows

Use either the ``schemaspy/diagrams/summary/relationships.real.compact.png`` or ``schemaspy/diagrams/summary/relationships.real.large.png`` file and check the ``schemaspy/diagrams/orphans/`` directory.

Reference
---------

-  `Improve slow queries <https://ocdsdeploy.readthedocs.io/en/latest/use/databases.html#improve-slow-queries>`__
