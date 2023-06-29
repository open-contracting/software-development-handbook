For developers
==============

.. seealso::

   :doc:`Git guide<../git/index>`

Assign issues
-------------

If an issue is assigned to you and you need clarification from OCP, you can re-assign the issue to OCP, so that it no longer appears in your `assigned issues <https://github.com/issues/assigned>`__.

Close issues
------------

If OCP asks a question, **DO NOT** close the issue after providing the answer. Instead, you can re-assign the issue to OCP. The issue is not closed until OCP has an opportunity to act on the provided information.

Automatically, with pull requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating a pull request that fixes one or more issues, add the text “fixes #42” or “closes #42” in the pull request’s description so that GitHub `automatically closes them after merging <https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue>`__.

Manually, with a rationale
~~~~~~~~~~~~~~~~~~~~~~~~~~

All issues should be closed with a brief rationale. This makes it easy to understand what happened and affords participants an opportunity to engage with the rationale. For example:

-  “Resolved in the above commit” if there’s a commit referencing the issue that appears nearby
-  “Resolved in the [name] extension” with a link to the OCDS extension that was created
-  “Closing, because [explanation]”

Pull requests
-------------

**DO NOT** force-push changes to a pull request in response to a code review. Force-pushing makes it impossible to use GitHub's *View changes* feature. If you want a single commit, select `Squash and merge <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges>`__ from the *Merge pull request* dropdown.

Projects
--------

The ``open-contracting`` `organization <https://github.com/orgs/open-contracting/projects?query=is%3Aopen>`__ uses `GitHub Projects <https://docs.github.com/en/issues/organizing-your-work-with-project-boards/managing-project-boards/about-project-boards>`__ to organize work in a `Kanban <https://en.wikipedia.org/wiki/Kanban>`__ system.

People expect to have visibility of all of a repository’s issues within the *Issues* tab; therefore, a card that is not attached to an issue should never be added to a project.

New projects should be created using the *Automated kanban* template.
