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

Frontend code is written for ECMAScript 6 (ES6) (`see the status of feature support in modern browsers <https://compat-table.github.io/compat-table/es6/>`__). We don't support `Internet Explorer 11 <https://death-to-ie11.com>`__.

.. tip::

   To transform older code to ECMAScript 6, use `lebab <https://github.com/lebab/lebab>`__, but be aware of its `bugs <https://github.com/lebab/lebab#unsafe-transforms>`__. There is a lebab `plugin <https://packagecontrol.io/packages/lebab>`__ for `Sublime Text <https://www.sublimetext.com>`__. Use these preferences (*Preferences* > *Package Settings* > *Lebab* > *Settings - User*):

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

   To transform newer code to ECMAScript 6, use `Babel <https://babeljs.io>`__ with the `defaults <https://babeljs.io/docs/options#no-targets>`__ query from `browserlist <https://github.com/browserslist/browserslist>`__.

Node
~~~~

Applications are written for the latest LTS version of Node. Packages are written for non-end-of-life versions (`see the status of Node versions <https://endoflife.date/nodejs>`__).

To upgrade Node, change the ``node-version`` key in GitHub Actions workflows and the ``node`` (or ``nikolaik/python-nodejs``) image in Dockerfiles. Check the relevant `changelog <https://github.com/nodejs/node/blob/main/CHANGELOG.md>`__ for breaking changes.

.. _javascript-preferences:

Preferences
-----------

Plain JavaScript is preferred to using jQuery, unless functionality depends on jQuery plugins. To replace jQuery in a project, refer to `You Might Not Need jQuery <https://youmightnotneedjquery.com>`__. Similarly, use the `Fetch <https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API>`__ API instead of the `Axios <https://axios-http.com>`__ package, etc.

Package manager
  `npm <https://docs.npmjs.com>`__, the default package manager of Node.js. Do not use `yarn <https://yarnpkg.com>`__. Yarn has no equivalent to ``npm audit fix``.
User interface
  `Vue <https://vuejs.org>`__ is preferred to `React <https://react.dev>`__. That said, do not use frameworks for simple interfaces.
Asset management
  `webpack <https://webpack.js.org>`__, unless a framework provides its own, like `Vue <https://cli.vuejs.org>`__.
Sass
  `sass <https://github.com/sass/dart-sass>`__ (dart-sass). Do not use `node-sass <https://github.com/sass/node-sass#node-sass>`__, which is deprecated.
Formatter
  `Biome <https://biomejs.dev>`__.

Requirements
------------

Use `npm <https://docs.npmjs.com>`__, not ``yarn``. Set the Node version in ``package.json``, `as documented <https://docs.npmjs.com/cli/v7/configuring-npm/package-json#engines>`__.

List outdated dependencies:

.. code-block:: bash

   npm outdated

Upgrade outdated dependencies:

.. code-block:: bash

   npm update

Upgrade Vue dependencies:

.. code-block:: bash

   vue upgrade --next

Vulnerabilities
~~~~~~~~~~~~~~~

.. admonition:: Dependabot alerts

   If the Dependabot alert is for a build dependency (like ``node-sass``) or a test dependency (like ``mocha``), you can dismiss it with "Risk is tolerable for this project". The npm ecosystem has `false positives <https://overreacted.io/npm-audit-broken-by-design/>`__.

To check for vulnerable dependencies:

.. code-block:: bash

   npm audit --production

.. note::

   ``npm audit`` (without ``--production``) has `false positives <https://overreacted.io/npm-audit-broken-by-design/>`__ (`Vue example <https://github.com/vuejs/vue-cli/issues/6686>`__).

To upgrade vulnerable dependencies:

#. Check the version of Node:

   .. code-block:: bash

      node --version

#. Upgrade npm:

   .. code-block:: bash

      npm install -g npm@latest

#. Run:

   .. code-block:: bash

      npm audit fix

#. Manually update version numbers in ``package.json``:

   #. Find a "fix available" line
   #. Read its following line ("Will install <package>@<version>")
   #. Check the package's changelog for changes between the two versions
   #. Update ``package.json``, and repeat

Code style
----------

package.json
~~~~~~~~~~~~

-  Do not set the `scripts <https://docs.npmjs.com/cli/v11/using-npm/scripts>`__ property. Instead, document the full commands in the readme, to reduce indirection and obfuscation.

Vue
~~~

-  When navigating between "pages", respect native browser behaviors (open in new tab, etc.) by using an ``<a>`` link or ``<router-link>``.

.. _javascript-ci:

Continuous integration
----------------------

Create a ``.github/workflows/js.yml`` file.

.. tip::

   In most cases, you can reuse the `js <https://github.com/open-contracting/.github/blob/main/.github/workflows/js.yml>`__ workflow. For example:

   .. code-block:: yaml

      name: Lint JavaScript
      on: [push, pull_request]
      jobs:
        lint:
          uses: open-contracting/.github/.github/workflows/js.yml@main
          permissions:
            contents: read

Reference
---------

-  `MDN Web Docs <https://developer.mozilla.org/en-US/>`__
-  `Can I use... <https://caniuse.com/>`__
