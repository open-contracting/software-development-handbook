Documentation
=============

.. note::

   Read the general :doc:`../general/documentation` page.

:doc:`packages` and :doc:`applications` *must* have documentation to describe their usage for an external audience. They *may* have documentation to describe how to contribute. Documentation is written using `Sphinx <https://www.sphinx-doc.org/>`__ in a ``docs`` directory.

:doc:`packages` must have `Sphinx-style docstrings <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists>`__ for public modules, classes and methods, so that Sphinx can automatically generate documentation and so that Python's `help() function <https://docs.python.org/3/library/functions.html#help>`__ can display useful output.

.. note::

   We can consider writing `Architecture Decision Records (ADRs) <https://github.blog/2020-08-13-why-write-adrs/>`__.

Building documentation locally
------------------------------

With Python 3 as your interpreter, install Python modules:

.. code-block:: shell

   pip install sphinx sphinx_rtd_theme

Build the HTML pages:

.. code-block:: shell

   sphinx-build docs docs/_build/html

Run a web server:

.. code-block:: shell

   python -m http.server 8000

Open http://localhost:8000/docs/_build/html/ in your web browser:

.. code-block:: shell

   open http://localhost:8000/docs/_build/html/

.. note::

   If you are using Python 3.7 or greater, you can pass ``-d docs/_build/html`` to the ``python`` command, and open http://localhost:8000/.

.. note::

   Documentation is built in ``docs/_build/html``, to match the location when building with ``make html`` from the ``docs/`` directory.
