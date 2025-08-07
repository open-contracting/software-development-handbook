Administrative access
=====================

See the `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/use/>`__ for access to self-hosted services, like servers, PostgreSQL, Kingfisher, Pelican and Prometheus.

If a service is down, check its status page:

-  `Amazon Web Services <https://health.aws.amazon.com/phd/status>`__
-  `Cloudflare <https://www.cloudflarestatus.com>`__
-  `GitHub <https://www.githubstatus.com>`__
-  `GoDaddy <https://status.godaddy.com>`__
-  `Google <https://www.google.com/appsstatus/dashboard/>`__
-  `Heroku <https://status.heroku.com>`__
-  `LastPass <https://status.lastpass.com>`__
-  `Linode <https://status.linode.com>`__
-  `Microsoft Azure <https://azure.status.microsoft/en-ca/status>`__
-  `PyPI <https://status.python.org>`__
-  `ReadTheDocs <https://status.readthedocs.com>`__
-  `Sentry <https://status.sentry.io>`__
-  `Transifex <https://status.transifex.com>`__
-  `WordFence <https://status.wordfence.com>`__

These :doc:`preferred services<../general/preferences>` don't have individual user accounts:

-  Ahrefs (`requires account upgrade <https://app.ahrefs.com/pricing>`__)
-  Fathom
-  Fixer
-  Hetzner (except :ref:`hetzner-cloud`)

.. note::

   If you are a consultant, **do not** use or create your own organizational accounts on services like `Fixer <https://fixer.io>`__, `Prerender <https://prerender.io>`__, `Docker Hub <https://hub.docker.com>`__, etc. All organizational accounts must be owned by OCP.

.. seealso::

   :doc:`../general/preferences`, for the context in which these services are used.

Amazon Web Services
-------------------

There should be a minimum of two `IAM users <https://console.aws.amazon.com/iam/home?region=us-east-1#/home>`__ in the administrators group from OCP only. `The root user should not be used <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html>`__.

.. _cloudflare:

Cloudflare
----------

There should be a minimum of two `users <https://dash.cloudflare.com/db6be30e1a0704432e9e1e32ac612fe9/members>`__ from OCP with "Super Administrator - All Privileges" access to "All domains".

Third-party sysadmins can be added with "Administrator" access to "All domains".

Figma
-----

There should be a minimum of two `admins <https://www.figma.com/files/team/967086771254173797/team-admin-console/members>`__ from OCP.

You can sort by *Last active* and remove seats from users who were last active more than 6 months ago.

GitHub
------

There should be a minimum of two `owners <https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization>`__ from OCP only. Owners do not need to be added to teams.

The ``ocp-deploy`` user generates `personal access tokens <https://github.com/settings/tokens>`__ to:

-  read and write to `ocp-data <https://github.com/open-contracting-partnership/ocp-data>`__ from the `OCP Form Server <https://survey.open-contracting.org>`__ on :ref:`heroku` (fine-grained)
-  auto-commit from :doc:`lint workflows<../github/maintainers>` to `selected repositories <https://github.com/orgs/open-contracting/teams/robots/repositories>`__ (classic)

.. tip::

   Use the `org:owners <https://github.com/open-contracting/standard-maintenance-scripts#github>`__ task to check the configuration.

.. seealso::

   :doc:`GitHub for maintainers<../github/maintainers>`

GoDaddy
-------

.. seealso::

   `DNS <https://ocdsdeploy.readthedocs.io/en/latest/deploy/services/dns.html>`__ in the Deploy documentation

There should be a minimum of two `accounts <https://sso.godaddy.com/access>`__ from OCP only at the "Products, Domains, & Purchase" access level.

Third-party sysadmins can be added with "Delegate" access.

Google
------

.. note::

   For web analytics, use `Fathom <https://app.usefathom.com/#/?range=last_7_days&site=61581>`__ instead.

Admin
~~~~~

There should be a minimum of two `Super Admin <https://admin.google.com/open-contracting.org/AdminHome?hl=en#DomainSettings/notab=1&role=9170516996784129&subtab=roles>`__ users from OCP only.

Cloud Platform
~~~~~~~~~~~~~~

.. note::

   Use Amazon Web Services, unless an application requires access to Google-exclusive services like Google Drive.

There should be a minimum of two `Organization Administrator <https://console.cloud.google.com/iam-admin/iam?organizationId=1015889055088>`__ users from OCP only.

Periodically review `all projects <https://console.cloud.google.com/cloud-resource-manager?organizationId=1015889055088>`__. To view a project’s history, click its `Activity tab <https://console.cloud.google.com/home/activity?organizationId=1015889055088&project=ocds-172716>`__. To view a project’s resources, click its `Dashboard tab <https://console.cloud.google.com/home/dashboard?organizationId=1015889055088&project=ocds-172716>`__. Projects include:

-  Library (two storage buckets)
-  Pelican (IAM user)
-  Website Search (API key)

If an administrator lacks access to a project, run, for example:

.. code-block:: bash

   gcloud projects add-iam-policy-binding ocds-172716 --member user:jmckinney@open-contracting.org --role roles/owner

If the user interface lacks access to an organization, run, for example:

.. code-block:: bash

   gcloud organizations add-iam-policy-binding organizations/1015889055088 --member domain:open-contracting.org --role roles/recommender.viewer

Drive
~~~~~

All users with access to the `Data & Technology folder <https://drive.google.com/drive/folders/0B5mFIGaULYDdZTFWcTJ1MUpuZU0>`__ should belong to OCP only.

Groups
~~~~~~

-  `standard-discuss <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__ (`owners <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Aowner>`__, `managers <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Amanager>`__)

There should be a minimum of two `Owner <https://support.google.com/a/answer/167094?hl=en>`__ members from OCP only.

.. _heroku:

Heroku
------

For each app, a minimum of two `collaborators <https://devcenter.heroku.com/articles/collaborating#collaborator-permissions-for-apps-in-a-personal-account>`__ from OCP only, including the owner.

Third-party sysadmins can be added with "Collaborator" access.

.. _hetzner-cloud:

Hetzner Cloud
-------------

There should be a minimum of two `admins <https://console.hetzner.cloud/projects/104976/security/members>`__ from OCP, including the ``sysadmin`` owner.

Third-party sysadmins can be added with "Member" access.

LastPass
--------

There should be a minimum of two Manager users from OCP, including the ``sysadmin`` user.

Third-party sysadmins can be added with "Member" access to the "Servers" and "Sysadmin" folders.

Linode
------

There should be a minimum of two `users <https://readthedocs.org/dashboard/ocds-standard-development-handbook/users/>`__ with Full account access from OCP.

Third-party sysadmins can be added with "Full" access.

Microsoft
---------

.. note::

   Use Amazon Web Services instead of Azure, unless an application requires access to Microsoft-exclusive services like Power BI, or a partner requires it.

.. tip::

   Check *Fabric Capacity* in the Microsoft Fabric (Power BI) `Admin portal <https://app.powerbi.com/admin-portal/capacities/capacitiesList/dc?experience=power-bi>`__.

There should be a minimum of two `users <https://admin.microsoft.com/#/rbac/directory/:/rbac/directory/62e90394-69f5-4237-9190-012177145e10/details/assigned>`__ with the Global Administrator role from OCP.

Third-party sysadmins can be added with "Global Administrator" access.

.. _pypi-access:

PyPI
----

`Transfer <https://pypi.org/manage/organization/opencontracting/projects/>`__ all projects to the `opencontracting <https://pypi.org/org/opencontracting/>`__ organization.

The organization should have a minimum of two `Owner <https://docs.pypi.org/organization-accounts/roles-entities/>`__ users from OCP, in addition to the `opencontracting <https://pypi.org/user/opencontracting/>`__ user, whose API token is used in `pypi.yml workflows <pypi-ci>`__.

Only users who are reasonably expected to upload releases should have an organization role.

If a third-party organization maintains a package, there can be one project collaborator (not organization member) from that organization with the Owner role on the specific project to add maintainers (e.g. ``OpenDataServices``).

ReadTheDocs
-----------

There should be a minimum of two `users <https://readthedocs.org/dashboard/ocds-standard-development-handbook/users/>`__ with the Maintainer role from OCP.

Third-party maintainers can be added to the package's associated ReadTheDocs project, including organizational accounts (e.g. ``opendataservices``).

SecurityScorecard
-----------------

The `Free Plan <https://securityscorecard.com/pricing-packages/>`__ has no `people management <https://support.securityscorecard.com/hc/en-us/articles/360056396951-Manage-users-and-permissions-in-SecurityScorecard>`__.

Third-party sysadmins can be `added <https://platform.securityscorecard.io/#/getting-started>`__.

Sentry
------

There should be a minimum of two `members <https://sentry.io/settings/open-contracting-partnership/members/>`__ with the Owner role and one member with the Billing role from OCP.

Third-party developers can be added with the Admin or Member role to organization-specific `teams <https://sentry.io/settings/open-contracting-partnership/teams/>`__ for specific projects.

Third-party sysadmins can be added with "Member" access.

Test PyPI
---------

For each package, the `opencontracting <https://test.pypi.org/user/opencontracting/>`__ user can be the single Owner, whose API token is used in `pypi.yml workflows <pypi-ci>`__.

Transifex
---------

There should be a minimum of two `Administrators <https://app.transifex.com/open-contracting-partnership-1/settings/>`__ from OCP only.

If we reach our collaborator limit, `manage collaborators <https://app.transifex.com/open-contracting-partnership-1/collaborators/>`__, removing those who were last seen more than 9 months ago.

Valimail
--------

There should be a minimum of two `Owners <https://app.valimail.com/app/open-contracting-partnership/settings/members>`__ from OCP.

Third-party sysadmins can be added with "Owner" access.

WordFence
---------

There should be a minimum of two `members <https://www.wordfence.com/central/teams>`__ from OCP. There can only be one Owner user.

Third-party sysadmins can be added with "Member" access.

WordPress (self-hosted)
-----------------------

There should be a minimum of two Administrator users from OCP.

Third-party sysadmins can be added with "Administrator" access.
