Git
===

Commit messages
---------------

Follow the format:

.. code-block:: none

   type(scope): Capitalized, <72 characters, no period

   A longer description of paragraph text, as needed.

   - Bullet points and other Markdown are okay, too

   #123

Most commits are made in pull requests, such that it's easy to find the related conversation on GitHub. As such, it's not necessary to provide a long narrative, if it exists in a pull request or linked issue.

Reference:

- `Angular Commit Message Format <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit-message-header>`__
- `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__
- `Write joyous git commit messages <https://joshuatauberer.medium.com/write-joyous-git-commit-messages-2f98891114c4>`__

Feature branches
----------------

In general, repositories should have only a default branch and pull request branches. If the repository is a fork, it may have a main branch for the source branch and an ``opencontracting`` (or ``open_contracting``) branch for the fork branch.

To start work on an issue, create a branch, following this naming convention:

.. code-block:: none

   {issue-number}-{brief-description}

This makes it easy to know what the changes in a branch are about.

.. note::

   If no issue exists for the work you want to do, please create an issue first.
