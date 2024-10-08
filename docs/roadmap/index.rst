Strategy
========

OCP creates a data & technology strategy each year, to guide individual work plans. This page documents common concepts for all strategies.

Product and service families
----------------------------

-  Using data

   -  `Credere <https://credere.open-contracting.org/>`__: An online service that facilitates the participation of Micro, Small, and Medium businesses (MSMEs) in the Colombian public procurement market.

-  Enabling use

   -  `Data Registry <https://data.open-contracting.org/>`__: An online tool to find and access public procurement datasets that are available in the OCDS format.
   -  `Cardinal <https://github.com/open-contracting/cardinal-rs>`__: A command-line tool to calculate red flags and procurement indicators from OCDS data.

-  Evaluating data

   -  `Data Review Tool <https://ocds-data-review-tool.readthedocs.io/en/latest/>`__: An `online tool <https://review.standard.open-contracting.org/>`__ to report structural errors in OCDS data. It is primarily used by OCDS implementers to check their conformance to the standard. Its `library <https://github.com/open-contracting/lib-cove-ocds>`__ is used by Kingfisher to check for structural errors.
   -  `Pelican <https://www.open-contracting.org/2020/01/28/meet-pelican-our-new-tool-for-assessing-the-quality-of-open-contracting-data/>`__: An online tool to report quality issues in OCDS data, sourced from Kingfisher. It is used internally by data support managers to provide feedback to OCDS publishers, and by program managers to better understand a publisher's data.

-  Pre-processing data

   -  `Kingfisher <https://ocdsdeploy.readthedocs.io/en/latest/use/kingfisher.html>`__: A family of tools to `collect <https://kingfisher-collect.readthedocs.io/en/latest/>`__, `pre-process <https://kingfisher-process.readthedocs.io/en/latest/>`__, `summarize <https://kingfisher-summarize.readthedocs.io/en/latest/>`__ and `query <https://kingfisher-colab.readthedocs.io/en/latest/>`__ OCDS data. It is used internally by data support managers to provide feedback to OCDS publishers, and by data analysts to calculate indicators and do research. It serves as a data source for other tools.
   -  `OCDS Kit <https://ocdskit.readthedocs.io/en/latest/>`__: A suite of command-line tools and a Python library for working with OCDS data. It contains common functionality used by Kingfisher, for example.
   -  `Spoonbill <https://github.com/open-contracting/spoonbill>`__: A command-line tool to transform OCDS data to tabular formats. It is an important tool for users who are more familiar with tabular formats.

-  Publishing data

   -  `OCDS Documentation <https://standard.open-contracting.org/latest/en/>`__: The official documentation of the Open Contracting Data Standard.

Together, these tools connect with different steps of the hypothesis for change expressed in the `Scope of Data Products and Services <https://docs.google.com/document/d/1bJKyyhccImRkV-zi2DTEe5U9HDc_ncr5YJfMMUQiLfs/edit>`__.

.. _health:

Health
~~~~~~

For each product and service, `this spreadsheet <https://docs.google.com/spreadsheets/d/1MMqid2qDto_9-MLD_qDppsqkQy_6OP-Uo-9dCgoxjSg/edit#gid=0>`__ briefly describes its use, development status, future work and code quality, in order to give a high-level overview of its present status and future plans.

.. _principles:

Principles
----------

This section serves to clarify important considerations, not establish a comprehensive philosophy.

.. seealso:: `Manifesto for Agile Software Development <https://agilemanifesto.org>`_, prior to its professionalization and ritualization.

Understand user needs
~~~~~~~~~~~~~~~~~~~~~

Our tools must respond to user needs. See our development guide for `new software <https://docs.google.com/document/d/1uJ1WecaE860tIskFBgWTn2B1czNWtszLNzZRPqg2hh4/edit>`__ for how user research is integrated into our approach. We also:

-  Listen to users and document their needs, when they communicate through the `mailing list <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__, `GitHub repositories <https://github.com/open-contracting>`__, data support, community calls, in-person events, etc.
-  Ask users about their needs, whether via the channels above, surveys, interviews, etc.
-  Observe users interact with tools, whether via usability testing (direct) or web analytics (indirect)
-  Reflect on what was heard and observed, whether in team retreats, collaboration tools, etc.
-  Promote the use of our tools and encourage feedback via the channels above and data support
-  Recognize that our tools are only one part of a user's workflow and of a wider ecosystem
-  Transfer knowledge from relevant domains, e.g. open data more broadly

.. _create-products-sustainably:

Create products sustainably
~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is important to avoid both vendor lock-in and personnel lock-in (i.e. cases in which only one party has the knowledge and access to modify a product). To mitigate this risk, our approach is to:

-  Not build a new tool if, with reasonable effort, a third-party tool can be used, adapted or improved to meet our needs (e.g. `jq <https://stedolan.github.io/jq/>`__).
-  Use a `Quality Assurance Surveillance Plan (QASP) <https://docs.google.com/document/d/1s-PJSdX43_DMAcXYalG9Upm31XvWCp31j_QGCzFJ7qY/edit>`__ with consultants, which includes:

   -  Have test coverage (with relevant assertions) above 90%, so that new developers can get involved without being overly concerned about breaking things.
   -  Have :doc:`good documentation<../python/documentation>` for developers and users, making it easier to onboard new developers. (Writing documentation during development helps identify and reduce complexity.)

-  Maintain this software development handbook, which includes:

   -  Use popular :doc:`libraries<../python/preferences>` where possible (e.g. Click, Django, Scrapy), so that developers have fewer APIs to learn.
   -  Use a small number of languages (primarily Python) and dependencies (like Django), so that it is less effort to update dependencies with security fixes.

-  Break big products (that change frequently) into small libraries (that change infrequently), so that a new developer isn't required to know as much to work on a product.
-  Follow good practices so that code isn't more complex than needed: `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`__, `KISS <https://en.wikipedia.org/wiki/KISS_principle>`__, `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__ (refactor as needed), `Unix philosophy <https://en.wikipedia.org/wiki/Unix_philosophy>`__ (limited responsibility, loose coupling), proper encapsulation, etc.

   .. note::

      However, don't sacrifice performance, maintainability or readability. See also :doc:`general code principles<../general/code>` and :ref:`avoiding object-oriented style<object-oriented>`.

-  Use the latest versions of languages and dependencies, to postpone costly upgrades as far into the future as possible.
-  Use tools properly and as intended. Don’t go for the quick fix.
-  Anticipate needs with respect to performance and extensibility.

The above broadly follows the spirit of `Choose Boring Technology <https://boringtechnology.club>`__, which applies `Maslow's hierarchy <https://en.wikipedia.org/wiki/Maslow's_hierarchy_of_needs>`__ in the context of software development. We try to ensure basic needs are always satisfied (*Is it tested? Is there a maintenance plan?*), so that we can spend more time on the big picture (*Is it achieving user goals? Is it achieving organizational goals?*).

.. similar, but hard to read: https://grugbrain.dev

.. note::

   Our approach to refactoring is similar to that expressed in these posts:

   -  `Semantic compression <https://caseymuratori.com/blog_0015>`__
   -  `Complexity and granularity <https://caseymuratori.com/blog_0016>`__

   Our approach to architecture is informed by:

   -  `The Only Unbreakable Law <https://www.youtube.com/watch?v=5IUj1EZwpJY>`__
   -  `How Do Committees Invent? <https://www.melconway.com/Home/Committees_Paper.html>`__

Manage products and services responsibly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Among other practices, we:

-  Sufficiently resource the maintenance of all software, to `manage technical debt <https://tashian.com/articles/managing-technical-debt/>`__
-  Sufficiently resource the hosting of all services, to avoid service disruptions
-  Review the :ref:`health of products and services<health>` in each strategy and plan maintenance and improvements accordingly

See our development guides for `new software <https://docs.google.com/document/d/1uJ1WecaE860tIskFBgWTn2B1czNWtszLNzZRPqg2hh4/edit>`__ and `simple websites <https://docs.google.com/document/d/1mgOzn3YrrpOZagmXrEy-zOXRMBAFHOZpAXS2ERuVAkg/edit>`__.

Build capacity through documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the users of our products and services grow more numerous and diverse, we need to ensure that our documentation meets different users' different needs. See our approach to :doc:`../python/documentation`.

Collaborate with others
~~~~~~~~~~~~~~~~~~~~~~~

If OCP is creating and funding all the tools for contracting data, its strategy is not working. We limit our software development activity to the highest priority tools in order to bootstrap data use and support internal operations, and otherwise encourage others to develop tools.

Outside our software development activity, we:

-  Promote others' tools through our communications channels, like in `blog posts <https://www.open-contracting.org/2018/05/09/check-ocds-data-validates/>`__.
-  Suggest others' tools, where appropriate, through data support.
-  Have bilateral calls with similar organizations about software development.

Within our software development activity, we:

-  Contract teams to deliver our major projects, to build capacity for OCDS tool-building. For example, `Datlab <https://datlab.eu>`__ was awarded the contract to develop `Pelican <https://www.open-contracting.org/2020/01/28/meet-pelican-our-new-tool-for-assessing-the-quality-of-open-contracting-data/>`__ (FY20).
-  Engage with other teams to explore collaboration on open-source tools. For example, we made `JSCC <https://jscc.readthedocs.io/en/latest/>`__ (FY20) and `OCDS Babel <https://ocds-babel.readthedocs.io/en/latest/>`__ (FY19) reusable by other standards.
-  Follow `semantic versioning <https://semver.org>`__, so that others' software can reliably use our libraries as dependencies.

We also support others through time-bound projects. For example, in FY20, we worked with the World Bank Group and The Engine Room to author a `primer on tool reuse in open contracting <https://www.open-contracting.org/resources/tool-re-use-in-open-contracting-a-primer/>`__. In FY19, we funded tools supporting a Latin American journalists network. In FY18, we created the `OCDS Bounty Program <https://www.open-contracting.org/2018/08/07/hunting-open-contracting-impact-bounty-better-tools/>`__ to support tool-builders to better document and package their existing OCDS tools for reuse. In FY17, we invited developers to participate in a prize-based `Open Contracting Innovation Challenge <https://challenge.open-contracting.org>`__, to support six innovative and experimental tools.

Reference
---------

-  `Software Product Management Orientation <https://docs.google.com/document/d/1d-LRAjbiMlScijjIu1jQT0YuXhMiVnHKfJbnjuycLKc/edit>`__
-  `Scope of Data Products and Services <https://docs.google.com/document/d/1bJKyyhccImRkV-zi2DTEe5U9HDc_ncr5YJfMMUQiLfs/edit>`__
