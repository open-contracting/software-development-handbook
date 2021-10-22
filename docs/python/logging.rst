Logging
=======

The `logging <https://docs.python.org/3/library/logging.html>`__ module is :doc:`preferred<preferences>`.

.. seealso::

   :ref:`String formatting style guide<string-logging>`

.. _logging-name:

Name
----

In most cases, use ``logger = logging.getLogger(__name__)``, as `recommended <https://docs.python.org/3/library/logging.html#logger-objects>`__.

If a file is run directly, ``__name__`` will be ``"__main__"``, which is less informative. In such cases, you can use the name of the module, like ``"checker.dataset"`` in `Pelican Backend <https://github.com/open-contracting/pelican-backend>`__, or you can include the name of the sub-command, like ``"ocdskingfisher.summarize.add"`` in `Kingfisher Summarize <https://github.com/open-contracting/kingfisher-summarize/blob/main/manage.py>`__.

If a command-line tool logs messages to give user feedback, we typically use the name of the command, like ``"oc4ids"``, ``"ocdskit"``, ``"ocdsextensionregistry"`` and ``"spoonbill"``.

Format
------

In the context of web servers and worker daemons, the `formatter <https://docs.python.org/3/library/logging.html#formatter-objects>`__'s format string should be set to:

.. code-block:: python

   "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s"

In most cases, the other `placeholders <https://docs.python.org/3/library/logging.html#logrecord-attributes>`__ are unnecessary:

-  If the logger's :ref:`name<logging-name>` is ``__name__``, then ``%(name)s`` covers ``%(module)s`` (identical), ``%(pathname)s`` (too long) and ``%(filename)s`` (too short).
-  ``%(funcName)s``, unless ``%(name)s``, ``%(lineno)s`` and ``%(message)s`` are insufficient to locate the relevant code.
-  ``%(process)s`` and ``%(thread)s``, unless the log messages from different processes/threads are written to the same location.

To configure the format in `Django <https://docs.djangoproject.com/en/3.2/topics/logging/#configuring-logging>`__:

.. code-block:: python

   LOGGING = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "console": {
               "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
           },
       },
       "handlers": {
           "console": {
               "class": "logging.StreamHandler",
               "formatter": "console",
           },
       },
       "loggers": {
           "": {
               "handlers": ["console"],
               "level": "INFO",
           },
           "mymodule": {
              "handlers": ["console"],
              "level": "DEBUG",
           },
       },
   }

To configure the format in general:

.. code-block:: python

   import logging

   logger = logging.getLogger(__name__)
   formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s")
   logger.setFormatter(formatter)

Methods
-------

Use the corresponding `method <https://docs.python.org/3/library/logging.html#logging.Logger.debug>`__ for the appropriate `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`__.

When logging messages inside an ``except`` clause, if the error is unexpected and isn't re-raised, use `logger.exception(msg) <https://docs.python.org/3/library/logging.html#logging.Logger.exception>`__ to log the message at the ``ERROR`` level along with exception information. Do not bother with the ``traceback`` module.

Maintainers can review loggers inside ``except`` branches with this regular expression: ``except (?!RecoverableException).+\n( +)(\S.*\n(\1.*\n)*\1)?.*log.*\.(?!exception\(|format\()``

Configuration
-------------

Loggers are organized into a `hierarchy <https://docs.python.org/3/library/logging.html#logger-objects>`__. As such, you can configure only the root logger (its name is ``''`` in Django, or ``None`` in general), or only the loggers for top-level modules (like only ``a``, instead of both ``a.b`` and ``a.c``).

Reference
---------

-  `Django's default logging configuration <https://github.com/django/django/blob/main/django/utils/log.py>`__
-  `Python's warnings.py format string <https://github.com/python/cpython/blob/v3.10.0/Lib/warnings.py#L37>`__
