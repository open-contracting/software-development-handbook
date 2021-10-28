Directory layout
================

Don't mix static files with Python files.

For :ref:`automated-testing`, put `tests outside application code <https://docs.pytest.org/en/latest/explanation/goodpractices.html#choosing-a-test-layout-import-rules>`__.

:doc:`applications` should follow the layout of the framework used, like `Django <https://docs.djangoproject.com/en/3.2/intro/tutorial01/>`__ or `Scrapy <https://docs.scrapy.org/en/latest/topics/commands.html#default-structure-of-scrapy-projects>`__. If no framework is used, prefer a smaller number of directories: Examples: `Kingfisher Summarize <https://github.com/open-contracting/kingfisher-summarize>`__, `Pelican backend <https://github.com/open-contracting/pelican-backend>`__.

:doc:`packages` should follow this layout, where ``PACKAGENAME`` is the name of the package:

.. code-block:: none

   .
   ├── PACKAGENAME
   ├── docs
   └── tests
       └── fixtures

.. note::

   We don't use the `src/ layout <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure>`__. Although a `single blog post <https://blog.ionelmc.ro/2015/02/24/the-problem-with-packaging-in-python/>`__ and a few passionate developers have popularized the idea, in practice, we rarely encounter the problems it solves, and our use of :ref:`check-manifest<python-package-release-process>` and `test_requirements.py <https://github.com/open-contracting/standard-maintenance-scripts/blob/main/tests/test_requirements.py>`__ guard against those problems.
