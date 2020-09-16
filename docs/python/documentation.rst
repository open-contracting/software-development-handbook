Documentation
=============

.. note::

   Read the general :doc:`../general/documentation` page.

Packages and applications must have documentation to describe their usage for an external audience. They may have documentation to describe how to contribute. Documentation is written using `Sphinx <https://www.sphinx-doc.org/>`__ in a ``docs`` directory.

Packages must have `Sphinx-style docstrings <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists>`__ for public modules, classes and methods, so that Sphinx can automatically generate documentation and so that Python's `help() function <https://docs.python.org/3/library/functions.html#help>`__ can display useful output.

.. note::

   We can consider writing `Architecture Decision Records (ADRs) <https://github.blog/2020-08-13-why-write-adrs/>`__.
