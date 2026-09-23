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

Onboard consultants / Start a project
-------------------------------------

#. Create `new repositories <https://github.com/orgs/open-contracting/repositories>`__, as needed by the consultants
#. Run the `fix:lint_repos <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task, to configure the repository
#. Create a `new team <https://github.com/orgs/open-contracting/teams>`__ named after the consultants' organization

   .. note::

      Do not use `outside collaborators <https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-outside-collaborators/adding-outside-collaborators-to-repositories-in-your-organization>`__. Add individual consultants to appropriate teams, like the `Standard <https://github.com/orgs/open-contracting/teams/standard>`__ team.

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

#. Add the new repositories to the `appropriate rulesets <https://github.com/organizations/open-contracting/settings/rules>`__, as described in :ref:`workflow-contexts`
#. If the repository has a ``requirements_dev.txt`` file, so that the :ref:`lint.yml workflow<linting-ci>` auto-fixes requirements files:

   #. Install the `open-contracting-requirements <https://github.com/organizations/open-contracting/settings/installations/162530796>`__ app on the new repositories
   #. Add the new repositories to the ``APP_CLIENT_ID`` and ``APP_PRIVATE_KEY`` secrets, in both the `Actions <https://github.com/organizations/open-contracting/settings/secrets/actions>`__ and `Dependabot <https://github.com/organizations/open-contracting/settings/secrets/dependabot>`__ stores
   #. Pass the secrets to the workflow:

      .. code-block:: yaml
         :emphasize-lines: 6-8

         jobs:
           lint:
             uses: open-contracting/.github/.github/workflows/lint.yml@main
             permissions:
               contents: write
             secrets:
               client-id: ${{ secrets.APP_CLIENT_ID }}
               private-key: ${{ secrets.APP_PRIVATE_KEY }}

#. Add the new repositories to `pre-commit ci <https://github.com/organizations/open-contracting/settings/installations/20658712>`__
#. Add any projects to :ref:`ReadTheDocs<readthedocs>` as appropriate
#. Use the :doc:`Django Cookiecutter template<../python/django>`, if relevant

Per the `Software terms of reference (TOR) template <https://docs.google.com/document/d/13-_eFQrelLdj92MWTiqzAfO62in7Xxrv3DTcmRqvNjE/edit>`__, consultants should not have access to the production server. As such, do not add any members to the `Servers <https://github.com/orgs/open-contracting/teams/servers>`__ team.

.. warning::

   **NEVER** assign the Owner role to non-OCP staff. The Owner role has access to a private repository with multi-factor authentication backup codes. `Transferring a repository <https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository>`__ does not require the Owner role.

.. tip::

   Update and then use the `org:members <https://github.com/open-contracting/standard-maintenance-scripts#access-tasks->`__, ``org:team_members``, ``org:team_repos`` and ``org:team_perms`` tasks to check the configuration.

.. note::

   In order to protect the private deploy repositories, the `base permissions <https://github.com/organizations/open-contracting/settings/member_privileges>`__ for ``open-contracting`` members is *None*.

.. note::

   A `custom security configuration <https://docs.github.com/en/code-security/how-tos/secure-at-scale/configure-organization-security/establish-complete-coverage/apply-custom-configuration>`__ is applied to all new repositories.

.. _workflow-contexts:

Add a workflow to a repository
------------------------------

A ruleset requires a status check by its *context*, which is the name that GitHub gives to a job's result. A job calling a reusable workflow reports ``<caller job ID> / <called job ID>``; a job calling no reusable workflow reports its job ID alone; and a matrix job reports one context per combination, like ``build (ubuntu-latest)``.

Only a workflow triggered by ``push`` or ``pull_request`` reports a context on a pull request. A workflow triggered by another event like ``workflow_run`` reports no context; therefore, its contexts are never required.

#. Use a consistent job ID in the caller, so that the repository reports the context that the ruleset requires:

   .. list-table::
      :header-rows: 1

      * - Reusable workflow
        - Job ID
        - Context
        - Ruleset
      * - ``lint.yml``
        - ``lint``
        - ``lint / build``
        - Require status check to pass: lint
      * - ``js.yml``
        - ``js``
        - ``js / build``
        - Require status check to pass: js
      * - ``shell.yml``
        - ``shell``
        - ``shell / build``
        - Require status check to pass: shell
      * - ``spellcheck.yml``
        - ``spellcheck``
        - ``spellcheck / build``
        - Require status check to pass: spellcheck
      * - ``i18n-babel.yml``, ``i18n-django.yml``
        - ``i18n``
        - ``i18n / build``
        - Require status check to pass: i18n
      * - ``ci-profile.yml``
        - ``ci``
        - ``ci / build``
        - Require status check to pass: ci
      * - N/A
        - ``build``
        - ``build``
        - Require status check to pass: build (ci, pypi, a11y, php, lint rust)

#. If the workflow has a matrix job or multiple jobs, add a ``build`` job that summarizes them:

   .. code-block:: yaml

      jobs:
        test:
          runs-on: ubuntu-latest
          ...
        nonlinux:
          runs-on: ${{ matrix.os }}
          strategy:
            matrix:
              os: [macos-latest, windows-latest]
          ...
        # Without `if: always()`, a failed dependency would skip `build`, and a skipped job satisfies a required status check.
        build:
          needs: [test, nonlinux]
          if: always()
          runs-on: ubuntu-latest
          steps:
            - if: ${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') }}
              run: exit 1

#. Add the repository to the matching `ruleset <https://github.com/organizations/open-contracting/settings/rules>`__, to require the context.
#. If the repository has no ``lint.yml`` workflow, add it to the ``lint`` ruleset's exclusion list, as that ruleset targets all repositories.

.. note::

   The `open-contracting-extensions <https://github.com/organizations/open-contracting-extensions/settings/rules>`__ organization groups its rulesets: ``Require status checks to pass: lint`` targets all repositories, and ``Require status checks to pass: ci, js, shell, spellcheck`` targets the profiles.

.. tip::

   Use the `repos:status_checks <https://github.com/open-contracting/standard-maintenance-scripts#review-github-repository-metadata-and-configuration->`__ task to report repositories whose required status checks don't match GitHub Actions workflows.

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

   To protect a new repository, add it to the appropriate rulesets, as described in :ref:`workflow-contexts`.

Branches are protected by `organization rulesets <https://github.com/organizations/open-contracting/settings/rules>`__. A repository's rules are the aggregate of every ruleset that targets it, so a repository needs no configuration of its own.

Broadly, the rulesets enforce two policies:

-  Deletions and force pushes are blocked on the default branch of every repository, with no bypass.
-  A push is rejected if its commits' required status checks aren't already passing. The rulesets that set the required status checks can be bypassed by Admin roles, and by the ``open-contracting-requirements`` app, whose auto-commit is pushed before any workflow runs on it.

A repository with release branches (like the standard and profiles) sets the bypass according to the branch's maturity:

-  Before 1.0, a branch (like ``0.9`` or ``0.9-dev``) can be bypassed.
-  From 1.0 onwards, a release branch (like ``1.0``) is in a "No bypass" ruleset.
-  From 1.0 onwards, a development branch (like ``1.0-dev``) is in a "No bypass" ruleset in the ``standard`` and ``infrastructure`` repositories only.

We don't generally enable the following behaviors for the provided reasons:

-  **Require branches to be up to date before merging**: While this may avoid introducing errors, it slows development in an environment in which there are many simultaneous pull requests, because each would require an extra step before merging. If the automated tests fail after merging, the error can be corrected, or the changes can be reverted.
-  **Required approvals**: While this is a best practice, it slows development as the team is not sufficiently large to staff it. It is okay, for example, for an author to self-merge a simple change. Authors should, of course, request reviews for significant changes. An approval is required, however, in a software repository to which an external partner has write access, unless that partner is its principal developer.

If a repository needs multiple branches (like the standard and profiles), the needed branches should be matched by a ruleset. Otherwise, unmatched branches more than a month old should either be opened as pull requests, or deleted.

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
#. Run the `local:badges <https://github.com/open-contracting/standard-maintenance-scripts#miscellaneous-tasks>`__ task.
