Documentation
=============

:doc:`packages` and applications *must* have documentation to describe their usage for an external audience. They *may* have documentation to describe how to contribute.

Documentation is written using `Sphinx <https://www.sphinx-doc.org/en/master/>`__ in a ``docs`` directory.

.. seealso::

   :doc:`General documentation guide<../general/documentation>`

.. note::

   We can consider writing `Architecture Decision Records (ADRs) <https://github.blog/2020-08-13-why-write-adrs/>`__.

.. _python-docstrings:

Write docstrings
----------------

:doc:`packages` must have `Sphinx-style docstrings <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists>`__ for public modules, classes and methods, so that Sphinx can generate documentation and so that Python's `help() function <https://docs.python.org/3/library/functions.html#help>`__ can display useful output.

Use the imperative mood (per `PEP 257 <https://peps.python.org/pep-0257/#one-line-docstrings>`__) in new projects. If an existing project uses the present tense, stay consistent.

Type hints are preferred to ``type``, ``rtype`` and ``vartype`` fields. Use `autodoc_type_aliases <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_type_aliases>`__ to simplify long type hints (`related <https://github.com/sphinx-doc/sphinx/issues/8934>`__). Use `intersphinx_mapping <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_mapping>`__ to link types from other packages. See :ref:`python-type-hints`.

.. note::

   Sphinx does not read ``.pyi`` files, so all type hints must be in the ``.py`` files (`issue <https://github.com/sphinx-doc/sphinx/issues/7630>`__/`pull <https://github.com/sphinx-doc/sphinx/pull/4824>`__).

.. seealso::

   :doc:`linting`

Build documentation locally
---------------------------

Install requirements:

.. code-block:: bash

   pip install sphinx-autobuild -r docs/requirements.txt

Build the HTML pages:

.. code-block:: bash

   sphinx-autobuild -q docs docs/_build/html --watch .

Open http://127.0.0.1:8000/ in your web browser.

.. note::

   Documentation is built in ``docs/_build/html``, like when building with ``make html`` from the ``docs/`` directory.

Check broken links
------------------

Sphinx's `linkcheck <https://www.sphinx-doc.org/en/master/usage/builders/#sphinx.builders.linkcheck.CheckExternalLinksBuilder>`__ builder reports redirects, error codes and non-existing anchors. It cannot be `configured <https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder>`__ to report only error codes. As such, it is tedious to include in :doc:`continuous integration<ci>` outside OCDS documentation, and to configure for manual invocation.

To check broken links, run:

.. code-block:: bash

   sphinx-build -q -b linkcheck docs _linkcheck

Review the broken links in the ``_linkcheck/output.txt`` file:

.. code-block:: bash

   cat _linkcheck/output.txt

.. _readthedocs:

ReadTheDocs
-----------

Create a project
~~~~~~~~~~~~~~~~

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
#. Click *Admin* then *Maintainers*, and for each of "yolile" and "jpmckinney":

   #. Enter the username in *Add maintainer*
   #. Click *Add*

#. Click *Admin* then *Email Notifications*

   #. Enter "sysadmin@open-contracting.org" in *Email*
   #. Click *Add*

#. Click *Edit Versions* (or *Versions*)

   #. Click *Edit* for the *stable* version
   #. Uncheck *Active*
   #. Click *Save*

Configure the project
~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

   .. tab-item:: Application

      .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/.readthedocs.yaml
         :language: yaml
         :caption: .readthedocs.yaml

      .. literalinclude:: ../../cookiecutter-django/{{cookiecutter.project_slug}}/docs/requirements.txt
         :caption: docs/requirements.txt

   .. tab-item:: Package

      .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/.readthedocs.yaml
         :language: yaml
         :caption: .readthedocs.yaml

      .. literalinclude:: ../../cookiecutter-pypackage/{{cookiecutter.repository_name}}/docs/requirements.txt
         :caption: docs/requirements.txt

Redirect a project
~~~~~~~~~~~~~~~~~~

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
