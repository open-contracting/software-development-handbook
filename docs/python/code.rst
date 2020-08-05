Code
====

Code is tested on Python 3.6 (`see the status of Python branches <https://devguide.python.org/#branchstatus>`__).

Reminders
---------

-  `Manage technical debt <https://tashian.com/articles/managing-technical-debt/>`__.
-  Instead of writing a ``TODO`` comment in the code, create an issue on GitHub. TODO’s in code are less visible to the rest of the team.

Style guide
-----------

All code is checked as documented by `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Repositories should not use ``.flake8`` or ``setup.cfg`` files to configure the behavior of ``flake8`` or ``isort``, except to ignore generated files like database migrations. Maintainers can find configuration files with:

.. code-block:: bash

   find . \( -name 'setup.cfg' -or -name '.flake8' \) -exec echo {} \; -exec cat {} \; 

``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``.

Otherwise, please refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

SQL statements
--------------

Follow `best practices <https://www.psycopg.org/docs/usage.html#sql-injection>`__ to avoid accidental errors and `SQL injection <https://en.wikipedia.org/wiki/SQL_injection>`__.

-  `Pass parameters to SQL queries <https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries>`__, using the second argument to the ``execute`` method. This adapts the Python value's type (like ``bool``, ``int``, ``str``) to the correct SQL representation:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > %(date)s", {'date': '2020-01-01'})

   **DO NOT** use string interpolation (``%``):

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '%(date)s'" % {'date': '2020-01-01'})

   **DO NOT** use string concatenation (``+``):

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '" + '2020-01-01' + "'")

   **AVOID** using literal values:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > '2020-01-01'")

   For example, if you forget that dates are represented as strings in SQL, you might do the following, which evaluates ``2020-12-31`` to ``1977``, which will match everything in the database:

   .. code-block:: python

      cur.execute("SELECT * FROM data WHERE data->>'date' > 2020-12-31")

-  Use named placeholders (like ``%(collection_id)s``). This allows you to (1) use the same placeholder multiple times in the query, while only having to pass a single parameter, and (2) edit and re-order your query without re-ordering your parameters.

   .. code-block:: python

      cur.execute("""
          SELECT * FROM release WHERE collection_id = %(collection_id)s
          UNION
          SELECT * FROM record WHERE collection_id = %(collection_id)s AND ocid = %(ocid)s
      """, {'collection_id': 1, 'ocid': 'ocds-213czf-1'})

   **DO NOT** use anonymous placeholders (``%s``):

   .. code-block:: python

      cur.execute("""
          SELECT * FROM release WHERE collection_id = %(collection_id)s
          UNION
          SELECT * FROM record WHERE collection_id = %(collection_id)s AND ocid = %(ocid)s
      """, (1, 1, 'ocds-213czf-1'))

-  If you are writing a query template in which you want to substitute column names or table names, use the ``format`` method and the ``SQL`` and ``Identifier`` classes (`documentation <https://www.psycopg.org/docs/sql.html#module-psycopg2.sql>`__):

   .. code-block:: python

      from psycopg2.sql import SQL, Identifier

      cur.execute(SQL("SELECT * FROM {table}").format(table=Identifier('collection')))

   You can use this together with passing parameters:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {table} WHERE id = %(id)s").format(table=Identifier('collection')), {'id': 1})

   Remember to format the ``SQL()`` object. **DO NOT** format the string itself:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {table} WHERE id = %(id)s".format(table='collection'), {'id': 1})

   **DO NOT** use string interpolation (``%``):

   .. code-block:: python

      cur.execute("SELECT * FROM %s" % 'collection')

   **DO NOT** use string concatenation (``+``):

   .. code-block:: python

      cur.execute("SELECT * FROM " + 'collection')

   **AVOID** using anonymous placeholders:

   .. code-block:: python

      cur.execute(SQL("SELECT * FROM {}".format('collection'))

Script patterns
---------------

-  For builds that involve independent command-line tools, use `Make <https://www.gnu.org/software/make/>`__, and follow `DataMade's Making Data Guidelines <https://github.com/datamade/data-making-guidelines>`__ and `Clark Grubb's Makefile Style Guide <https://clarkgrubb.com/makefile-style-guide>`__. Examples: `standard_profile_template <https://github.com/open-contracting/standard_profile_template>`__
-  If a repository has scripts to set itself up and/or update itself, follow `GitHub's Scripts to Rule Them All <https://github.com/github/scripts-to-rule-them-all>`__. Examples: `deploy <https://github.com/open-contracting/deploy/tree/master/script>`__, `standard_profile_template <https://github.com/open-contracting/standard_profile_template/tree/master/script>`__
-  If a repository requires a command-line tool for management tasks, create an executable script named ``manage.py`` in the root of the repository. (This matches Django.) Examples: `extension_registry <https://github.com/open-contracting/extension_registry/blob/master/manage.py>`__, `deploy <https://github.com/open-contracting/deploy/blob/master/manage.py>`__

Output formats
--------------

We read and write a lot of CSV and JSON files. Their format should be consistent.

CSV
~~~

Use LF (``\n``) as the line terminator. Example:

.. code:: python

   with open(path) as f:
       reader = csv.DictReader(f)
       fieldnames = reader.fieldnames
       rows = [row for row in reader]

   with open(path, 'w') as f:
       writer = csv.DictWriter(f, fieldnames, lineterminator='\n')
       writer.writeheader()
       writer.writerows(rows)

JSON
~~~~

Indent with 2 spaces and preserve order of object pairs. Example:

.. code:: python

   with open(path) as f:
       data = json.load(f)

   with open(path, 'w') as f:
       json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
       f.write('\n')

If (and only if) the code must support Python 3.5 or earlier, use:

.. code:: python

   from collections import OrderedDict

   with open(path) as f:
       data = json.load(f, object_pairs_hook=OrderedDict)

Preferred packages
------------------

We prefer packages in order to:

-  Limit the number of packages with which developers need to be familiar.
-  Re-use code (like Click) instead of writing new code (with argparse).

For :doc:`applications`, we prefer all-inclusive and opinionated packages, because they:

-  Encourage greater similarity and code re-use across projects. With Django, for example, developers are encouraged to use its authentication mechanism. With Flask, each developer can choose a different mechanism, or write their own.
-  Are more robust to changes in scope. For example, you might not need the `Django admin site <https://docs.djangoproject.com/en/3.0/ref/contrib/admin/>`__ on day one, but you'll be happy to have it when it becomes a requirement.

Web framework
  `Django <https://www.djangoproject.com/>`__. Do not use `Flask <https://flask.palletsprojects.com/>`__, except in limited circumstances like generating a static site with `Frozen-Flask <https://pythonhosted.org/Frozen-Flask/>`__.
Command-line interface
  `Click <https://click.palletsprojects.com/>`__, unless a framework provides its own, like `Django <https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/>`__ or `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#custom-project-commands>`__. Do not use `argparse <https://docs.python.org/3/library/argparse.html>`__.
Object Relational Mapper (ORM)
  Django. Do not use `SQLAlchemy <https://www.sqlalchemy.org/>`__, except in low-level libraries with limited scope.
HTTP library
  `Requests <https://requests.readthedocs.io/>`__, unless a framework uses another, like Scrapy (Twisted).
Templating
  `Jinja <https://jinja.palletsprojects.com/>`__
Translation
  `gettext <https://docs.python.org/3/library/gettext.html>`__, `Babel <http://babel.pocoo.org/>`__ and `transifex-client <https://pypi.org/project/transifex-client/>`__, unless a framework provides an interface to these, like `Django <https://docs.djangoproject.com/en/3.0/topics/i18n/>`__ or `Sphinx <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`__.
Logging
  `logging <https://docs.python.org/3/library/logging.html>`__
Testing
  `pytest <https://docs.pytest.org/>`__, unless a framework uses another, like `Django <https://docs.djangoproject.com/en/3.0/topics/testing/>`__ (unittest).
Coverage
  `Coveralls <https://coveralls-python.readthedocs.io/>`__
Documentation
  `Sphinx <https://www.sphinx-doc.org/>`__. Its Markdown extensions should only be used for OCDS documentation.

Maintainers can find dependencies with:

.. code-block:: bash

   find . \( -name 'setup.py' -or -name 'requirements.in' \) -exec echo {} \; -exec cat {} \; 
