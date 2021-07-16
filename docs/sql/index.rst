SQL
===

Code style
----------

Style SQL files with `pg_format <https://github.com/darold/pgFormatter>`__, which has web and command-line interfaces.

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
