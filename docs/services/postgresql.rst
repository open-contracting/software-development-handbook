PostgreSQL
==========

.. note::

   The `Deploy <https://ocdsdeploy.readthedocs.io/en/latest/index.html>`__ documentation covers many topics relating to PostgreSQL, including: configuration, maintenance, and usage by clients. This page addresses topics relating to software development.

Connect to a database
---------------------

Connect to the database using a connection string stored in the ``DATABASE_URL`` environment variable.

In Python, connect to the database using `dj-database-url <https://github.com/kennethreitz/dj-database-url#readme>`__ if using :doc:`Django<../python/django>`, or `psycopg2.connect() <https://www.psycopg.org/docs/module.html#psycopg2.connect>`__ otherwise.

To set the search path for a PostgreSQL connection, append to the connection string:

.. code-block:: none
   :caption: psycopg2

   ?options=-csearch_path%3Dmyschema,public

.. code-block:: none
   :caption: dj-database-url

   ?currentSchema=myschema,public

Identify the client
~~~~~~~~~~~~~~~~~~~

Database administrators need to identify the sources of queries, in order to notify developers of inefficient queries or alert users whose queries will be interrupted by maintenance. For example:

-  Django applications set the `application_name <https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME>`__ query string parameter in the PostgreSQL `connection URI <https://www.postgresql.org/docs/11/libpq-connect.html#id-1.7.3.8.3.6>`__, or use a service-specific user
-  Kingfisher Summarize uses the `psycopg2 <https://www.psycopg.org/docs/>`__ package, and adds ``/* kingfisher-summarize {identifier} */`` as a comment to expensive queries
-  Kingfisher Colab uses the `ipython-sql <https://pypi.org/project/ipython-sql/>`__ package, and adds the Google Colaboratory notebook URL as a comment to all queries

.. sql-statements:

Construct SQL statements
------------------------

Follow `best practices <https://www.psycopg.org/docs/usage.html#sql-injection>`__ to avoid accidental errors and `SQL injection <https://en.wikipedia.org/wiki/SQL_injection>`__. The code samples below use the psycopg2 Python package.

-  `Pass parameters to SQL queries <https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries>`__, using the second argument to the ``execute`` method. This adapts the Python value's type (like ``bool``, ``int``, ``str``) to the correct SQL representation:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > %(date)s", {'date': '2020-01-01'})

   **DO NOT** use string interpolation (``%``):

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '%(date)s'" % {'date': '2020-01-01'})  # WRONG

   **DO NOT** use string concatenation (``+``):

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '" + '2020-01-01' + "'")  # WRONG

   **AVOID** using literal values:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '2020-01-01'")  # AVOID

   For example, if you forget that dates are represented as strings in SQL, you might do the following, which evaluates ``2020-12-31`` to ``1977``, which will match everything in the database:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > 2020-12-31")  # BROKEN

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

Paginate data
-------------

Do not use ``LIMIT`` with ``OFFSET``. ``OFFSET`` becomes more inefficient as its value increases. Instead, filter on the table's primary key, which has near-constant performance. For example:

.. code-block:: sql

   SELECT id, mycolumn
   FROM mytable
   WHERE
       id > %s
       AND myfilter = %s
   ORDER BY id
   LIMIT 1000

Load and dump data
------------------

Use the `\copy <https://www.postgresql.org/docs/13/app-psql.html#APP-PSQL-META-COMMANDS-COPY>`__ meta-command instead of the `COPY <https://www.postgresql.org/docs/13/sql-copy.html>`__ command, so that file accessibility and privileges are those of the user, not the server – such that no SQL superuser privileges are required.

.. _postgresql-erd:

Generate Entity Relationship Diagram
------------------------------------

#. Install `SchemaSpy <https://schemaspy.readthedocs.io/en/latest/installation.html>`__
#. Download the `PostgreSQL JDBC Driver <https://jdbc.postgresql.org/>`__
#. Rename the JAR files to ``schemaspy.jar`` and ``postgresql.jar``
#. Move the JAR files to a preferred location

Run SchemaSpy, using appropriate values for the ``-db`` (database name), ``-s`` (schema, optional), ``-u`` (user) and ``-p`` (password, optional) arguments:

.. code-block:: bash

   java -jar schemaspy.jar -t pgsql -dp postgresql.jar -host localhost -db DATABASE -s SCHEMA -u USER -p PASSWORD -o schemaspy -norows

Use either the ``schemaspy/diagrams/summary/relationships.real.compact.png`` or ``schemaspy/diagrams/summary/relationships.real.large.png`` file and check the ``schemaspy/diagrams/orphans/`` directory.
