Administrative access
=====================

See the `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/reference/index.html>`__ for access to self-hosted services.

If a service is down, check its status page:

* `Amazon Web Services <https://health.aws.amazon.com/phd/status>`__
* `GitHub <https://www.githubstatus.com>`__
* `Google <https://www.google.com/appsstatus/dashboard/>`__
* `PyPI <https://status.python.org>`__
* `ReadTheDocs <https://status.readthedocs.com>`__
* `Sentry <https://status.sentry.io>`__
* `Transifex <https://status.transifex.com>`__

.. note::

   If you are a consultant, **do not** use or create your own organizational accounts on services like `Fixer <https://fixer.io>`__, `Prerender <https://prerender.io>`__, `Docker Hub <https://hub.docker.com>`__, etc. All organizational accounts must be owned by OCP.

Amazon Web Services
-------------------

There should be a minimum of two `IAM users <https://console.aws.amazon.com/iam/home?region=us-east-1#/home>`__ in the administrators group from OCP only. `The root user should not be used <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html>`__.

Cloudflare
----------

There should be a minimum of two `users <https://dash.cloudflare.com/db6be30e1a0704432e9e1e32ac612fe9/members>`__ from OCP with "Super Administrator - All Privileges" to "All domains".

Third-party managers of static websites can be added.

GitHub
------

There should be a minimum of two `owners <https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization>`__ from OCP only. Owners do not need to be added to teams.

.. tip::

   Use the `org:owners <https://github.com/open-contracting/standard-maintenance-scripts#github>`__ task to check the configuration.

.. seealso::

   :doc:`GitHub for maintainers<../github/maintainers>`

Google
------

Admin
~~~~~

There should be a minimum of two `Super Admin <https://admin.google.com/open-contracting.org/AdminHome?hl=en#DomainSettings/notab=1&role=9170516996784129&subtab=roles>`__ users from OCP only.

Analytics
~~~~~~~~~

Use `Fathom <https://app.usefathom.com/#/?range=last_7_days&site=61581>`__ instead.

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

All users with access to `this folder <https://drive.google.com/drive/folders/0B5mFIGaULYDdZTFWcTJ1MUpuZU0>`__ should belong to OCP only.

Groups
~~~~~~

-  `standard-discuss <https://groups.google.com/a/open-contracting.org/g/standard-discuss>`__ (`owners <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Aowner>`__, `managers <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Amanager>`__)

There should be a minimum of two `Owner <https://support.google.com/a/answer/167094?hl=en>`__ members from OCP only.

Linode
------

There should be a minimum of two `users <https://readthedocs.org/dashboard/ocds-standard-development-handbook/users/>`__ with Full account access from OCP.

Third-party managers of Linode servers can be added.

.. _pypi-access:

PyPI
----

For each package owned by the `opencontracting <https://pypi.org/user/opencontracting/>`__ user, there should be a minimum of two `Owner <https://pypi.org/help/#collaborator-roles>`__ users from OCP, including ``opencontracting``.

Only users who are reasonably expected to upload releases should have the Maintainer role.

If a third-party organization maintains a package, there can be one user from that organization with the Owner role to add maintainers (e.g. ``OpenDataServices``).

ReadTheDocs
-----------

There should be a minimum of two `users <https://readthedocs.org/dashboard/ocds-standard-development-handbook/users/>`__ with the Maintainer role from OCP.

Third-party maintainers of PyPI packages can be added to the package's associated ReadTheDocs project, including organizational accounts (e.g. ``opendataservices``).

Sentry
------

There should be a minimum of two `members <https://sentry.io/settings/open-contracting-partnership/members/>`__ with the Owner role and one member with the Billing role from OCP.

Third-party developers can be added with the Admin or Member role to organization-specific `teams <https://sentry.io/settings/open-contracting-partnership/teams/>`__ for specific projects.

Transifex
---------

There should be a minimum of two `Administrators <https://app.transifex.com/open-contracting-partnership-1/settings/>`__ users from OCP only.

If we reach our collaborator limit, `manage collaborators <https://app.transifex.com/open-contracting-partnership-1/collaborators/>`__, removing those who were last seen more than 9 months ago.
