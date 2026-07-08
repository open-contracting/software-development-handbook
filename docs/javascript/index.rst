JavaScript and TypeScript
=========================

.. note::

   Don't use `CoffeeScript <https://coffeescript.org>`__. Unless the repository is a fork, use `Decaffeinate <https://decaffeinate-project.org>`__ to convert CoffeeScript to ECMAScript.

.. _javascript-license:

License
-------

Use the `MIT license <https://choosealicense.com/licenses/mit/>`__.

Version
-------

ECMAScript
~~~~~~~~~~

Write modern JavaScript. If needed, use a :ref:`bundler<esbuild>` to transpile code for older browsers.

.. dropdown:: Modernizing legacy code

   Use `lebab <https://github.com/lebab/lebab>`__, but be aware of its `bugs <https://github.com/lebab/lebab#unsafe-transforms>`__. There is a lebab `plugin <https://packagecontrol.io/packages/lebab>`__ for `Sublime Text <https://www.sublimetext.com>`__. Use these preferences (*Preferences* > *Package Settings* > *Lebab* > *Settings - User*):

   .. code-block:: json

      {
        "transforms": [
          "arrow",
          "arrow-return",
          "let",
          "for-of",
          "for-each",
          "arg-rest",
          "arg-spread",
          "obj-method",
          "obj-shorthand",
          "no-strict",
          "exponent",
          "class",
          "commonjs",
          "template",
          "default-param",
          "includes"
        ]
      }

Node
~~~~

Applications are written for the latest LTS version of Node. Packages are written for non-end-of-life versions (`see the status of Node versions <https://endoflife.date/nodejs>`__).

To upgrade Node, change the ``node-version`` key in GitHub Actions workflows and the ``node`` (or ``nikolaik/python-nodejs``) image in Dockerfiles. Check the relevant `changelog <https://github.com/nodejs/node/blob/main/CHANGELOG.md>`__ for breaking changes.

.. _javascript-preferences:

Preferences
-----------

Use plain JavasScript:

-  Do not use `lodash <https://lodash.com>`__ or `underscore <https://underscorejs.org>`__.
-  Do not use `axios <https://axios-http.com>`__. Use the `Fetch API <https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API>`__.
-  Do not use jQuery, unless existing functionality depends on jQuery plugins. To replace jQuery, refer to `You Might Not Need jQuery <https://youmightnotneedjquery.com>`__.

Package manager
  `pnpm <https://pnpm.io>`__, for its built-in supply-chain protections (`dependency cooldown <https://pnpm.io/settings#minimumreleaseage>`__, `trust policy <https://pnpm.io/settings#trustpolicy>`__, `build scripts blocked by default <https://pnpm.io/global-packages#build-script-approval>`__) and its improved `node_modules structure <https://pnpm.io/symlinked-node-modules-structure>`__. Do not use `npm <https://docs.npmjs.com>`__ or `yarn <https://yarnpkg.com>`__.
Framework
  `Vue <https://vuejs.org>`__ is preferred to `React <https://react.dev>`__. That said, do not use frameworks for simple interfaces.
Bundler
  `esbuild <https://esbuild.github.io>`__ to bundle assets for a server-rendered application (e.g. assets referenced by ``script`` tags in Django templates) or for an npm package. `Vite <https://vite.dev>`__ for a single-page application.
Sass
  `sass <https://github.com/sass/dart-sass>`__ (dart-sass). Do not use `node-sass <https://github.com/sass/node-sass#node-sass>`__, which is deprecated.
Formatter
  `Biome <https://biomejs.dev>`__. Do not use `Prettier <https://prettier.io>`__.
Linter
  `Biome <https://biomejs.dev>`__. Do not use `ESLint <https://eslint.org>`__.

Requirements
------------

Set the pnpm version in the `packageManager <https://nodejs.org/api/packages.html#packagemanager>`__ property of ``package.json``.

List outdated dependencies:

.. code-block:: bash

   pnpm outdated

Upgrade outdated dependencies:

.. code-block:: bash

   pnpm update

Upgrade Vue dependencies:

.. code-block:: bash

   vue upgrade --next

.. _javascript-supply-chain:

Supply chain
~~~~~~~~~~~~

To protect against supply chain attacks, set in ``pnpm-workspace.yaml``:

.. code-block:: yaml

   minimumReleaseAge: 10080
   trustPolicy: no-downgrade

``no-downgrade`` has false positives if packages drop provenance attestation. Exclude the versions that ``pnpm install`` reports:

.. code-block:: yaml

   trustPolicyExclude:
     - chokidar@4.0.3
     - semver@6.3.1

By default, pnpm enables ``minimumReleaseAge`` (1 day) and ``blockExoticSubdeps`` (prevents transitive dependencies from using git or tarballs).

Vulnerabilities
~~~~~~~~~~~~~~~

.. admonition:: Dependabot alerts

   If the Dependabot alert is for a build dependency (like ``node-sass``) or a test dependency (like ``mocha``), you can dismiss it with "Risk is tolerable for this project". The npm ecosystem has `false positives <https://overreacted.io/npm-audit-broken-by-design/>`__.

To check for vulnerable dependencies:

.. code-block:: bash

   pnpm audit --prod

.. note::

   ``pnpm audit`` (without ``--prod``) has `false positives <https://overreacted.io/npm-audit-broken-by-design/>`__ (`Vue example <https://github.com/vuejs/vue-cli/issues/6686>`__).

To upgrade vulnerable dependencies:

.. code-block:: bash

   pnpm audit --fix update

This updates the lockfile to non-vulnerable versions, where the dependency ranges allow it. Check each package's changelog before committing.

Where the dependency ranges don't allow it, ``pnpm audit --fix override`` can add ``overrides`` to ``package.json`` to force non-vulnerable versions, instead.

Linting
~~~~~~~

Use `knip <https://knip.dev>`__ to find unused files, dependencies and exports. Install it as a development dependency, configure it in a ``knip.jsonc`` file, and keep it up-to-date with :ref:`dependabot`:

.. code-block:: yaml
   :caption: .github/dependabot.yml

   - package-ecosystem: "npm"
     directories:
       - "/"
       - "**/*"
     schedule:
       interval: "yearly"
     allow:
       - dependency-name: "knip"
     cooldown:
       default-days: 7

:ref:`javascript-ci` runs knip if you reuse the ``js`` workflow.

Code style
----------

package.json
~~~~~~~~~~~~

-  Do not set the `scripts <https://docs.npmjs.com/cli/v11/using-npm/scripts>`__ property. Instead, document the full commands in the readme, to reduce indirection and obfuscation.

.. _biome:

Biome
~~~~~

.. seealso:: `Biome configuration reference <https://biomejs.dev/reference/configuration/>`__

Check and style `many languages <https://biomejs.dev/internals/language-support/>`__ using `Biome <https://biomejs.dev>`__. For example:

.. code-block:: json
   :caption: biome.json

   {
     "vcs": {
       "enabled": true,
       "clientKind": "git",
       "useIgnoreFile": true,
       "defaultBranch": "main"
     },
     "assist": {
       "actions": {
         "source": {
           "organizeImports": "on"
         }
       }
     },
     "formatter": {
       "indentStyle": "space",
       "indentWidth": 4,
       "lineWidth": 119
     },
     "json": {
       "formatter": {
         "indentWidth": 2
       }
     },
     "linter": {
       "enabled": true,
       "rules": {
         "recommended": true
       }
     }
   }

Run Biome with :ref:`pre-commit<linting-pre-commit>`:

.. code-block:: yaml
   :caption: .pre-commit-config.yaml

   repos:
     - repo: https://github.com/biomejs/pre-commit
       rev: v2.5.2
       hooks:
         - id: biome-check

:ref:`javascript-ci` runs Biome if you reuse the ``js`` workflow.

Vue
~~~

-  When navigating between "pages", respect native browser behaviors (open in new tab, etc.) by using an ``<a>`` link or ``<router-link>``.

.. _javascript-ci:

Continuous integration
----------------------

.. important::

   In GitHub workflows, install project dependencies safely with:

   .. code-block:: yaml

      - run: pnpm install --frozen-lockfile --ignore-scripts

Create a ``.github/workflows/js.yml`` file. In most cases, you can reuse the `js <https://github.com/open-contracting/.github/blob/main/.github/workflows/js.yml>`__ workflow, like:

.. code-block:: yaml

   name: Lint JavaScript
   on: [push, pull_request]
   jobs:
     lint:
       uses: open-contracting/.github/.github/workflows/js.yml@main
       permissions:
         contents: read

If you don't use this workflow, and the project uses npm, include this step:

.. code-block:: yaml

   - run: npx lockfile-lint --path package-lock.json --type npm --allowed-hosts npm --validate-https

Reference
---------

-  `MDN Web Docs <https://developer.mozilla.org/en-US/>`__
-  `Can I use... <https://caniuse.com/>`__
