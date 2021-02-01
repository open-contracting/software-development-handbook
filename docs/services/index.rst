Administrative access
=====================

See the `Deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/reference/index.html>`__ for access to self-hosted services and to third-party monitoring services.

Airtable
--------

There should be a minimum of two `Owners <https://airtable.com/wspXFnEMMAgLMWfe0/workspace/billing>`__ from OCP only.

Amazon Web Services
-------------------

There should be a minimum of two `IAM users <https://console.aws.amazon.com/iam/home?region=us-east-1#/home>`__ in the administrators group from OCP only.

GitHub
------

See :ref:`GitHub Teams<github-teams>`.

Google
------

Admin
~~~~~

There should be a minimum of two `Super Admin <https://admin.google.com/open-contracting.org/AdminHome?hl=en#DomainSettings/notab=1&role=9170516996784129&subtab=roles>`__ users from OCP only.

*Less secure apps* is set to “Allow users to manage their access to less secure apps” for the open-contracting.org domain, and `Allow less secure apps <https://myaccount.google.com/lesssecureapps>`__ is set to “ON” for the data@open-contracting.org user, so that Redmine can fetch mail.

Analytics
~~~~~~~~~

There should be a minimum of two `users <https://analytics.google.com/analytics/web/#/a35677147w162037252p163071392/admin/suiteusermanagement/account>`__ with all permissions from OCP only.

There should be at most two users with the Read & Analyze permissions from any other organization.

The *OCDS Tools* property tracks:

-  Toucan
-  OCDS Show
-  OCDS Show for PPPs
-  Extension Creator

The *Open Contracting* property tracks:

-  OCDS Documentation
-  OCDS Data Review Tool
-  Extension Explorer
-  All OCDS profiles
-  OC4IDS Documentation
-  OC4IDS Data Review Tool

Cloud Platform
~~~~~~~~~~~~~~

There should be a minimum of two `Organization Administrator <https://console.cloud.google.com/iam-admin/iam?organizationId=1015889055088>`__ roles from OCP only.

For the ``ocds`` project, `IAM <https://console.cloud.google.com/iam-admin/iam?organizationId=1015889055088&project=ocds-172716>`__ should only include Google-managed service accounts, ``ods-crm-redmine-backup`` and ``sysadmin@dogsbody.com``. `Service accounts <https://console.cloud.google.com/iam-admin/serviceaccounts?organizationId=1015889055088&project=ocds-172716>`__ should only include default service accounts and ``ods-crm-redmine-backup``. It should only use two storage buckets (``crm-open-contracting-org-daily-backups`` and ``crm-open-contracting-org-weekly-backups``). ``sysadmin@dogsbody.com`` must have the `“Storage Admin” role <https://cloud.google.com/storage/docs/access-control/iam-roles>`__ (``roles/storage.admin``), to get the ``storage.buckets.list`` permission.

Periodically review `all projects <https://console.cloud.google.com/cloud-resource-manager?organizationId=1015889055088>`__. To view a project’s history, click its `Activity tab <https://console.cloud.google.com/home/activity?organizationId=1015889055088&project=ocds-172716>`__. To view a project’s resources, click its `Dashboard tab <https://console.cloud.google.com/home/dashboard?organizationId=1015889055088&project=ocds-172716>`__. Projects include:

-  Library (two storage buckets)
-  Pelican
-  Toucan
-  Website Search (API key)

In case a new user needs to be given admin access to the ``ocds`` project, you can run, for example:

.. code-block:: bash

   gcloud projects add-iam-policy-binding ocds-172716 --member user:jmckinney@open-contracting.org --role roles/owner

Drive
~~~~~

All users with access to `this folder <https://drive.google.com/drive/folders/0B79uNIOfT24eZTZqZjNNblVrek0>`__ should belong to OCP, Centro de Desarrollo Sostenible (CDS) and Open Data Services Co-operative Limited (ODS).

Groups
~~~~~~

-  `standard-discuss <https://groups.google.com/a/open-contracting.org/forum/#!forum/standard-discuss>`__ (`owners <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Aowner>`__, `managers <https://groups.google.com/a/open-contracting.org/g/standard-discuss/members?q=role%3Amanager>`__)

There should be a minimum of two `Owner <https://support.google.com/a/answer/167094?hl=en>`__ members from OCP only.

There should be at most two members with the Manager role from each other organization.

PyPi
----

For each package owned by the `opencontracting <https://pypi.org/user/opencontracting/>`__ user, there should be a minimum of two `Owner <https://pypi.org/help/#collaborator-roles>`__ roles from OCP only, including ``opencontracting``.

Only users who are reasonably expected to upload releases should have the Maintainer role.

ReadTheDocs
-----------

There should be at most two `users <https://readthedocs.org/dashboard/ocds-standard-development-handbook/users/>`__ with the Maintainer role from each of OCP and ODS, excluding organization-wide accounts.

Transifex
---------

Transifex is used by ODS for multiple clients. There should be at most two members with the `Project Maintainer and Team Manager <https://docs.transifex.com/teams/understanding-user-roles>`__ roles from OCP.
