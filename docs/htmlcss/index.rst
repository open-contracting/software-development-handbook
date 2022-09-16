HTML and CSS
============

HTML
----

Code style
~~~~~~~~~~

Style HTML code using `Prettier <https://prettier.io>`__ with 4-space indentation.

CSS
---

Frameworks
~~~~~~~~~~

Most projects use `Bootstrap <https://getbootstrap.com>`__, some of which use Python packages like `django-bootstrap5 <https://pypi.org/project/django-bootstrap5/>`__. Designers are free to use other frameworks like:

-  `Tailwind <https://tailwindcss.com>`__, a `utility classes <https://adamwathan.me/css-utility-classes-and-separation-of-concerns/>`__ framework
-  `Vuetify <https://vuetifyjs.com>`__, a `Material Design <https://material.io/design>`__ framework

Reminders
~~~~~~~~~

-  Use a CSS framework's variables and utility classes, instead of creating new classes
-  Avoid using too many font sizes on the same page. To check:

   .. code-block:: javascript

      const sizes = {}
      for (const element of document.getElementsByTagName('*')) {
          const size = window.getComputedStyle(element).fontSize
          if (!(size in sizes)) { sizes[size] = [] }
              sizes[size].push(element)
          }
      sizes

Code style
~~~~~~~~~~

Style CSS code using `Prettier <https://prettier.io>`__ with 2-space indentation. In terms of naming conventions, options include:

-  `Block Element Modifier (BEM) <http://getbem.com>`__

Development
~~~~~~~~~~~

-  `Tachyons X-ray <http://tachyons.io/xray/>`__ to align objects to a grid

Reference
---------

-  `MDN Web Docs <https://developer.mozilla.org/en-US/>`__
-  `Can I use... <https://caniuse.com/>`__
