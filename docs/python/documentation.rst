Documentation
=============

.. _doc-types:

Types of documentation
----------------------

Read [The Documentation System](https://documentation.divio.com) to learn about the four types of documentation we write: tutorials, how-to guides, technical reference and explanation.

Locations of documentation
--------------------------

Packages and applications must have documentation to describe their usage for an external audience. They may have documentation to describe how to contribute. Documentation is written using `Sphinx <https://www.sphinx-doc.org/>`__.

Packages must have `Sphinx-style docstrings <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists>`__ for public modules, classes and methods, so that Sphinx can automatically generate documentation and so that Python's `help() function <https://docs.python.org/3/library/functions.html#help>`__ can display useful output.

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

-  Don't include information that is not directly relevant to the how-to guide.
-  Use numbered lists for instructions. Nest sub-tasks to give structure to long lists.
-  Give example commands, but don't include default arguments or any other extraneous detail.

Word choice
~~~~~~~~~~~

Use consistent terms and constructions
  For example: "connect to the server," not a mix of "go to the app server", "access the remote machine", etc.
Use specific and non-metaphorical language
  For example: "connect" to the server, not "go" to the server.
Link unfamiliar terms to external documentation, if available
  For example: `concatenated JSON <https://en.wikipedia.org/wiki/JSON_streaming#Concatenated_JSON>`__.
