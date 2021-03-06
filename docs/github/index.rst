GitHub
======

Organizations
-------------

-  `open-contracting <https://github.com/open-contracting/>`__: all repositories supported by OCP
-  `open-contracting-extensions <https://github.com/open-contracting-extensions/>`__: OCDS extensions and OCDS profiles
-  `open-contracting-archive <https://github.com/open-contracting-archive/>`__: all unsupported repositories
-  `open-contracting-partnership <https://github.com/open-contracting-partnership/>`__: `www.open-contracting.org <https://www.open-contracting.org/>`__-related repositories

.. _github-teams:

Teams
-----

In order to protect the private deploy repositories, the `base permissions <https://github.com/organizations/open-contracting/settings/member_privileges>`__ for ``open-contracting`` members is *None*. There are two main teams, with additional teams for specific projects:

-  `General <https://github.com/orgs/open-contracting/teams/general>`__:

   -  **Members**: All `people <https://github.com/orgs/open-contracting/people>`__ from OCP, Centro de Desarrollo Sostenible (CDS) and Open Data Services Co-operative Limited (ODS)
   -  **Repositories**: All repositories, except `archived <https://github.com/open-contracting?type=archived>`__, `deploy <https://github.com/search?q=topic%3Adeployment+org%3Aopen-contracting>`__ and `health <https://github.com/orgs/open-contracting/teams/health/repositories>`__ repositories
   -  **Permission levels**: *Triage* for issue-only repositories, *Write* for other repositories

-  `Servers <https://github.com/orgs/open-contracting/teams/servers>`__:

   -  **Members**: All people with `root access <https://ocdsdeploy.readthedocs.io/en/latest/reference/index.html#root-access>`__ to any server
   -  **Repositories**: The `deploy <https://github.com/search?q=topic%3Adeployment+org%3Aopen-contracting>`__ repositories
   -  **Permission levels**: *Write*

GitHub’s `outside collaborators <https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/adding-outside-collaborators-to-repositories-in-your-organization>`__ feature should only be used for one-off projects.

There should be a minimum of two `owners <https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/permission-levels-for-an-organization>`__ from OCP. Owners do not need to be added to teams.

.. warning::

   **NEVER** assign the Owner role to non-OCP staff. The Owner role has access to a private repository with multi-factor authentication backup codes. `Transferring a repository <https://docs.github.com/en/github/administering-a-repository/managing-repository-settings/transferring-a-repository>`__ does not require the Owner role.

Issues
------

Reporting incorrect behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Write a brief, clear and specific issue title
#. Provide sufficient detail in the issue description

You can use this template for the issue description:

What were you trying to do?
  Describe the expected behavior. List *every* step to reproduce the incorrect behavior. Assume the reader is unfamilar with the tool. Attach any input data to the issue (you might need to save as TXT or ZIP). If you are working on the command-line, paste the specific commands.
What error did you receive?
  Provide the entire output, error message and stacktrace, if available. Do not omit any output, as this will delay resolution. If part of the output is large, attach it to the issue instead (you might need to save as TXT or ZIP). If the tool has a graphical interface, you can attach screenshots to illustrate.
What is your environment?
  Where relevant, please provide: tool's version, web browser name and version, operating system name and version (the precise version like "10.15.6", not the major version like "Catalina") and/or Python version.
Did you attempt a fix?
  If so, describe what you did.
How soon do you need a fix?
  If unspecified, no urgency is assumed.

.. note::

   The Data Review Tool expires results pages, so please attach the input data instead of linking to the results page.

.. note::

   Data publishers can change their data at any time. Please attach a copy of the data instead of linking to it.

Managing long issues
~~~~~~~~~~~~~~~~~~~~

Some issues produce long discussions, and the original intent of the issue may change over time; this can make it more difficult to catch up on the current state of the issue. To deal with this, the issue’s description should be edited to reflect the current state of the issue, summarize the discussion so far, and link to the most recent comment from which the discussion may continue.

Restarting the discussion with a new issue causes the following problems:

-  Old participants aren’t notified of activity on the new issue, and need to subscribe to it.
-  New participants need to read all issues referencing the new issue to rebuild the context.
-  If the old issue is closed in favor of a new issue, and the new issue is thereafter not resolved but is closed (for whatever reason, like insufficient demand), a reader of the old issue may assume that the new issue is either open or resolved. They would need to follow the chain to realize that it’s unresolved and closed, before adding a comment to say, “I need this.”

Automatically closing issues with pull requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating a pull request that fixes one or more issues, add the text “fixes #42” or “closes #42” in the pull request’s description so that GitHub `automatically closes them after merging <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue>`__.

Manually closing issues
~~~~~~~~~~~~~~~~~~~~~~~

All issues should be closed with a brief rationale. This makes it easy to understand what happened and affords participants an opportunity to engage with the rationale. For example:

-  “Resolved in the above commit” if there’s a commit referencing the issue that appears nearby
-  “Resolved in the [name] extension” with a link to the extension that was created
-  “Closing, because [explanation]”

Projects
--------

The ``open-contracting`` `organization <https://github.com/orgs/open-contracting/projects>`__ uses `GitHub Projects <https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards>`__ to organize work in a `Kanban <https://en.wikipedia.org/wiki/Kanban>`__ system.

We also have an `agile board <https://crm.open-contracting.org/projects/ocds-team-tools-development-portfolio/agile/board>`__ in the CRM. Its uses and features are distinct (e.g. time tracking) and complementary (e.g. long-term project management) to what GitHub offers.

People expect to have visibility of all of a repository’s issues within the *Issues* tab; therefore, a card that is not attached to an issue should never be added to a project.

New projects should be created using the *Automated kanban* template.

Branches
--------

In general, repositories should have only a default branch and pull request branches. If the repository is a fork, it may have a main branch for the source branch and an ``opencontracting`` (or ``open_contracting``) branch for the fork branch.

If a repository needs multiple branches (like the standard and profiles), the needed branches should be protected. Otherwise, unprotected branches more than a month old should either be opened as pull requests, protected, or deleted.

See the pages for the branch management of the `standard <https://ocds-standard-development-handbook.readthedocs.io/en/latest/standard/technical/repository.html>`__ and `profiles <https://ocds-standard-development-handbook.readthedocs.io/en/latest/profiles/technical/repository.html>`__ (including OC4IDS).

Naming convention
~~~~~~~~~~~~~~~~~

To start work on an issue, create a branch, following this naming convention:

.. code-block:: none

   {issue-number}-{brief-description}

This makes it easy to know what the changes in a branch are about.

.. note::

   If no issue exists for the work you want to do, please create an issue first.

Commits
-------

**DO NOT** force-push changes to a pull request in response to a code review. Force-pushing makes it impossible to use GitHub's *View changes* feature. If you want a single commit, select `Squash and merge <https://docs.github.com/en/github/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>`__ from the *Merge pull request* dropdown.


Commit messages
~~~~~~~~~~~~~~~

Follow the format:

.. code-block:: none

   type(scope): Capitalized, <72 characters, no period

   A longer description of paragraph text, as needed.

   - Bullet points and other Markdown are okay, too

   #123

Most commits are made in pull requests, such that it's easy to find the related conversation on GitHub.

Reference: `Angular Commit Message Format <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit-message-header>`__

Reference: `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__

Reference: `Write joyous git commit messages <https://joshuatauberer.medium.com/write-joyous-git-commit-messages-2f98891114c4>`__

Repository settings
-------------------

Metadata
~~~~~~~~

#. Add a description. The description should not describe the project’s status (‘draft’), because people frequently forget to update repository descriptions. Describe the status in the readme instead.
#. Add a website to the repository, if relevant: for example, a link to a deployment of the tool or to its documentation.

The `fix:lint_repos <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ Rake task otherwise normalizes configurations.

.. _branch-protection:

Branch protection
~~~~~~~~~~~~~~~~~

The `fix:protect_branches <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ Rake task in `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts>`__ protects default branches.

We don’t generally enable the following behaviors on `protected branches <https://docs.github.com/en/github/administering-a-repository/defining-the-mergeability-of-pull-requests/about-protected-branches>`__ for the provided reasons:

-  **Require branches to be up to date before merging**: While this may avoid introducing errors, it slows development in an environment in which there are many simultaneous pull requests, because each would require an extra step before merging. If the automated tests fail after merging, the error can be corrected, or the changes can be reverted.
-  **Require pull request reviews before merging**: While this is a best practice, it slows development as the team is not sufficiently large to staff it. It is okay, for example, for an author to self-merge a simple change. Authors may, of course, request reviews for significant changes.

Archival
~~~~~~~~

Repositories that are no longer supported should be archived.

#. Agree whether to archive the repository. The archived repositories presently include:

   -  Superseded repositories (e.g. `json-merge-patch <https://github.com/OpenDataServices/json-merge-patch>`__ supersedes `jsonmerge <https://github.com/open-contracting-archive/jsonmerge>`__)
   -  Abandoned extensions (e.g. `ocds-equityTransferCaps-extension <https://github.com/open-contracting-archive/ocds-equityTransferCaps-extension>`__)
   -  Merged changes to the core standard, expressed as extension repositories (``ocds_upgrade_###``)
   -  Exploratory repositories from pre-1.0 and pre-2015

#. Scan the repository’s open issues, milestones, pull requests and non-default branches in case any can be quickly closed, merged or deleted. Counter `GitHub’s recommendation <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/archiving-a-github-repository/about-archiving-repositories>`__, open issues and pull requests indicate the development status of a repository, and should be left open.
#. Change the repository’s description to describe the reason for archival. If the repository has been superseded, change it to “Superseded by [owner]/[repository]” and change the URL to the new repository’s URL.
#. Run the `fix:archive_repos REPOS=repo1,repo2 <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task on the repository.
#. Move the archive to the ``open-contracting-archive`` organization.
#. `Archive <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/archiving-a-github-repository/about-archiving-repositories>`__ the repository through its settings.
#. Run the `local:badges <https://github.com/open-contracting/standard-maintenance-scripts#change-github-repository-configuration>`__ task.

Integrations
------------

-  **Coveralls**, to measure test coverage (:ref:`see setup instructions<code-coverage>`)
-  **ReadTheDocs**, to build repository-specific documentation (`access all docs <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/badges.md#readme>`__)
-  **GitHub Actions**, to run tests, and to build documentation (`view all badges <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/badges.md#readme>`__)
-  **Code Climate**, to monitor maintanability (`view all badges <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/badges.md#readme>`__)
