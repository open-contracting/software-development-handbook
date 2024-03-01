Git
===

Configuration
-------------

Add the following to your ``~/.config/git/ignore`` file:

.. code-block:: none

   /coverage
   .DS_Store
   .sass_cache
   *.pyc

We recommend using:

.. code-block:: bash

   # Create a "main" branch (instead of a "master" branch) when creating repositories.
   git config --global init.defaultBranch main

   # Use --set-upstream (-u) with `git push` by default.
   git config --global push.autoSetupRemote true

   # Ignore the commits in this file (if it exists), like code formatting or file renaming.
   git config --global blame.ignoreRevsFile .git-blame-ignore-revs

   # See demo at https://ductile.systems/zdiff3/
   git config --global merge.conflictstyle zdiff3

   # Display dates as 2001-02-03 04:05:06 instead of Sat Feb 3 04:05:06 2001.
   git config --global log.date iso

   # Detect moved lines better.
   git config --global diff.algorithm histogram
   # Use different colors for moved lines (minimum 20 characters).
   git config --global diff.colorMoved default
   # Allow indentation changes when detecting moved lines.
   git config --global diff.colorMovedWS allow-indentation-change

   # Delete branches/tags locally that were deleted remotely (e.g. after merge on GitHub).
   git config --global fetch.prune true
   git config --global fetch.pruneTags true

You might also like `delta <https://github.com/dandavison/delta#readme>`__ (`installed separately <https://difftastic.wilfred.me.uk/installation.html>`__).

If you sign commits, `tell Git about your signing key <https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key>`__, for example:

.. code-block:: bash

   git config --global commit.gpgsign true

.. tab-set::

   .. tab-item:: SSH key

      .. code-block:: bash

         git config --global --unset gpg.program
         git config --global gpg.format ssh
         git config --global user.signingkey ~/.ssh/id_rsa.pub

   .. tab-item:: GPG key

      .. code-block:: bash

         git config --global --unset gpg.format
         git config --global user.signingkey 3AA5C34371567BD2
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
