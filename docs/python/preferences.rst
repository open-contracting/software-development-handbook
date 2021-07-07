Preferred packages
==================

Web framework
  `Django LTS <https://www.djangoproject.com/download/>`__, unless a newer version has desirable features. Do not use `Flask <https://flask.palletsprojects.com/>`__, except in limited circumstances like generating a static site with `Frozen-Flask <https://pythonhosted.org/Frozen-Flask/>`__.
API
  `Django REST Framework <https://www.django-rest-framework.org>`__ or `FastAPI <https://fastapi.tiangolo.com>`__. Do not use `Django Tastypie <http://tastypieapi.org>`__, which has fallen behind on Django and Python versions.
Command-line interface
  `Click <https://click.palletsprojects.com/>`__, unless a framework provides its own, like `Django <https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/>`__ or `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#custom-project-commands>`__. Do not use `argparse <https://docs.python.org/3/library/argparse.html>`__.
Object Relational Mapper (ORM)
  Django. If you don't need an ORM, use `psycopg2 <https://www.psycopg.org/docs/>`__. Do not use `SQLAlchemy <https://www.sqlalchemy.org/>`__, except in low-level libraries with limited scope *where an ORM is needed*.
HTTP client
  `Requests <https://docs.python-requests.org/en/master/>`__, unless a framework uses another, like Scrapy (Twisted).
HTML parsing
  `lxml <https://pypi.org/project/lxml/>`__. Do not use `BeautifulSoup <https://pypi.org/project/BeautifulSoup/>`__.
Markdown parsing
  `markdown-it-py <https://pypi.org/project/markdown-it-py/>`__. Do not use `commonmark <https://pypi.org/project/commonmark/>`__, which is slower and less well maintained.
Templating
  `Jinja <https://jinja.palletsprojects.com/>`__
Translation
  `gettext <https://docs.python.org/3/library/gettext.html>`__, `Babel <http://babel.pocoo.org/en/latest/>`__ and `transifex-client <https://pypi.org/project/transifex-client/>`__, unless a framework provides an interface to these, like `Django <https://docs.djangoproject.com/en/3.2/topics/i18n/>`__ or `Sphinx <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`__.
Logging
  `logging <https://docs.python.org/3/library/logging.html>`__
Testing
  `pytest <https://docs.pytest.org/>`__, unless a framework uses another, like `Django <https://docs.djangoproject.com/en/3.2/topics/testing/>`__ (unittest).
Coverage
  `Coveralls <https://coveralls-python.readthedocs.io/en/latest/>`__
Documentation
  `Sphinx <https://www.sphinx-doc.org/en/master/>`__. Its Markdown extensions should only be used for OCDS documentation.

Rationale
---------

We have preferences in order to:

-  Limit the number of packages with which developers need to be familiar.
-  Re-use code (like Click) instead of writing new code (with argparse).

For :doc:`applications`, we prefer all-inclusive and opinionated packages, because they:

-  Promote greater similarity and code reuse across projects. Django encourages developers to use its authentication mechanism. With Flask, each developer can choose a different mechanism.
-  Are more robust to changes in scope. For example, you might not need the `Django admin site <https://docs.djangoproject.com/en/3.2/ref/contrib/admin/>`__ on day one, but you'll be happy to have it when it becomes a requirement.

Criteria
--------

A preferred package should meet the following criteria:

-  It is properly released: its readme is rendered on PyPI, a changelog is maintained, tags are used, etc.
-  It supports the most recent version of Python and frameworks (if relevant), like Django or Sphinx. Counter-example: `django-tastypie <https://github.com/django-tastypie/django-tastypie/pull/1623>`__ (since resolved).

   -  Simple libraries might not need new releases for new Python versions.

-  It meets the [QASP criteria](https://docs.google.com/document/d/1s-PJSdX43_DMAcXYalG9Upm31XvWCp31j_QGCzFJ7qY/edit) of published, tested and documented.

   -  *Published*: Find its repository and check its open source license.
   -  *Tested*: Check its CI badges, GitHub Actions tab, or CI configuration.
   -  *Documented*: Check its documentation website.

-  Its issue tracker demonstrates that the maintainers are responsive. Counter-example: `django-environ <https://github.com/joke2k/django-environ/pull/291>`__ (`issue <https://github.com/OpenDataServices/lib-cove-web/issues/80>`__).

   -  The repository is not described as archived or unmaintained.
   -  The maintainer's other repositories can be considered if the repository is new or unpopular.

Enforcement
-----------

Maintainers can find dependencies with:

.. code-block:: shell

   find . \( -name 'setup.py' -or -name 'requirements.in' \) -exec echo {} \; -exec cat {} \; 
