Roadmap
=======

OCP prepares a software roadmap each fiscal year. This page documents common concepts for all roadmaps.

Product and service families
----------------------------

-  `Data Review Tool <https://ocds-data-review-tool.readthedocs.io/>`__: An `online tool <https://standard.open-contracting.org/review/>`__ to report structural errors in OCDS data. It is primarily used by OCDS implementers to check their conformance to the standard. Its `library <https://github.com/open-contracting/lib-cove-ocds>`__ is used by Kingfisher to check for structural errors.
-  `Kingfisher <https://ocdsdeploy.readthedocs.io/en/latest/use/kingfisher.html>`__: A family of tools to `collect <https://kingfisher-collect.readthedocs.io/>`__, `pre-process <https://kingfisher-process.readthedocs.io/>`__, `summarize <https://kingfisher-summarize.readthedocs.io/>`__ and `query <https://kingfisher-colab.readthedocs.io/>`__ OCDS data. It is used internally by helpdesk analysts to provide feedback to OCDS publishers, and by data analysts to calculate indicators and do research. It serves as a data source for other tools.
-  `Pelican <https://www.open-contracting.org/2020/01/28/meet-pelican-our-new-tool-for-assessing-the-quality-of-open-contracting-data/>`__: An online tool to report quality issues in OCDS data, sourced from Kingfisher. It is used internally by helpdesk analysts to provide feedback to OCDS publishers, and by program managers to better understand a publisher's data.
-  `Spoonbill <https://github.com/open-contracting/spoonbill>`__: A command-line tool to transform OCDS data to tabular formats. It is an important tool for users who are more familiar with tabular formats.
-  `OCDS Kit <https://ocdskit.readthedocs.io/>`__: A suite of command-line tools and a Python library for working with OCDS data. It contains common functionality used by Kingfisher and Toucan, in particular.
-  `Toucan <https://toucan.open-contracting.org>`__: An online tool to replicate the functionality of command-line tools in a browser. It gives access to OCDS Kit and `Flatten Tool <https://flatten-tool.readthedocs.io/usage-ocds/>`__.
-  `Redash <https://redash.open-contracting.org>`__: A deployment of `Redash <https://redash.io>`__ to give users access to the Kingfisher database.
-  `OCDS Documentation <https://standard.open-contracting.org>`__: The official documentation of the Open Contracting Data Standard.

Together, these tools connect with different steps of the hypothesis for change expressed in the `Scope of Data Products and Services <https://docs.google.com/document/d/1bJKyyhccImRkV-zi2DTEe5U9HDc_ncr5YJfMMUQiLfs/edit>`__.

.. _health:

Health
~~~~~~

For each product and service, `this spreadsheet <https://docs.google.com/spreadsheets/d/1MMqid2qDto_9-MLD_qDppsqkQy_6OP-Uo-9dCgoxjSg/edit#gid=0>`__ briefly describes its use, development status, future work and code quality, in order to give a high-level overview of its present status and future plans.

Principles
----------

This section serves to clarify important considerations, not establish a comprehensive philosophy.

Understand user needs
~~~~~~~~~~~~~~~~~~~~~

It is of course of primary importance that our tools respond to user needs. See our development guide for `new software <https://docs.google.com/document/d/1uJ1WecaE860tIskFBgWTn2B1czNWtszLNzZRPqg2hh4/edit>`__ for how user research is integrated into our approach. We also:

-  Listen to users and document their needs, when they communicate through the `mailing list <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__, `GitHub repositories <https://github.com/open-contracting>`__, OCDS Helpdesk, community calls, in-person events, etc.
-  Ask users about their needs, whether through the channels above, online surveys, phone interviews, or other methods
-  Observe users interact with our tools, whether indirectly through web analytics or directly through usability testing
-  Reflect on what was heard and observed, whether during OCDS retreats, OCDS Helpdesk weekly calls, CRM issues, GitHub repositories, etc.
-  Promote the use of our tools and encourage feedback through the mailing list, GitHub repositories, and OCDS Helpdesk
-  Recognize that our tools are only one part of a user's workflow and of a wider ecosystem
-  Transfer knowledge from relevant domains, e.g. open data more broadly

Create products sustainably
~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is important to avoid both vendor lock-in and personnel lock-in (i.e. cases in which only one party has the knowledge and access to modify a product). To mitigate this risk, our approach is to:

-  Not build a new tool if, with reasonable effort, a third-party tool can be used, adapted or improved to meet our needs (e.g. `jq <https://stedolan.github.io/jq/>`__).
-  Use a `Quality Assurance Surveillance Plan (QASP) <https://docs.google.com/document/d/1s-PJSdX43_DMAcXYalG9Upm31XvWCp31j_QGCzFJ7qY/edit>`__ with consultants, which includes:

   -  Have test coverage above 90%, so that new developers can get involved without being overly concerned about breaking things.
   -  Have :doc:`good documentation<../python/documentation>` for developers and users, making it easier to onboard new developers. Documenting methods can expose complexity, which helps to simplify APIs.

-  Maintain this software development handbook, which includes:

   -  Use popular :doc:`libraries<../python/preferred_packages>` where possible (e.g. Click, Django, Scrapy), so that developers have fewer APIs to learn.
   -  Use a small number of languages (primarily Python) and dependencies (like Django), so that it is less effort to update dependencies with security fixes.

-  Break big products (that change frequently) into small libraries (that change infrequently), so that a new developer isn't required to know as much to work on a product.
-  Follow good practices so that code isn't more complex than needed: `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`__, `KISS <https://en.wikipedia.org/wiki/KISS_principle>`__, `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__ (refactor regularly), `Unix philosophy <https://en.wikipedia.org/wiki/Unix_philosophy>`__ (limited responsibility, loose coupling), proper encapsulation, etc.
-  Use the latest versions of languages and dependencies, to postpone costly upgrades as far into the future as possible.
-  Use tools properly and as intended. Don’t go for the quick fix.
-  Anticipate needs with respect to performance and extensibility.

Manage products and services responsibly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Among other practices, we:

-  Sufficiently resource the maintenance of all software, to limit technical debt
-  Sufficiently resource the hosting of all services, to avoid service disruptions
-  Review the :ref:`health of products and services<health>` in each roadmap and plan maintenance and improvements accordingly

See our development guides for `new software <https://docs.google.com/document/d/1uJ1WecaE860tIskFBgWTn2B1czNWtszLNzZRPqg2hh4/edit>`__ and `simple websites <https://docs.google.com/document/d/1mgOzn3YrrpOZagmXrEy-zOXRMBAFHOZpAXS2ERuVAkg/edit>`__.

Build capacity through documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the users of our products and services grow more numerous and diverse, we need to ensure that our documentation meets different users' different needs. See our approach to :doc:`../python/documentation`.

Collaborate with others
~~~~~~~~~~~~~~~~~~~~~~~

If OCP is creating and funding all the tools, its strategy is not working. We limit our software development activity to the highest priority tools in order to bootstrap data use and support internal operations, and otherwise encourage others to develop tools.

Outside our software development activity, we:

-  Promote others' tools through our communications channels, like in `blog posts <https://www.open-contracting.org/2018/05/09/check-ocds-data-validates/>`__.
-  Offer a `mailing list <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__ through which others can share and promote their tools.
-  Suggest others' tools, where appropriate, through the OCDS Helpdesk.
-  Maintain an `Open Contracting Tools Directory <https://www.open-contracting.org/resources/open-contracting-tools-directory/>`__, to promote tools authored by others.
-  Have bilateral calls with similar organizations about software development.

Within our software development activity, we:

-  Contract teams to deliver our major projects, to build capacity for OCDS tool-building. For example, `Datlab <https://datlab.eu>`__ was awarded the contract to develop `Pelican <https://www.open-contracting.org/2020/01/28/meet-pelican-our-new-tool-for-assessing-the-quality-of-open-contracting-data/>`__ (FY20).
-  Share new versions of our tools and libraries with other teams through the `mailing list <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__, so that they are aware of any changes.
-  Follow `semantic versioning <https://semver.org>`__, so that others' software can reliably use our libraries as dependencies.
-  Engage with other teams to explore collaboration on open-source tools. For example, we made `JSCC <https://jscc.readthedocs.io/>`__ (FY20) and `OCDS Babel <https://ocds-babel.readthedocs.io/>`__ (FY19) reusable by other standards.

We also support others through time-bound projects. For example, in FY20, we worked with the World Bank Group and The Engine Room to author a `primer on tool reuse in open contracting <https://www.open-contracting.org/resources/tool-re-use-in-open-contracting-a-primer/>`__. In FY19, we funded tools supporting a Latin American journalists network. In FY18, we created the `OCDS Bounty Program <https://www.open-contracting.org/2018/08/07/hunting-open-contracting-impact-bounty-better-tools/>`__ to support tool-builders to better document and package their existing OCDS tools for reuse. In FY17, we invited developers to participate in a prize-based `Open Contracting Innovation Challenge <http://challenge.open-contracting.org>`__, to support six innovative and experimental tools.

Reference
---------

-  `Software Product Management Orientation <https://docs.google.com/document/d/1d-LRAjbiMlScijjIu1jQT0YuXhMiVnHKfJbnjuycLKc/edit>`__
-  `Scope of Data Products and Services <https://docs.google.com/document/d/1bJKyyhccImRkV-zi2DTEe5U9HDc_ncr5YJfMMUQiLfs/edit>`__
