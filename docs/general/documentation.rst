Documentation
=============

.. _doc-types:

Types of documentation
----------------------

Read `The Documentation System <https://documentation.divio.com>`__ to learn about the four types of documentation we write: tutorials, how-to guides, technical reference and explanation.

Locations of documentation
--------------------------

External documentation can be accessed via the *Docs* links on `this page <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/badges.md>`__.

Internal documentation can be accessed via the `User Guides <https://ocdsdeploy.readthedocs.io/en/latest/use/index.html>`__ in the ``deploy`` repository.

Documentation should be maximally proximate to the thing it is documenting. For example, to document what a method in software does, it's best to author that documentation as a heredoc in the method itself, instead of in a separate document.

Required documentation
----------------------

The ``README.md`` file or documentation website must document how to:

-  Install requirements
-  Initialize services (e.g. via database migrations)
-  Configure settings (e.g. via environment variables)
-  Perform common actions, like:

   -  Start server
   -  Translate text
   -  Run tests

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
-  It's okay to put many how-to guides on one page; however, the setup guide should be on its own.

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

Documentation and examples for external users should use ``sh`` or ``bash`` syntax. Documentation for internal users can use ``fish`` syntax.

.. note::

   Read the Python :doc:`../python/documentation` page to learn what to document in Python projects and how to build Sphinx documentation.
