Preferred packages
==================

We have preferences for :doc:`requirements<requirements>` in order to:

-  Limit the number of packages with which developers need to be familiar.
-  Reuse code (like Click) instead of writing new code (with argparse).

For applications, we prefer all-inclusive and opinionated packages, because they:

-  Promote greater similarity and code reuse across projects. Django encourages developers to use its authentication mechanism. With Flask, each developer can choose a different mechanism.
-  Are more robust to changes in scope. For example, you might not need the `Django admin site <https://docs.djangoproject.com/en/4.2/ref/contrib/admin/>`__ on day one, but you'll be happy to have it when it becomes a requirement.

Maintainers can find dependencies with:

.. code-block:: bash

   find . \( -name 'setup.cfg' -or -name 'requirements.in' \) -exec echo {} \; -exec cat {} \;

Preferences
-----------

Web framework
  `Django LTS <https://www.djangoproject.com/download/>`__, unless a newer version has desirable features. Do not use `Flask <https://flask.palletsprojects.com/>`__, except in limited circumstances like generating a static site with `Frozen-Flask <https://pythonhosted.org/Frozen-Flask/>`__.
API
  `Django REST Framework <https://www.django-rest-framework.org>`__ or `FastAPI <https://fastapi.tiangolo.com>`__. Do not use `Django Tastypie <https://django-tastypie.readthedocs.io/en/latest/>`__, which has fallen behind on Django and Python versions.
Command-line interface
  `Click <https://click.palletsprojects.com/>`__, unless a framework provides its own, like `Django <https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/>`__ or `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#custom-project-commands>`__. Do not use `argparse <https://docs.python.org/3/library/argparse.html>`__.
Object Relational Mapper (ORM)
  Django. If you don't need an ORM, use `psycopg2 <https://www.psycopg.org/docs/>`__. Do not use `SQLAlchemy <https://www.sqlalchemy.org/>`__, except with FastAPI or in low-level libraries with limited scope *where an ORM is needed*.

  .. note::

     Use ``psycopg2`` in production, not ``psycopg2-binary``, `as recommended <https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary>`__. :ref:`See instructions<requirements-psycopg2>`.

HTTP client
  `Requests <https://docs.python-requests.org/en/latest/>`__, unless a framework uses another, like Scrapy (Twisted).
HTML parsing
  `lxml <https://pypi.org/project/lxml/>`__. Do not use `BeautifulSoup <https://pypi.org/project/BeautifulSoup/>`__.
Markdown parsing
  `markdown-it-py <https://pypi.org/project/markdown-it-py/>`__. Do not use `commonmark <https://pypi.org/project/commonmark/>`__, which is deprecated.
Templating
  `Jinja <https://jinja.palletsprojects.com/>`__. Do not use CSS framework integration packages like ``django-bootstrap*``, as they tend to lag the most recent releases. See :doc:`../htmlcss/index`.
Asset management
  Do not use `django-compressor <https://django-compressor.readthedocs.io/en/stable/>`__ or `django-pipeline <https://django-pipeline.readthedocs.io/en/latest/>`__, which are always behind NPM packages. See :ref:`javascript-preferences` for JavaScript.
Translation
  `gettext <https://docs.python.org/3/library/gettext.html>`__ and `Babel <https://babel.pocoo.org/en/latest/>`__, unless a framework provides an interface to these, like `Django <https://docs.djangoproject.com/en/4.2/topics/i18n/>`__ or `Sphinx <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`__.
Logging
  `logging <https://docs.python.org/3/library/logging.html>`__
Testing
  `pytest <https://docs.pytest.org/>`__, unless a framework uses another, like `Django <https://docs.djangoproject.com/en/4.2/topics/testing/>`__ (unittest).
Coverage
  `Coveralls <https://coveralls-python.readthedocs.io/en/latest/>`__
Documentation
  `Sphinx <https://www.sphinx-doc.org/en/master/>`__. Its Markdown extensions should only be used for OCDS documentation.

.. tip::

   `Jazzband <https://jazzband.co/projects?sorter=stargazers&order=desc>`__ packages are a good choice.

Criteria
--------

A preferred package should meet the following criteria:

-  It is properly released: its readme is rendered on PyPI, a changelog is maintained, tags are used, etc.
-  It supports the most recent version of Python and frameworks (if relevant), like Django or Sphinx. Counter-example: `django-tastypie <https://github.com/django-tastypie/django-tastypie/pull/1623>`__ (since resolved).

   -  Simple libraries might not need new releases for new Python versions.

-  It meets the `QASP criteria <https://docs.google.com/document/d/1s-PJSdX43_DMAcXYalG9Upm31XvWCp31j_QGCzFJ7qY/edit>`__ of published, tested and documented.

   -  *Published*: Find its repository and check its open source license.
   -  *Tested*: Check its CI badges, GitHub Actions tab, or CI configuration.
   -  *Documented*: Check its documentation website.

-  Its issue tracker demonstrates that the maintainers are responsive. Counter-example: `django-environ <https://github.com/joke2k/django-environ/pull/291>`__ (since resolved).

   -  The repository is not described as archived or unmaintained.
   -  The maintainer's other repositories can be considered if the repository is new or unpopular.

`Snyk Open Source Advisor <https://snyk.io/advisor/>`__ might also be used to answer the above.

License compliance
------------------

To ease license compliance and code reuse, avoid software distributed under `strong copyleft <https://en.wikipedia.org/wiki/Copyleft>`__ licenses.

-  Use an alternative dependency.

   -  `rfc3339-validator <https://pypi.org/project/rfc3339-validator/>`__, not `strict-rfc3339 <https://pypi.org/project/strict-rfc3339/>`__
   -  `rfc3986-validator <https://pypi.org/project/rfc3986-validator/>`__, not `rfc3987 <https://pypi.org/project/rfc3987/>`__
   -  `text-unidecode <https://pypi.org/project/text-unidecode/>`__, not `unidecode <https://pypi.org/project/Unidecode/>`__

-  Make the dependency optional.

   .. code-block:: python

      try:
          import some_gpl_package

          using_some_gpl_package = True
      except ImportError:
          using_some_gpl_package = False

      if using_some_gpl_package:
          print("Some optional behavior")

.. note::

   This does not apply to software that is only used as a utility and is not linked to the code, like `libsass <https://pypi.org/project/libsass/>`__.

To list the licenses under which installed packages are distributed:

-  Install the packages

-  Install `pip-licenses <https://pypi.org/project/pip-licenses/>`__:

   .. code-block:: bash

      pip install pip-licenses

-  List the licenses:

   .. code-block:: bash

      pip-licenses --with-urls

If you have virtual environments for multiple repositories, you can do a bulk operation:

-  Install `pip-licenses <https://pypi.org/project/pip-licenses/>`__ in all virtual environments. For example, if using `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`__ (fish shell):

   .. code-block:: fish

      for env in (pyenv virtualenvs --skip-aliases --bare)
          pyenv activate $env
          pip install pip-licenses
      end

-  Initialize a CSV file as the output file:

   .. code-block:: bash

      echo Venv,Name,Version,License,URL > licenses.csv

-  Append licenses to the output file:

   .. code-block:: fish

      for env in (pyenv virtualenvs --skip-aliases --bare)
          pyenv activate $env
          pip-licenses --format=csv --with-urls | tail -n +2 | sed "s`^`$env,`" >> licenses.csv
      end

-  Run this script from the `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts>`__ repository:

   .. code-block:: bash

      ./manage.py check-licenses licenses.csv
