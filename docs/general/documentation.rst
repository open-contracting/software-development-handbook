Documentation
=============

.. _doc-types:

Types of documentation
----------------------

Read `The Documentation System <https://documentation.divio.com>`__ to learn about the four types of documentation we write: tutorials, how-to guides, technical reference and explanation.

Locations of documentation
--------------------------

External documentation can be accessed via the *Docs* links on `this page <https://github.com/open-contracting/standard-maintenance-scripts/blob/master/badges.md>`__.

Internal documentation can be accessed via the `User Guides <https://ocdsdeploy.readthedocs.io/en/latest/use/index.html>`__ in the ``deploy`` repository.

Writing documentation
---------------------

Technical documentation should be clear and unambiguous. It should sacrifice style, flair, brevity and personality in favor of clarity.

General structure
~~~~~~~~~~~~~~~~~

-  Determine which :ref:`type of documentation<doc-types>` you are writing
-  Separate the types of documentation (different pages or, at minimum, different sections), but link between them

How-to guides
~~~~~~~~~~~~~

-  Give explicit instructions. `Don't make me think <https://en.wikipedia.org/wiki/Don%27t_Make_Me_Think>`__.
-  Don't include information that is not directly relevant to the how-to guide.
-  Use numbered lists for instructions. Nest sub-tasks to give structure to long lists.
-  Give example commands, but don't include default arguments or any other extraneous detail.
-  It's okay to put many how-to guides on one page; however, the setup guide should be its own page.

Word choice
~~~~~~~~~~~

Use consistent terms and constructions
  For example: "connect to the server," not a mix of "go to the app server", "access the remote machine", etc.
Use specific and non-metaphorical language
  For example: "connect" to the server, not "go" to the server.
Link unfamiliar terms to external documentation, if available
  For example: `concatenated JSON <https://en.wikipedia.org/wiki/JSON_streaming#Concatenated_JSON>`__.

Shell examples
~~~~~~~~~~~~~~

Documentation and examples for external users should use ``sh`` or ``bash``. Documentation for internal users can use ``fish``.

Building documentation locally
------------------------------

With Python 3 as your default interpreter, install Python modules:

.. code-block:: shell-session

   pip install sphinx sphinx_rtd_theme

Build the HTML pages:

.. code-block:: shell-session

   sphinx-build docs docs/_build/html

Run a web server:

.. code-block:: shell-session

   python -m http.server 8000

Open http://localhost:8000/docs/_build/html/ in your web browser:

.. code-block:: shell-session

   open http://localhost:8000/docs/_build/html/

.. note::

   If you are using Python 3.7 or greater, you can pass ``-d docs/_build/html`` to the ``python`` command, and open http://localhost:8000/.

.. note::

   Documentation is built in ``docs/_build/html``, to match the location when building with ``make html`` from the ``docs/`` directory.
