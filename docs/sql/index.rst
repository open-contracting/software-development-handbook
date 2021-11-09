SQL
===

.. seealso::

   :doc:`PostgresQL guide<../services/postgresql>`

Name conventions
----------------

-  Timestamp columns: ``created_at``, ``updated_at`` and ``deleted_at``. (Some projects use ``created`` and ``modified``.)

Code style
----------

Paginate data
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

Load and dump data
~~~~~~~~~~~~~~~~~~

Use the `\copy <https://www.postgresql.org/docs/13/app-psql.html#APP-PSQL-META-COMMANDS-COPY>`__ meta-command instead of the `COPY <https://www.postgresql.org/docs/13/sql-copy.html>`__ command, so that file accessibility and privileges are those of the user, not the server – such that no SQL superuser privileges are required.

Code format
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

Reference
---------

-  `Improve slow queries <https://ocdsdeploy.readthedocs.io/en/latest/use/databases.html#improve-slow-queries>`__
