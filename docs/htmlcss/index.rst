HTML and CSS
============

HTML
----

Code style
~~~~~~~~~~

Check and style HTML using :ref:`Biome <biome>`.

Subresource integrity (SRI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using unbundled external packages:

-  Reference a package's specific version on a content delivery network (CDN), like `unpkg <https://unpkg.com>`__, `jsDelivr <https://www.jsdelivr.com>`__, `cdnjs <https://cdnjs.com>`__ or the package's own CDN (like `Redocly <https://github.com/Redocly/redoc#add-an-html-element-to-the-page>`__)
-  Use the `SRI Hash Generator <https://www.srihash.org>`__, as `recommended <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity#tools_for_generating_sri_hashes>`__ by MDN, with the default SHA-384 algorithm

Some scripts cannot use subresource integrity:

-  ``https://cdn.usefathom.com/script.js``
-  ``https://fonts.googleapis.com/css?...`` (`reason <https://github.com/google/fonts/issues/473#issuecomment-331329601>`__ and `alternative <https://github.com/google/fonts/issues/473#issuecomment-2102946515>`__)
-  ``https://use.typekit.net/xxxxxxx.js``
-  ``https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX``

Reference: `Subresource Integrity <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`__ on MDN

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

.. seealso::

   -  `Faceted Navigation: Definition, Examples & SEO Best Practices <https://ahrefs.com/blog/faceted-navigation/>`__

.. _css:

CSS
---

.. seealso:: :ref:`esbuild` for compiling SCSS (Sass)

Frameworks
~~~~~~~~~~

Most projects use `Bootstrap <https://getbootstrap.com>`__. Designers are free to use other frameworks like:

-  `Tailwind <https://tailwindcss.com>`__, a `utility classes <https://adamwathan.me/css-utility-classes-and-separation-of-concerns/>`__ framework
-  `Vuetify <https://vuetifyjs.com>`__, a `Material Design <https://m3.material.io>`__ framework

When using Bootstrap, `customize <https://getbootstrap.com/docs/5.2/customize/sass/>`__ it and `@import only the components you need <https://getbootstrap.com/docs/5.2/customize/optimize/>`__.

.. seealso::

   The Data Registry's `_custom.scss file <https://github.com/open-contracting/data-registry/blob/main/src/scss/_custom.scss>`__, for customizing Bootstrap.

Reminders
~~~~~~~~~

-  Use a CSS framework's variables and utility classes, instead of creating new classes
-  Conform to WCAG 2.1 at Level AA for `contrast <https://color.adobe.com/create/color-contrast-analyzer>`__
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

Check and style CSS using :ref:`Biome <biome>`, with 2-space indentation.

In terms of naming conventions, consider `Block Element Modifier (BEM) <https://getbem.com>`__.

Development
~~~~~~~~~~~

-  `Tachyons X-ray <https://tachyons.io/xray/>`__ to align objects to a grid

Reference
---------

-  `MDN Web Docs <https://developer.mozilla.org/en-US/>`__
-  `Can I use... <https://caniuse.com/>`__
