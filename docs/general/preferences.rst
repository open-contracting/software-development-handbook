Preferences
===========

We have preferences in order to limit the number of tools with which developers need to be familiar.

Collaboration
-------------

-  GitHub (version control, issue tracking, `project board <https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards>`__)
-  Google Docs (collaborative editing)
-  Google Meet (audio/video calling)
-  Slack (instant messaging)

.. _devops:

DevOps
------

-  `SaltStack <https://docs.saltproject.io>`__ (service deployment)
-  `GitHub Actions <https://docs.github.com/en/actions>`__ (continuous testing)
-  `GitHub Packages <https://docs.github.com/en/packages>`__ (Docker images)
-  `Coveralls <https://coveralls.io/github/open-contracting>`__ (coverage reporting)
-  `LastPass <https://lastpass.com/vault/>`__ (shared secrets)

Monitoring
----------

.. seealso::

   `Monitoring >https://ocdsdeploy.readthedocs.io/en/latest/reference/#monitoring>`__ in the Deploy documentation

-  `Prometheus <https://prometheus.io>`__
-  `Sentry <https://sentry.io>`__
-  `Ahrefs <https://ahrefs.com>`__
-  `SecurityScorecard <https://securityscorecard.com>`__
-  `WordFence <https://www.wordfence.com>`__

Hosting
-------

.. seealso::

   `Hosting >https://ocdsdeploy.readthedocs.io/en/latest/reference/#hosting>`__ in the Deploy documentation

-  Cloudflare Pages
-  Linode
-  Hetzner
-  ReadTheDocs

Languages
---------

-  Python (backend)
-  JavaScript (frontend)
-  Rust (performance)
-  Make (build)
-  Bash (script)
-  `reStructured Text <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__ (`Sphinx <https://www.sphinx-doc.org/en/master/>`__ documentation)
-  `Markdown <https://commonmark.org>`__ (non-Sphinx documentation)

Datastores
----------

-  PostgreSQL
-  Elasticsearch if our needs exceed PostgreSQL's `capabilities <https://www.postgresql.org/docs/current/textsearch.html>`__, or if there is no PostgreSQL database

Web servers
-----------

-  Apache on hosts
-  Nginx in containers

Miscellaneous
-------------

-  Amazon Web Services (non-compute), including:

   -  CloudFront (content delivery network)
   -  Cognito (identity provider)
   -  Relational Database Service (RDS)
   -  Simple Email Service (SES)
   -  Simple Notification Service (SNS)
   -  Simple Storage Service (S3)

   CloudWatch and Identity and Access Management (IAM) are used to monitor and access these.

   .. note:: OCP has `AWS credits from TechSoup <https://www.techsoup.org/amazon-web-services>`__.

-  Fathom (web analytics)
-  Fixer (currency conversion)
-  GoDaddy (registrar and DNS) `#340 <https://github.com/open-contracting/deploy/issues/340>`__
-  Memcached (page caching)
-  Power BI (business intelligence)
-  RabbitMQ (message broker)
-  Transifex (translation) for collaboration, otherwise gettext

Reference
---------

-  `18F Language Selection Guide <https://engineering.18f.gov/language-selection/>`__
-  `18F Datastore Selection Guide <https://engineering.18f.gov/datastore-selection/>`__
