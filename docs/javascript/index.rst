JavaScript
==========

Version
-------

Frontend code is written for ECMAScript 6 (ES6) (`see the status of feature support in modern browsers <https://kangax.github.io/compat-table/es6/>`__). We don't support `Internet Explorer 11 <https://death-to-ie11.com>`__.

.. note::

   Don't use `CoffeeScript <https://coffeescript.org>`__. Unless the repository is a fork, use `Decaffeinate <https://decaffeinate-project.org>`__ to convert CoffeeScript to ECMAScript.

Code style
----------

Non-vendored code is checked and formatted using `Standard <https://github.com/standard/standard>`__.

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
       "destruct-param",
       "includes"
     ]
   }


To transform newer code to ECMAScript 6, use `Babel <https://babeljs.io>`__ with the `defaults <https://babeljs.io/docs/en/babel-preset-env#no-targets>`__ query from `browserlist <https://github.com/browserslist/browserslist>`__.

Preferences
-----------

Plain JavaScript is preferred to using jQuery, unless functionality depends on jQuery plugins. To replace jQuery in a project, refer to `You Might Not Need jQuery <http://youmightnotneedjquery.com>`__.

User interfaces
  `Vue <https://vuejs.org>`__ or `React <https://reactjs.org>`__
