For developers
==============

Issues
------

Automatically close issues with pull requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating a pull request that fixes one or more issues, add the text “fixes #42” or “closes #42” in the pull request’s description so that GitHub `automatically closes them after merging <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue>`__.

Manually close issues
~~~~~~~~~~~~~~~~~~~~~

All issues should be closed with a brief rationale. This makes it easy to understand what happened and affords participants an opportunity to engage with the rationale. For example:

-  “Resolved in the above commit” if there’s a commit referencing the issue that appears nearby
-  “Resolved in the [name] extension” with a link to the extension that was created
-  “Closing, because [explanation]”

Pull requests
-------------

**DO NOT** force-push changes to a pull request in response to a code review. Force-pushing makes it impossible to use GitHub's *View changes* feature. If you want a single commit, select `Squash and merge <https://docs.github.com/en/github/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>`__ from the *Merge pull request* dropdown.

Projects
--------

The ``open-contracting`` `organization <https://github.com/orgs/open-contracting/projects>`__ uses `GitHub Projects <https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards>`__ to organize work in a `Kanban <https://en.wikipedia.org/wiki/Kanban>`__ system.

We also have an `agile board <https://crm.open-contracting.org/projects/ocds-team-tools-development-portfolio/agile/board>`__ in the CRM. Its uses and features are distinct (e.g. time tracking) and complementary (e.g. long-term project management) to what GitHub offers.

People expect to have visibility of all of a repository’s issues within the *Issues* tab; therefore, a card that is not attached to an issue should never be added to a project.

New projects should be created using the *Automated kanban* template.
