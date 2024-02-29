Git
===

Configuration
-------------

We recommend using:

.. code-block:: bash

   git config --global init.defaultBranch main
   git config --global push.autoSetupRemote true
   git config --global merge.conflictstyle zdiff3
   git config --global diff.algorithm histogram
   git config --global diff.colorMoved default
   git config --global diff.colorMovedWS allow-indentation-change

You might also like (requires installing `difftastic <https://difftastic.wilfred.me.uk/installation.html>`__):

.. code-block:: bash

   git config --global diff.tool difftastic

If you sign commits, `tell Git about your signing key <https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key>`__, for example:

.. code-block:: bash

   git config --global user.signingkey 3AA5C34371567BD2
   git config --global commit.gpgsign true
   git config --global gpg.program $(which gpg)

.. seealso::

   `Popular git config options <https://jvns.ca/blog/2024/02/16/popular-git-config-options/>`__

Commit messages
---------------

Follow the format:

.. code-block:: none

   type(scope): Capitalized, <72 characters, no period

   A longer description of paragraph text, as needed.

   - Bullet points and other Markdown are okay, too

   #123

Most commits are made in pull requests, such that it's easy to find the discussion on GitHub. As such, it's not necessary to provide a long narrative, if it exists in a pull request or linked issue.

Reference:

- `Angular Commit Message Format <https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit-message-header>`__
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
