For maintainers
===============

.. seealso::

   `GitHub Burndown <https://observablehq.com/@tmcw/github-burndown>`__ is a handy visualization of the longevity of issues over time.

Name a project
--------------

A product name should be:

-  **Unique** within OCP

   e.g. having two ‘scoping methodologies’ is confusing

-  **Easy to spell and pronounce**

   | e.g. Shwowp became Buyosphere because no one could spell ‘Shwowp’
   | e.g. an unpronounceable acronym

-  **Memorable**
-  **Not competing** with another relevant or prominent thing
-  **Not generic** unless only one thing fits the description

   | e.g. ocdsdata became OCDS Kingfisher
   | e.g. there will only ever be one OCDS Extension Registry

-  **Not cryptic**

   i.e. several hops of translation and analogy

-  **Not grossly offensive** to relevant stakeholders 

Furthermore, if the product is specific to OCDS, its full name should be prefixed with 'OCDS'.

Onboard consultants or Start a project
--------------------------------------

#. Create `new repositories <https://github.com/orgs/open-contracting/repositories>`__, as needed by the consultants
#. Run the `fix:lint_repos <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ and ``fix:protect_branches`` tasks, to configure the repository
#. Create a `new team <https://github.com/orgs/open-contracting/teams>`__ named after the consultants' organization

   .. note::

      Do not use `outside collaborators <https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/adding-outside-collaborators-to-repositories-in-your-organization>`__. Individual consultants can be collected into appropriate teams, like the `Standard <https://github.com/orgs/open-contracting/teams/standard>`__ team.

#. From the *Members* tab:

   #. Remove yourself from the team
   #. Invite the Project Manager
   #. Once the invitation is accepted, set their role to Maintainer
   #. Ask them to invite the rest of their team
   #. Invite OCP program managers or project management consultants, as needed

#. From the *Repositories* tab:

   #. Add the new repositories
   #. Set the *Permission level* to "Maintain"

      .. note::

         If consultants need to make changes that require Admin privileges, instead, ask the consultants for instructions to make the changes yourself.

#. If using the ``stefanzweifel/git-auto-commit-action`` action in the :ref:`lint.yml workflow<linting-ci>`, like in the :doc:`../python/django` Cookiecutter template to auto-fix requirements files:

   #. Add the new repositories to the `Robots <https://github.com/orgs/open-contracting/teams/robots/repositories>`__ team
   #. Set the *Permission level* to "Admin"

   .. note::

      This permission level is required to **push fixes to protected branches**. The ``ocp-deploy`` user is the only member of the Robots team. The ``PAT`` environment variable is its personal access token to access all repositories of the ``open-contracting`` organization with a *Contents* permission of *Read and write*.

#. Add the new repositories to `pre-commit ci <https://github.com/organizations/open-contracting/settings/installations/20658712>`__
#. Add the new repositories to `Coveralls <https://coveralls.io/repos/new>`__
#. Add any projects to :ref:`ReadTheDocs<readthedocs>` as appropriate
#. Use the :doc:`Django Cookiecutter template<../python/django>`, if relevant

Per the `Software terms of reference (TOR) template <https://docs.google.com/document/d/13-_eFQrelLdj92MWTiqzAfO62in7Xxrv3DTcmRqvNjE/edit>`__, consultants should not have access to the production server. As such, do not add any members to the `Servers <https://github.com/orgs/open-contracting/teams/servers>`__ team.

.. warning::

   **NEVER** assign the Owner role to non-OCP staff. The Owner role has access to a private repository with multi-factor authentication backup codes. `Transferring a repository <https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository>`__ does not require the Owner role.

.. tip::

   Update and then use the `org:members <https://github.com/open-contracting/standard-maintenance-scripts#github>`__, ``org:team_members``, ``org:team_repos`` and ``org:team_perms`` tasks to check the configuration.

.. note::

   In order to protect the private deploy repositories, the `base permissions <https://github.com/organizations/open-contracting/settings/member_privileges>`__ for ``open-contracting`` members is *None*.

.. note::

   A `custom security configuration <https://docs.github.com/en/code-security/securing-your-organization/enabling-security-features-in-your-organization/applying-a-custom-security-configuration>`__ is applied to all new repositories.

Offboard consultants
--------------------

If the consultants are anticipated to contribute again, set the *Permission level* for all repositories to "Write". Otherwise, delete the team.

.. _repository-metadata:

Add repository metadata
-----------------------

#. Add a description. Do not describe the project’s status (‘draft’), because people frequently forget to update repository descriptions. Describe the status in the readme instead.
#. Add a website to the repository, if relevant: for example, a link to a deployment of the tool or to its documentation.

Protect branches
----------------

.. tip::

   Use the `fix:protect_branches <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task to protect branches.

We don’t generally enable the following behaviors on `protected branches <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>`__ for the provided reasons:

-  **Require branches to be up to date before merging**: While this may avoid introducing errors, it slows development in an environment in which there are many simultaneous pull requests, because each would require an extra step before merging. If the automated tests fail after merging, the error can be corrected, or the changes can be reverted.
-  **Require pull request reviews before merging**: While this is a best practice, it slows development as the team is not sufficiently large to staff it. It is okay, for example, for an author to self-merge a simple change. Authors may, of course, request reviews for significant changes.

If a repository needs multiple branches (like the standard and profiles), the needed branches should be protected. Otherwise, unprotected branches more than a month old should either be opened as pull requests, protected, or deleted.

.. seealso::

   Branch management of the `standard <https://ocds-standard-development-handbook.readthedocs.io/en/latest/standard/technical/repository.html>`__ and `profiles <https://ocds-standard-development-handbook.readthedocs.io/en/latest/profiles/technical/repository.html>`__ (including OC4IDS).

Archive a repository
--------------------

Repositories that are no longer supported should be archived.

#. Agree whether to archive the repository. The archived repositories presently include:

   -  Superseded repositories (e.g. `json-merge-patch <https://github.com/OpenDataServices/json-merge-patch>`__ supersedes `jsonmerge <https://github.com/open-contracting-archive/jsonmerge>`__)
   -  Abandoned extensions (e.g. `ocds-equityTransferCaps-extension <https://github.com/open-contracting-archive/ocds-equityTransferCaps-extension>`__)
   -  Merged changes to the core standard, expressed as extension repositories (``ocds_upgrade_###``)
   -  Exploratory repositories from pre-1.0 and pre-2015

#. Scan the repository’s open issues, milestones, pull requests and non-default branches in case any can be quickly closed, merged or deleted. Counter `GitHub’s recommendation <https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>`__, open issues and pull requests indicate the development status of a repository, and should be left open.
#. Change the repository’s description to describe the reason for archival. If the repository has been superseded, change it to “Superseded by [owner]/[repository]” and change the URL to the new repository’s URL.
#. Run the `fix:archive_repos REPOS=repo1,repo2 <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task on the repository.
#. Move the archive to the ``open-contracting-archive`` organization.
#. `Archive <https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>`__ the repository through its settings.
#. Run the `local:badges <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task.
