General style
=============

You may also refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

.. seealso::

   The :doc:`../services/index` section contains Python-related content for :doc:`../services/postgresql` and :doc:`../services/rabbitmq`.

   :ref:`Organization-wide spell-checking<python-additional-linting>`

Naming
------

   *There are only two hard things in computer science: cache invalidation, naming things and off-by-one errors.*

-  Use ``lower_snake_case`` for everything except constants (``UPPER_SNAKE_CASE``) and classes (``UpperCamelCase``).
-  Use the same terminology as other projects. At minimum, don't use the same term for a different concept.
-  Use terminology from `Enterprise Integration Patterns <https://www.enterpriseintegrationpatterns.com/patterns/messaging/>`__.
-  Don't use "cute" names.

Comments
--------

-  Use sentence case, correct punctuation, and correct capitalization. Do not omit articles.
-  Do not add ``TODO`` comments. Instead, create GitHub issues. TODO's are less visible to the team.

Maintainers can find TODO comments with this command:

.. code-block:: none

   grep -R -i --exclude-dir .git --exclude-dir .sass-cache --exclude-dir .tox --exclude-dir __pycache__ --exclude-dir _build --exclude-dir _static --exclude-dir build --exclude-dir dist --exclude-dir htmlcov --exclude-dir node_modules --exclude-dir sass --exclude-dir LC_MESSAGES --exclude app.js --exclude conf.py '\btodo\b' .

.. _python-type-hints:

Type annotations
----------------

Type hints are especially useful in :doc:`packages<packages>` for :ref:`documentation<python-docstrings>` using Sphinx and linting using `Mypy <https://mypy-lang.org>`__. Use of type hints is optional.

.. note::

   Since Mypy has many open issues for `relatively common scenarios <https://github.com/open-contracting/software-development-handbook/issues/9#issuecomment-975143550>`__, using Mypy to validate your type hints is optional.

Reference: `typing – Support for type hints <https://docs.python.org/3/library/typing.html>`__

Exceptions
----------

-  Do not raise `built-in exceptions <https://docs.python.org/3/library/exceptions.html>`__. Define specific exceptions in an ``exceptions.py`` module. For example:

   .. code-block:: python

      class ProjectNameError(Exception):
          """Base class for exceptions from within this package/application"""


      class SpecificNameError(ProjectNameError):
          """Raised if this clear condition is true"""

-  Do not use a bare ``except:`` or a generic ``except Exception:``. Use specific error classes to avoid handling exceptions incorrectly.
-  Do not catch an exception and raise a new exception, *unless* the new exception has a special meaning (e.g. ``CommandError`` in Django).
-  If an unexpected error occurs within a long-running worker, allow the worker to die. For example, if a worker is failing due to a broken connection, it should not survive to uselessly attempt to reuse that broken connection.

Warnings
--------

-  Do not add or override any methods in a `Warning <https://docs.python.org/3/library/warnings.html>`__ subclass. In particular, do not add required positional arguments to the ``__init__`` method.

   .. admonition:: Why?

      The `warnings.catch_warnings(record=True) <https://docs.python.org/3/library/warnings.html#warnings.catch_warnings>`__ context manager catches instances of ``warnings.WarningMessage``, not instances of the original warning classes. To reissue a warning, you need to do, like in `Apache Airflow <https://github.com/apache/airflow/blob/main/airflow/utils/warnings.py>`__:

      .. code-block:: python

         warnings.warn_explicit(w.message, w.category, w.filename, w.lineno, source=w.source)

      The `warnings.warn_explicit() <https://docs.python.org/3/library/warnings.html#warnings.warn_explicit>`__ function calls `category(message) <https://github.com/python/cpython/blob/v3.10.0/Lib/warnings.py#L345>`__. If the ``_init__`` method is overridden with additional required arguments, a ``TypeError`` is raised, like ``MyWarning.__init__() missing 2 required positional arguments``.

      Because the additional required arguments are unavailable, you can't do:

      .. code-block:: python

         warnings.warn(category(w.message, var1, var2))  # var1 and var2 are indeterminable

-  Call ``warnings.warn(message, category=MyWarning)``, not ``warnings.warn(MyWarning(message))``, to avoid the temptation to add required positional arguments to the ``__init__`` method.
-  ``warnings.catch_warnings(record=True)`` catches all warnings. To reissue warnings you aren't interested in:

   .. code-block:: python

      with warnings.catch_warnings(record=True) as wlist:
          warnings.simplefilter("always", category=MyWarning)

          ...

      for w in wlist:
          if issubclass(w.category, MyWarning):
              ...
          else:
              warnings.warn_explicit(w.message, w.category, w.filename, w.lineno, source=w.source)

-  Subclass from the `UserWarning <https://docs.python.org/3/library/exceptions.html#UserWarning>`__ class, not the ``Warning`` class.

.. seealso::

   `Default warning message f-string <https://github.com/python/cpython/blob/v3.10.0/Lib/warnings.py#L37>`__

Formatted strings
-----------------

.. tip::

   Don't use regular expressions or string methods to parse and construct filenames and URLs.

   Use the `pathlib <https://docs.python.org/3/library/pathlib.html#module-pathlib>`__ (or `os.path <https://docs.python.org/3/library/os.path.html>`__) module to parse or construct filenames, for cross-platform support.

   Use the `urllib.parse <https://docs.python.org/3/library/urllib.parse.html>`__ module to parse and construct URLs, notably: `urlsplit <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit>`__ (not ``urlparse``), `parse_qs <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qs>`__, `urljoin <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin>`__ and `urlencode <https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode>`__. To replace part of a URL parsed with the ``urlsplit`` function, use its `_replace <https://docs.python.org/3/library/collections.html#collections.somenamedtuple._replace>`__ method. `See examples <https://docs.python.org/3/library/urllib.request.html#urllib-examples>`__.

..
   To find unexpected use of pathlib or os.path around __file__:

   (?<!os\.path\.dirname\(os\.path\.realpath\()__file__(?!\)\.resolve\(\)\.parent)

.. seealso::

   How to construct :ref:`SQL statements<sql-statements>`

`Format strings <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`__ (f-strings), introduced in Python 3.6 via `PEP 498 <https://peps.python.org/pep-0498/>`__, are preferred for interpolation of variables:

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

   message = f"""Is '{person["name"]}' correct?"""  # AVOID

There are two cases in which f-strings and ``str.format()`` are not preferred:

.. _string-logging-i18n:

Logging
  `"Formatting of message arguments is deferred until it cannot be avoided." <https://docs.python.org/3/howto/logging.html#optimization>`__ If you write:

  .. code-block:: python

     logger.debug("hello {}".format("world"))  # WRONG

  then ``str.format()`` is called whether or not the message is logged. Instead, please write:

  .. code-block:: python

     logger.debug("hello %s", "world")
Internationalization (i18n)
  String extraction in most projects is done by the ``xgettext`` command, which doesn't support f-strings. To have a single syntax for translated strings, use named placeholders and the ``%`` operator, as recommended by `Django <https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#standard-translation>`__. For example:

  .. code-block:: python

     _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}

  Remember to put the ``%`` operator outside, not inside, the ``_()`` call:

  .. code-block:: python

     _('Today is %(month)s %(day)s.' % {'month': m, 'day': d})  # WRONG

.. note::

   To learn how to use or migrate between ``%`` and ``format()``, see `pyformat.info <https://pyformat.info/>`__.

Maintenance
~~~~~~~~~~~

Maintainers can find improper formatting with these regular expressions. Test directories and Sphinx ``conf.py`` files can be ignored, if needed.

-  Unnamed placeholders, except for log messages, ``strftime()``, `psycopg2.extras.execute_values() <https://www.psycopg.org/docs/extras.html#psycopg2.extras.execute_values>`__ and common false positives (e.g. ``%`` in ``SECRET_KEY`` default value):

   .. code-block:: none

      (?<!info)(?<!debug|error)(?<!getenv)(?<!warning)(?<!critical|strftime)(?<!exception)(?<!execute_values)\((\n( *['"#].*)?)* *['"].*?%[^( ]

-  Named placeholders, except for translation strings and :ref:`SQL statements<sql-statements>`:

   .. code-block:: none

      (?<!\b[t_])(?<!one|all)(?<!pluck)(?<!gettext|execute|sql\.SQL)\((\n( *['"#].*)?)* *['"].*?%\(

-  Named placeholders, with incorrect position of ``%`` operator (trailing space):

   .. code-block:: none

      %\(.+(?<!\) )% 

-  Log messages using f-strings or ``str.format()`` (case-sensitive), ignoring the `extra keyword argument <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`__, `ArgumentParser.error <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.error>`__ and `Directive.error <https://docutils.sourceforge.io/docs/howto/rst-directives.html#error-handling>`__:

   .. code-block:: none

      ^( *)(?:\S.*)?\b(?<!self\.)(?<!subparser\.)_?(?:debug|info|warning|error|critical|exception)\((?:\n(\1 .+)?)*.*?(?<!extra=){

-  Translation strings using f-strings or ``str.format()``:

   .. code-block:: none

      ^( *)(?:\S.*)?(?:\b__?|gettext|lazy)\((?:\n(\1 .+)?)*.*?(?<!% ){

-  Remaining occurrences of ``str.format()``:

   .. code-block:: none

      [^\w\]]\.format\(

To correct any remaining occurrences of ``str.format()``, use these patterns and replacements:

.. list-table::
   :header-rows: 1

   * - Pattern
     - Replacement
   * - ``("[^"]*?{)(}[^"]*")\.format\(([\w.]+)\)``
     - ``f$1$3$2``
   * - ``('[^']*?{)(}[^']*')\.format\(([\w.]+)\)``
     - ``f$1$3$2``
   * - ``("[^"]*?{)(}[^"]*?{)(}[^"]*")\.format\(([\w.]+), ([\w.]+)\)``
     - ``f$1$4$2$5$3``
   * - ``('[^']*?{)(}[^']*?{)(}[^']*')\.format\(([\w.]+), ([\w.]+)\)``
     - ``f$1$4$2$5$3``
   * - ``("[^"]*?{)(}[^"]*?{)(}[^']*?{)(}[^"]*?")\.format\(([\w.]+), ([\w.]+), ([\w.]+)\)``
     - ``f$1$5$2$6$3$7$4``
   * - ``('[^']*?{)(}[^']*?{)(}[^']*?{)(}[^']*?')\.format\(([\w.]+), ([\w.]+), ([\w.]+)\)``
     - ``f$1$5$2$6$3$7$4``

Long strings
------------

For cases in which whitespace has no effect, like SQL statements, use multi-line strings:

.. code-block:: python

   cursor.execute("""
       SELECT *
       FROM table
       WHERE id > 1000
   """)

For cases in which whitespace changes the output, like log messages, use consecutive strings:

.. code-block:: python

   logger.info(
       "A line with up to 119 characters. Use consecutive strings, one on each line, without `+` operators or join "
       "methods. Do not start a string with a space. Instead, append it to the previous string. If the message has "
       "multiple sentences, do not break the line at punctuation."
   )

However, in some cases, it might be easier to edit in the form:

.. code-block:: python

   from textwrap import dedent

   content = dedent("""\
   # Heading

   A long paragraph.

   - Item 1
   - Item 2
   - Item 3
   """)

Maintainers can find improper use of multi-line strings with this regular expression:

.. code-block:: none

   (?<!all|raw)(?<!dedent)(?<!execute)\((\n( *)(#.*)?)*"""

Data structures
---------------

.. admonition:: Reference

   `Data Structures <https://docs.python.org/3/tutorial/datastructures.html>`__

-  To test whether a value equals one of many literals, use a set (not a tuple or list), because a set is fastest. For example:

   .. code-block:: python

      if status in {"cancelled", "unsuccessful"}:
          pass

-  To iterate over manually composed values, use a tuple (not a list or dict), because a tuple is simplest, because it is immutable. For example:

   .. code-block:: python

      for subject, index, column in (
          ("Buyer", 2, "buyer_id"),
          ("ProcuringEntity", 3, "procuring_entity_id"),
          ("Tenderer", 4, "tenderer_id"),
      ):
          pass

Default values
~~~~~~~~~~~~~~

Use ``dict.setdefault`` instead of a simple if-statement. A simple if-statement has no ``elif`` or ``else`` branches, and a single statement in the ``if`` branch.

.. code-block:: python

   data.setdefault('key', 1)

.. code-block:: python

   if 'key' not in data:  # AVOID
       data['key'] = 1

Maintainers can find simple if-statements with this regular expression:

.. code-block:: none

   ^( *)if (.+) not in (.+):(?: *#.*)?\n(?: *#.*\n)* +\3\[\2\] = .+\n(?!(?: *#.*\n)*\1(else\b|elif\b|    \S))

Input/Output
------------

.. code-block:: python

   import sys

   print('message', file=sys.stderr)
   sys.stderr.write('message\n')  # WRONG

.. seealso::

   :doc:`file_formats`

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

.. _object-oriented:

Object-oriented style
---------------------

Don't force polymorphism and inheritance, especially if it sacrifices performance, maintainability or readability.

Python provides encapsulation via modules. As such, functions are preferred to classes where appropriate.

.. seealso::

   `"Clean" Code, Horrible Performance <https://www.youtube.com/watch?v=tD5NrevFtbU>`__

.. epigraph::

   The primary feature for easy maintenance is locality: Locality is that characteristic of source code that enables a programmer to understand that source by looking at only a small portion of it.

   -- `Richard Gabriel <https://www.dreamsongs.com/Files/PatternsOfSoftware.pdf>`__

Maintainers can find class hierarchies, excluding those imposed by dependencies (Click, Docutils, Django, Django REST Framework, and standard libraries), with this regular expression:

.. code-block:: none

   \bclass \S+\((?!(AdminConfig|AppConfig|Directive|Exception|SimpleTestCase|TestCase|TransactionTestCase|json\.JSONEncoder|yaml.SafeDumper)\b|(admin|ast|click|forms|migrations|models|nodes|serializers|template|views|viewsets)\.|\S+(Command|Error|Warning)\b)

Simple statements
-----------------

.. admonition:: Reference

   `Simple statements <https://docs.python.org/3/reference/simple_stmts.html>`__

-  Never use relative ``import``.

Standard library
----------------

.. admonition:: Reference

   `The Python Standard Library <https://docs.python.org/3/library/>`__

-  Use `@dataclass <https://docs.python.org/3/library/dataclasses.html>`__ for simple classes only. Using ``@dataclass`` with inheritance, mixins, class variables, etc. tends to increase complexity.

.. _python-scripts:

Scripts
-------

If a repository requires a command-line tool for management tasks, create an executable script named ``manage.py`` in the root of the repository. (This matches Django.)

If you are having trouble with the Python path, try running the script with ``python -m script_module``, which will add the current directory to ``sys.path``.

**Examples**: `extension_registry <https://github.com/open-contracting/extension_registry/blob/main/manage.py>`__, `deploy <https://github.com/open-contracting/deploy/blob/main/manage.py>`__

.. seealso::

   :doc:`Shell script guide<../shell/index>`
