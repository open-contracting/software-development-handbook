General style
=============

You may also refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

.. seealso::

   The :doc:`../services/index` section contains Python-related content for :doc:`../services/postgresql` and :doc:`../services/rabbitmq`.

Comments
--------

-  Use sentence case, correct punctuation, and correct capitalization. Do not omit articles.
-  Do not add ``TODO`` comments. Instead, create GitHub issues. TODO's are less visible to the team.

Maintainers can find TODO comments with this command:

.. code-block:: none

   grep -R -i --exclude-dir .git --exclude-dir .sass-cache --exclude-dir .tox --exclude-dir __pycache__ --exclude-dir _build --exclude-dir _static --exclude-dir build --exclude-dir dist --exclude-dir htmlcov --exclude-dir node_modules --exclude-dir sass --exclude-dir LC_MESSAGES --exclude app.js --exclude conf.py '\btodo\b' .

Exception handling
------------------

-  Do not use a bare ``except:`` or a generic ``except Exception:``. Use specific error classes to avoid handling exceptions incorrectly.
-  If an unexpected error occurs within a long-running worker, allow the worker to die. For example, if a worker is failing due to a broken connection, it should not survive to uselessly attempt to re-use that broken connection.

String formatting
-----------------

.. tip::

   Use Python's standard library instead of regular expressions or string methods to parse and construct filenames and URLs.

   Use the `os.path <https://docs.python.org/3/library/os.path.html>`__ or `pathlib <https://docs.python.org/3/library/pathlib.html#module-pathlib>`__ module to parse or construct filenames. This promotes cross-platform support.

   Use the `urllib.parse <https://docs.python.org/3.8/library/urllib.parse.html>`__ module to parse and construct URLs, notably `urlsplit <https://docs.python.org/3.8/library/urllib.parse.html#urllib.parse.urlsplit>`__ (not ``urlparse``), `parse_qs <https://docs.python.org/3.8/library/urllib.parse.html#urllib.parse.parse_qs>`__, `urljoin <https://docs.python.org/3.8/library/urllib.parse.html#urllib.parse.urljoin>`__ and `urlencode <https://docs.python.org/3.8/library/urllib.parse.html#urllib.parse.urlencode>`__. When constructing URLs, this ensures a properly encoded query string and avoids missing or extra ``/`` characters between the base URL and URL path. To replace part of a URL parsed with the ``urlsplit`` function, use its `_replace <https://docs.python.org/3/library/collections.html#collections.somenamedtuple._replace>`__ method. `See examples <https://docs.python.org/3.8/library/urllib.request.html#urllib-examples>`__.

.. seealso::

   How to construct :ref:`SQL statements<sql-statements>`

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

.. _string-logging:

Logging
  `"Formatting of message arguments is deferred until it cannot be avoided." <https://docs.python.org/3/howto/logging.html#optimization>`__ If you write:

  .. code-block:: python

     logger.debug("hello {}".format("world"))  # WRONG

  then ``str.format()`` is called whether or not the message is logged. Instead, please write:

  .. code-block:: python

     logger.debug("hello %s", "world")
Internationalization (i18n)
  String extraction in most projects is done by the ``xgettext`` command, which doesn't support f-strings. To have a single syntax for translated strings, use named placeholders and the ``%`` operator, as recommended by `Django <https://docs.djangoproject.com/en/3.2/topics/i18n/translation/#standard-translation>`__. For example:

  .. code-block:: python

     _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}

  Remember to put the ``%`` operator outside, not inside, the ``_()`` call:

  .. code-block:: python

     _('Today is %(month)s %(day)s.' % {'month': m, 'day': d})  # WRONG

.. note::

   To learn how to use or migrate between ``%`` and ``format()``, see `pyformat.info <https://pyformat.info/>`__.

Maintainers can find improper formatting with this regular expression:

.. code-block:: none

   [^\w\]]\.format\(

To correct formatting, the following patterns and replacements can be used:

.. list-table::
   :header-rows: 1

   * - Pattern
     - Replacement
   * - ``('[^']*?{)(}[^']*')\.format\(([\w.]+)\)``
     - ``f$1$3$2``
   * - ``("[^"]*?{)(}[^"]*")\.format\(([\w.]+)\)``
     - ``f$1$3$2``
   * - ``('[^']*?{)(}[^']*?{)(}[^']*')\.format\(([\w.]+), ([\w.]+)\)``
     - ``f$1$4$2$5$3``
   * - ``("[^"]*?{)(}[^"]*?{)(}[^"]*")\.format\(([\w.]+), ([\w.]+)\)``
     - ``f$1$4$2$5$3``
   * - ``('[^']*?{)(}[^']*?{)(}[^']*?{)(}[^']*?')\.format\(([\w.]+), ([\w.]+), ([\w.]+)\)``
     - ``f$1$5$2$6$3$7$4``
   * - ``("[^"]*?{)(}[^"]*?{)(}[^']*?{)(}[^"]*?")\.format\(([\w.]+), ([\w.]+), ([\w.]+)\)``
     - ``f$1$5$2$6$3$7$4``

Default values
--------------

Use ``dict.setdefault`` instead of a simple if-statement. A simple if-statement has no ``elif`` or ``else`` branches, and a single statement in the ``if`` branch.

.. code-block:: python

   data.setdefault('key', 1)

.. code-block:: python

   if 'key' not in data:  # AVOID
       data['key'] = 1

Maintainers can find simple if-statements with this regular expression:

.. code-block:: none

   ^( *)if (.+) not in (.+):(?: *#.*)?\n(?: *#.*\n)* +\3\[\2\] = .+\n(?!(?: *#.*\n)*\1(else\b|elif\b|    \S))

Functional style
----------------

``itertools``, ``filter()`` and ``map()`` can be harder to read, less familiar, and longer. On PyPy, they can also be `slower <https://www.pypy.org/performance.html>`__.

Instead of using ``filter()`` and ``map()`` with a lambda expression, you can use a list comprehension in most cases. For example:

.. code-block:: python

   output = list(filter(lambda x: x < 10, xs))  # AVOID

.. code-block:: python

   output = [x for x in xs if x < 10]

.. code-block:: python

   output = list(map(lambda x: f'a strong with {x}', xs))  # AVOID

.. code-block:: python

   output = [f'a string with {x}' for x in xs]

That said, it is fine to do:

.. code-block:: python

   output = map(str, xs)

.. _python-scripts:

Scripts
-------

If a repository requires a command-line tool for management tasks, create an executable script named ``manage.py`` in the root of the repository. (This matches Django.)

If you are having trouble with the Python path, try running the script with ``python -m script_module``, which will add the current directory to ``sys.path``.

**Examples**: `extension_registry <https://github.com/open-contracting/extension_registry/blob/main/manage.py>`__, `deploy <https://github.com/open-contracting/deploy/blob/main/manage.py>`__

.. seealso::

   :doc:`Shell script guide<../shell/index>`

Input/Output
------------

.. code-block:: python

   import sys

   print('message', file=sys.stderr)
   sys.stderr.write('message\n')  # WRONG

.. seealso::

   :doc:`file_formats`
