Testing
=======

You should write tests as you write code – not as an afterthought once the project is complete.

.. seealso::

   :ref:`File naming and directory layout<layout-tests>` for tests

Write tests
-----------

Test code tends to be written once and only read when the test fails. As a result, test code tends to be poorly written, with a lot of copy-pasting between test methods, which makes intent unclear.

To write clear tests:

-  Test one scenario per test.
-  Name tests, fixtures, and mocks descriptively. Do not suffix them ``1``, ``2``, ``3``, etc.
-  Use `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__ to test something with different inputs (like in `OCDS Kit <https://github.com/open-contracting/ocdskit/blob/main/tests/test_util.py>`__).
-  Use `pytest.fixture <https://docs.pytest.org/en/stable/fixture.html>`__ to re-use test scaffolding (like in `OCDS Merge <https://github.com/open-contracting/ocds-merge/blob/main/tests/conftest.py>`__ or `Kingfisher Colab <https://github.com/open-contracting/kingfisher-colab/blob/main/tests/conftest.py>`__).
-  Use `unittest.TestCase <https://docs.python.org/3/library/unittest.html#unittest.TestCase>`__ to re-use testing logic, including:

   -  Test methods (like `ViewTests <https://github.com/open-contracting/toucan/blob/main/tests/__init__.py>`__ in Toucan)
   -  Test scaffolding, using `setUp() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp>`__ and `tearDown() <https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown>`__

-  Use `subTest() <https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests>`__ from ``unittest`` (with `pytest-subtests <https://pypi.org/project/pytest-subtests/>`__ if using ``pytest``) to reduce duplication (like in `Pelican backend <https://github.com/open-contracting/pelican-backend/blob/main/tests/__init__.py>`__).

.. note::

   There are `important caveats <https://docs.pytest.org/en/stable/unittest.html>`__ to using ``pytest`` with ``unittest``.

.. _automated-testing:

Run tests
---------

For Django applications:

.. code-block:: shell

   python manage.py test

Otherwise, pytest is :doc:`preferred<preferences>`. For applications:

.. code-block:: shell

   pip-sync requirements_dev.txt
   pytest

For :doc:`packages<packages>`:

.. code-block:: shell

   pip install .[test]
   pytest
