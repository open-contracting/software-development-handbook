Shell script
============

Directory layout
----------------

For builds that involve independent command-line tools, use `Make <https://www.gnu.org/software/make/>`__, and follow DataMade's `Making Data Guidelines <https://github.com/datamade/data-making-guidelines>`__ and Clark Grubb's `Makefile Style Guide <https://clarkgrubb.com/makefile-style-guide>`__, for example: `standard_profile_template <https://github.com/open-contracting/standard_profile_template>`__

If a repository has scripts to set itself up and/or update itself, follow GitHub's `Scripts to Rule Them All <https://github.com/github/scripts-to-rule-them-all>`__, for example: `deploy <https://github.com/open-contracting/deploy/tree/main/script>`__ and `standard_profile_template <https://github.com/open-contracting/standard_profile_template/tree/latest/script>`__

Filename conventions
~~~~~~~~~~~~~~~~~~~~

``sh`` and ``bash`` scripts should use the ``.sh`` extension, unless they are in a ``script/`` directory.

Shell options
-------------

Start shell scripts with `set -euo pipefail <https://wizardzines.com/comics/bash-errors/>`__. If the script explicitly handles unset variables, omit ``-u``. To see which command failed due to the ``-e`` option, add ``-x``.

.. seealso::

   `The Set Builtin <https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html>`__

Code style
----------

Check ``/bin/sh`` scripts using `checkbashisms <https://manpages.debian.org/stable/devscripts/checkbashisms.1.en.html>`__.

Check shell scripts using `shellcheck <https://www.shellcheck.net>`__.

Style shell scripts using `shfmt <https://github.com/mvdan/sh>`__: for example, ``shfmt -w -i 4 -sr (shfmt -f .)``.

Use:

-  ``sh`` instead of ``bash``, where possible. Bash is needed for:

   -  `Shell Parameter Expansion <https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html>`__ (``//``, ``##``, ``%%``, etc.)
   -  `Process Substitution <https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html>`__ (``<()``)
   -  `The mapfile Builtin <https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html#index-mapfile>`__
   -  `The pipefail Option <https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html>`__

-  ``[ ]`` instead of ``test``
-  ``[ ]`` instead of ``[[ ]]`` in Bash, `unless required <https://www.gnu.org/software/bash/manual/bash.html#Bash-Conditional-Expressions>`__
-  ``$NAME`` instead of ``${NAME}``, unless followed by a word character
-  Subshells to temporarily change directory, for example:

   .. code-block:: bash

      (
         cd subdir/
         mv x.txt y.txt
      )

   Instead of:

   .. code-block:: bash

      cd subdir/
      mv x.txt y.txt
      cd ..  # AVOID

And:

-  Avoid ``set -x`` in scripts run by continuous integration, because it will expand any secret variables

.. _shell-ci:

Continuous integration
----------------------

Create a ``.github/workflows/shell.yml`` file with:

.. literalinclude:: samples/shell.yml
   :language: yaml

Reference
---------

-  `Shell Command Language <https://pubs.opengroup.org/onlinepubs/9699919799.2018edition/utilities/V3_chap02.html>`__
-  `Bash Conditional Constructs <https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html>`__
-  `Wizard Zines Bite Size series <https://wizardzines.com>`__
