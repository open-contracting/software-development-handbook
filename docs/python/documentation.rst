Documentation
=============

:doc:`packages` and applications *must* have documentation to describe their usage for an external audience. They *may* have documentation to describe how to contribute. Documentation is written using `Sphinx <https://www.sphinx-doc.org/en/master/>`__ in a ``docs`` directory.

:doc:`packages` must have `Sphinx-style docstrings <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists>`__ for public modules, classes and methods, so that Sphinx can automatically generate documentation and so that Python's `help() function <https://docs.python.org/3/library/functions.html#help>`__ can display useful output.

.. seealso::

   :doc:`General documentation guide<../general/documentation>`

.. note::

   We can consider writing `Architecture Decision Records (ADRs) <https://github.blog/2020-08-13-why-write-adrs/>`__.

Build documentation locally
---------------------------

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

Check broken links
------------------

Sphinx's `linkcheck <https://www.sphinx-doc.org/en/master/usage/builders/index.html#sphinx.builders.linkcheck.CheckExternalLinksBuilder>`__ builder reports redirects, error codes and non-existing anchors. It cannot be `configured <https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder>`__ to report only error codes. As such, it is tedious to include in :doc:`continuous integration<ci>` outside OCDS documentation, and to configure for manual invocation.

To check broken links, run:

.. code-block:: shell

   sphinx-build -q -b linkcheck docs _linkcheck

Review the broken links in the ``_linkcheck/output.txt`` file:

.. code-block:: shell

   cat _linkcheck/output.txt

.. _readthedocs:

Create a ReadTheDocs project
----------------------------

#. Sign in to `ReadTheDocs <https://readthedocs.org/dashboard/>`__
#. Click *Import a Project*
#. Click *Import Manually*

   #. Enter the name of the repository in *Name*
   #. Paste the URL of the repository in *Repository URL*
   #. Enter "main" in *Default branch*
   #. Check *Edit advanced project options*
   #. Click *Next*

#. Set *Programming language* to "Python"
#. Click *Finish*
#. Click *Admin*
#. Click *Advanced Settings*

   #. Uncheck *Enable PDF build*
   #. Uncheck *Enable EPUB build*
   #. Click *Save*

#. Click *Notifications*

   #. Enter "sysadmin@open-contracting.org" in *Email*
   #. Click *Add*

#. Click *Versions*

   #. Click *Edit* for the *stable* version
   #. Uncheck *Active*
   #. Click *Save*

Redirect a ReadTheDocs project
------------------------------

#. Replace ``docs/_templates/layout.html`` with the below, replacing ``SUBDOMAIN``:

   .. code-block:: html

      <!DOCTYPE html>
      <html>
      <head>
          <meta charset="utf8">
          <meta http-equiv="refresh" content="0; url=https://SUBDOMAIN.readthedocs.io/">
          <link rel="canonical" href="https://SUBDOMAIN.readthedocs.io/">
          <title>This page has moved</title>
      </head>
      <body>
          <p>This page has moved. Redirecting you to <a href="https://SUBDOMAIN.readthedocs.io/">https://SUBDOMAIN.readthedocs.io/</a>&hellip;</p>
      </body>
      </html>

#. Push the change to build the documentation
#. Sign in to `ReadTheDocs <https://readthedocs.org/dashboard/>`__
#. Click on the project
#. Click *Admin*
#. Click *Integrations*
#. Click *GitHub incoming webhook*
#. Click *Delete webhook*
