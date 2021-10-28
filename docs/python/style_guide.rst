General
=======

Version
-------

Code is written for Python 3.6 and above (`see the status of Python branches <https://devguide.python.org/#branchstatus>`__).

.. _common-checks:

Common checks
-------------

All code is checked as documented by `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Repositories should not use ``setup.cfg``, ``pyproject.toml``, ``.editorconfig`` or tool-specific files to configure the behavior of tools, except to ignore generated files like database migrations. Maintainers can find configuration files with:

.. code-block:: shell

   find . \( -name setup.cfg -or -name pyproject.toml -or -name .editorconfig -or -name .flake8 -or -name .isort.cfg -or -name .pylintrc -or -name pylintrc -or -name pytest.ini \) -not -path '*/node_modules/*' -exec bash -c 'sha=$(shasum {} | cut -d" " -f1); if [[ ! "4b679b931113f9a779bfea5e8c55cea40f8a5efe 1031acedc073ce860655c192071a0b0ad7653919" =~ $sha ]]; then echo -e "\n\033[0;32m{}\033[0m"; echo $sha; cat {}; fi' \;

..
   The shasums are:

   4b679b931113f9a779bfea5e8c55cea40f8a5efe minimal pyproject.toml file for Black
   1031acedc073ce860655c192071a0b0ad7653919 minimal setup.cfg file for Black

.. note::

   If a project uses `Black <https://black.readthedocs.io/en/stable/>`__, it needs a ``setup.cfg`` file for `flake8 <https://github.com/PyCQA/flake8/issues/234>`__ and ``isort`` and a ``pyproject.toml`` file for `black <https://github.com/psf/black/issues/683>`__. Otherwise, use only a ``setup.cfg`` file. Black is not used in all projects, because its `vertical style <https://github.com/open-contracting/standard-maintenance-scripts/issues/148#issuecomment-693556236>`__ is slower to scan.

``noqa`` comments should be kept to a minimum, and should reference the specific error, to avoid shadowing another error: for example, ``# noqa: E501``. The errors that are allowed to be ignored are:

-  ``E501 line too long`` for long strings, especially URLs
-  ``F401 module imported but unused`` in a library's top-level ``__init__.py`` file
-  ``W291 Trailing whitespace`` in tests relating to trailing whitespace
-  ``isort:skip`` if ``sys.path`` needs to be changed before an import

Maintainers can find unwanted ``noqa`` comments with this regular expression: ``# noqa(?!(: (E501|F401|W291)| isort:skip)\n)``

Otherwise, please refer to common guidance like the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.

Optional checks
---------------

flake8's ``--max-complexity`` option (provided by `mccabe <https://pypi.org/project/mccabe/>`__) is deactivated by default. A threshold of 10 or 15 is `recommended <https://en.wikipedia.org/wiki/Cyclomatic_complexity#Limiting_complexity_during_development>`__:

.. code-block:: shell

   flake8 . --max-line-length 119 --max-complexity 10

`pylint <https://pylint.org/>`__ and `pylint-django <https://pypi.org/project/pylint-django/>`__ provides useful, but noisy, feedback:

.. code-block:: shell

   pip install pylint
   pylint --max-line-length 119 directory

The `Python Code Quality Authority <https://github.com/PyCQA>`__ maintains ``flake8`` (which includes ``mccabe``, ``pycodestyle`` and ``pyflakes``), ``isort`` and ``pylint``.

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

.. _string-logging:

Logging
  `"Formatting of message arguments is deferred until it cannot be avoided." <https://docs.python.org/3/howto/logging.html#optimization>`__. If you write:

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

Default values
--------------

Use ``dict.setdefault`` instead of a simple if-statement. A simple if-statement has no ``elif`` or ``else`` branches, and a single statement in the ``if`` branch.

.. code-block:: python

   data.setdefault('key', 1)

.. code-block:: python

   if 'key' not in data:  # AVOID
       data['key'] = 1

Maintainers can find simple if-statements with this regular expression: ``^( *)if (.+) not in (.+):(?: *#.*)?\n(?: *#.*\n)* +\3\[\2\] = .+\n(?!(?: *#.*\n)*\1(else\b|elif\b|    \S))``

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

.. note::

   Read the general :doc:`../shell/index` content.

If a repository requires a command-line tool for management tasks, create an executable script named ``manage.py`` in the root of the repository. (This matches Django.)

**Examples**: `extension_registry <https://github.com/open-contracting/extension_registry/blob/main/manage.py>`__, `deploy <https://github.com/open-contracting/deploy/blob/main/manage.py>`__

.. _python-tests:

Tests
-----

Test code tends to be written once and only read when the test fails. As a result, test code tends to be poorly written, with a lot of copy-pasting between test methods, which makes intent unclear.

To write clear tests:

-  Test one scenario per test.
-  Name tests, fixtures, and mocks descriptively. Do not suffix them ``1``, ``2``, ``3``, etc.
-  Use `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__ to test something with different inputs (like in `OCDS Kit <https://github.com/open-contracting/ocdskit/blob/main/tests/test_util.py>`__).
-  Use `pytest.fixture <https://docs.pytest.org/en/stable/fixture.html>`__ to re-use test scaffolding (like in `OCDS Merge <https://github.com/open-contracting/ocds-merge/blob/main/tests/conftest.py>`__ or `Kingfisher Colab <https://github.com/open-contracting/kingfisher-colab/blob/main/tests/conftest.py>`__).
-  Use `unittest.TestCase <https://docs.python.org/3/library/unittest.html#unittest.TestCase>`__ to re-use testing logic, including:

   -  Test methods (like `ViewTests <https://github.com/open-contracting/toucan/blob/main/tests/__init__.py>`__ in Toucan)
   -  Test scaffolding, using `setUp() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp>`__ and `tearDown() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown>`__

Note: There are some `caveats <https://docs.pytest.org/en/stable/unittest.html>`__ to using ``pytest`` with ``unittest``.

.. seealso::

   :ref:`Test file naming and directory layout<layout-tests>`
