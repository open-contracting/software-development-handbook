HTML and CSS
============

HTML
----

Code style
~~~~~~~~~~

Style HTML code using `Prettier <https://prettier.io>`__ with 4-space indentation.

Search engine optimization (SEO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On each page of a public-facing website:

-  Set a unique ``<title>`` tag
-  Set a unique ``<meta name="description" content="">`` tag
-  Set social media meta tags, at minimum:

   .. code-block:: html

      <meta property="og:title" content="">
      <meta property="og:description" content="">
      <meta property="og:type" content="article"> <!-- or "website" for homepage -->
      <meta property="og:image" content="">
      <meta property="og:url" content="">
      <meta name="twitter:card" content="summary">

   .. seealso::

      -  `Open Graph protocol <https://ogp.me>`__
      -  `Twitter Summary Card <https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary>`__
      -  `Facebook Sharing Debugger <https://developers.facebook.com/tools/debug/>`__
      -  `Twitter Card validator <https://cards-dev.twitter.com/validator>`__

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
