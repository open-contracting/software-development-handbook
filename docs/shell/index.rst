Shell script
============

File location
-------------

For builds that involve independent command-line tools, use `Make <https://www.gnu.org/software/make/>`__, and follow DataMade's `Making Data Guidelines <https://github.com/datamade/data-making-guidelines>`__ and Clark Grubb's `Makefile Style Guide <https://clarkgrubb.com/makefile-style-guide>`__.

.. admonition:: Examples

   - `standard_profile_template <https://github.com/open-contracting/standard_profile_template>`__

If a repository has scripts to set itself up and/or update itself, follow GitHub's `Scripts to Rule Them All <https://github.com/github/scripts-to-rule-them-all>`__.

.. admonition:: Examples

   -  `deploy <https://github.com/open-contracting/deploy/tree/master/script>`__
   -  `standard_profile_template <https://github.com/open-contracting/standard_profile_template/tree/master/script>`__

``bash`` and ``sh`` scripts should use the ``.sh`` extension, unless they are in a ``script/`` directory.

Shell options
-------------

Start a Bash script with `set -euo pipefail <https://wizardzines.com/comics/bash-errors/>`__. If the script explicitly handles unset variables, omit ``u``.
