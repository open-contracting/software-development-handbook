Style guide
===========

Code is written for Python 3.6 and above (`see the status of Python branches <https://devguide.python.org/#branchstatus>`__).

Common checks
-------------

All code is checked as documented by `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Repositories should not use ``setup.cfg``, ``.editorconfig``, ``pyproject.toml`` or tool-specific files to configure the behavior of tools, except to ignore generated files like database migrations. Maintainers can find configuration files with:

.. code-block:: shell-session

   find . \( -name 'setup.cfg' -or -name 'pyproject.toml' -or -name '.editorconfig' -or -name '.flake8' -or -name '.isort.cfg' -or -name '.pylintrc' -or -name '.pylintrc' \) -exec echo {} \; -exec cat {} \;

.. note::

   If a project uses `Black <https://black.readthedocs.io>`__ it needs a ``setup.cfg`` file for `flake8 <https://gitlab.com/pycqa/flake8/-/issues/428>`__ and ``isort`` and a ``pyproject.toml`` file for `black <https://github.com/psf/black/issues/683>`__. Otherwise, use only a ``setup.cfg`` file.

``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``. The errors that are allowed to be ignored are:

-  ``E501 line too long`` for long strings, especially URLs
-  ``F401 module imported but unused`` in a library's top-level ``__init__.py`` file
-  ``W291 Trailing whitespace`` in tests relating to trailing whitespace
-  ``isort:skip`` if ``sys.path`` needs to be changed before an import

Maintainers can find unwanted ``noqa`` comments with this regular expression: ``# noqa(?!(: (E501|F401|W291)| isort:skip)\n)``.

Otherwise, please refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

Optional checks
---------------

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: shell-session

   flake8 . --max-line-length 119 --max-complexity 10

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: shell-session

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``. Its other tools, for your consideration, include `pydocstyle <http://pydocstyle.org/>`__ (docstrings), `doc8 <https://pypi.org/project/doc8/>`__ (RST files), `bandit <https://bandit.readthedocs.io/en/latest/>`__ (security issues) and `flake8-bugbear <https://pypi.org/project/flake8-bugbear/>`__ (additional checks).

String formatting
-----------------

`Format strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`__ (f-strings), introduced in Python 3.6 via `PEP 498 <https://www.python.org/dev/peps/pep-0498/>`__, are preferred for interpolation of variables:

.. code-block:: python

   message = f"hello {name}"

For interpolation of expressions, the `str.format() <https://docs.python.org/3/library/string.html#formatstrings>`__ method is preferred if it is easier to read and write. For example:

.. code-block:: python

   message = "Is '{name}' correct?".format(name=person["name"])

or:

.. code-block:: python

   message = "Is '{person[name]}' correct?".format(person=person)

is easier to write than:

.. code-block:: python

   message = f"""Is '{person["name"]}' correct?"""

There are two cases in which f-strings and ``str.format()`` are not preferred:

Logging
  `"Formatting of message arguments is deferred until it cannot be avoided." <https://docs.python.org/3/howto/logging.html#optimization>`__. If you write:

  .. code-block:: python

     logger.debug("hello {}".format("world"))  # WRONG

  then ``str.format()`` is called whether or not the message is logged. Instead, please write:

  .. code-block:: python

     logger.debug("hello %s", "world")
Internationalization (i18n)
  String extraction in most projects is done by the ``xgettext`` command, which doesn't support f-strings. To have a single syntax for translated strings, use named placeholders and the ``%`` operator, as recommended by `Django <https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#standard-translation>`__. For example:

  .. code-block:: python

     _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}

  Remember to put the ``%`` operator outside, not inside, the ``_()`` call:

  .. code-block:: python

     _('Today is %(month)s %(day)s.' % {'month': m, 'day': d})  # WRONG

.. note::

   To learn how to use or migrate between ``%`` and ``format()``, see `pyformat.info <https://pyformat.info/>`__.

SQL statements
--------------

Follow `best practices <https://www.psycopg.org/docs/usage.html#sql-injection>`__ to avoid accidental errors and `SQL injection <https://en.wikipedia.org/wiki/SQL_injection>`__.

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
          SELECT * FROM release WHERE collection_id = %(collection_id)s
          UNION
          SELECT * FROM record WHERE collection_id = %(collection_id)s AND ocid = %(ocid)s
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

Scripts
-------

.. note::

   Read the general :ref:`scripts` content.

If a repository requires a command-line tool for management tasks, create an executable script named ``manage.py`` in the root of the repository. (This matches Django.)

**Examples**: `extension_registry <https://github.com/open-contracting/extension_registry/blob/master/manage.py>`__, `deploy <https://github.com/open-contracting/deploy/blob/master/manage.py>`__
