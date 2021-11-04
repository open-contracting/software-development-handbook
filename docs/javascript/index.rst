JavaScript
==========

Version
-------

Frontend code is written for ECMAScript 6 (ES6) (`see the status of feature support in modern browsers <https://kangax.github.io/compat-table/es6/>`__). We don't support `Internet Explorer 11 <https://death-to-ie11.com>`__.

.. note::

   Don't use `CoffeeScript <https://coffeescript.org>`__. Unless the repository is a fork, use `Decaffeinate <https://decaffeinate-project.org>`__ to convert CoffeeScript to ECMAScript.

Code style
----------

Non-vendored code is checked and formatted using `Prettier <https://prettier.io>`__ (or `Standard <https://github.com/standard/standard>`__).

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


To transform newer code to ECMAScript 6, use `Babel <https://babeljs.io>`__ with the `defaults <https://babeljs.io/docs/en/babel-preset-env#no-targets>`__ query from `browserlist <https://github.com/browserslist/browserslist>`__.

Preferences
-----------

Plain JavaScript is preferred to using jQuery, unless functionality depends on jQuery plugins. To replace jQuery in a project, refer to `You Might Not Need jQuery <http://youmightnotneedjquery.com>`__.

Package manager
  `npm <https://docs.npmjs.com>`__, the default package manager of Node.js. Do not use `yarn <https://yarnpkg.com>`__.
User interface
  `Vue <https://vuejs.org>`__ or `React <https://reactjs.org>`__

.. _javascript-ci:

Continuous integration
----------------------

Create a ``.github/workflows/js.yml`` file. As a base, use:

.. literalinclude:: samples/js.yml
   :language: yaml

Maintainers can find and compare ``js.yml`` files with:

.. code-block:: bash

   find . -name js.yml -exec bash -c 'echo $(tail -r {} | tail +2 | tail -r | shasum - | cut -d" " -f1) {}' \;

Reference
---------

-  `MDN Web Docs <https://developer.mozilla.org/en-US/>`__
-  `Can I use... <https://caniuse.com/>`__
