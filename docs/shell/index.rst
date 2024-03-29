Shell script
============

Directory layout
----------------

For builds that involve independent command-line tools, use `Make <https://www.gnu.org/software/make/>`__, and follow DataMade's `Making Data Guidelines <https://github.com/datamade/data-making-guidelines>`__ and Clark Grubb's `Makefile Style Guide <https://clarkgrubb.com/makefile-style-guide>`__. Examples: `standard_profile_template <https://github.com/open-contracting/standard_profile_template>`__

If a repository has scripts to set itself up and/or update itself, follow GitHub's `Scripts to Rule Them All <https://github.com/github/scripts-to-rule-them-all>`__. Examples: `deploy <https://github.com/open-contracting/deploy/tree/main/script>`__, `standard_profile_template <https://github.com/open-contracting/standard_profile_template/tree/latest/script>`__

Filename conventions
~~~~~~~~~~~~~~~~~~~~

``bash`` and ``sh`` scripts should use the ``.sh`` extension, unless they are in a ``script/`` directory.

Shell options
-------------

Start a Bash script with `set -euo pipefail <https://wizardzines.com/comics/bash-errors/>`__. If the script explicitly handles unset variables, omit ``-u``. To see which command failed due to the ``-e`` option, add ``-x``.

Reference: `The Set Builtin <https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html>`__

Code style
----------

Check shell scripts using `shellcheck <https://www.shellcheck.net>`__.

Style shell scripts using `shfmt <https://github.com/mvdan/sh>`__: for example, ``shfmt -w -i 4 -sr (shfmt -f .)``.

Use:

-  ``[ ]`` instead of ``test``
-  ``[ ]`` instead of ``[[ ]]``, `unless required <https://www.gnu.org/software/bash/manual/bash.html#Bash-Conditional-Expressions>`__
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

Avoid:

-  ``set -x`` in scripts run by continuous integration, because it will expand any secret variables

.. _shell-ci:

Continuous integration
----------------------

Create a ``.github/workflows/shell.yml`` file with:

.. literalinclude:: samples/shell.yml
   :language: yaml

Reference
---------

-  `Shell Parameter Expansion <https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html>`__ (``##``, ``%%``, etc.)
-  `Conditional Constructs <https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html>`__ (``=``, ``=~``, etc.)
-  `Wizard Zines Bite Size series <https://wizardzines.com>`__
