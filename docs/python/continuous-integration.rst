Continuous Integration
======================

Repositories should use GitHub actions and the branch protection features in GitHub to ensure Continuous Integration runs for all code.

(As documented in our :doc:`../general/preferences`.)

Standard maintenance scripts
----------------------------

All Repositories should call standard maintenance scripts. These ensure a set of standard tests is carried out including isort, flake8 and tests on data files.

Details on these tests and how to run them locally `are found in the standard maintenance scripts repository <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

pytest
------

`pytest <https://docs.pytest.org/>`__ should be preferred, unless a framework uses another, like `Django <https://docs.djangoproject.com/en/3.0/topics/testing/>`__ (unittest).

(As documented in our :ref:`preferred-packages`.)


I18N strings tests
------------------

For repositories that are applications with multiple locales, we test that all strings have been translated.

We only do this on pull requests; not on every push. This is so a developer can work on a feature and still easily see the results of Continuous Integration runs. But they then need to get strings translated right at the end of their work, as they make a pull request.

You can see `an example of this in Cove <https://github.com/open-contracting/cove-ocds/blob/master/.github/workflows/ci.yml>`__, with commands like:

.. code:: bash

    - run: sudo apt install gettext translate-toolkit
    - run: python manage.py makemessages -l es
    - run: "[ \"$GITHUB_EVENT_NAME\" != \"pull_request\" ] || [ \"`pocount --incomplete cove_ocds/locale/es/LC_MESSAGES/django.po`\" = \"\" ]"

The first clause of the "or" statement will mean that line will always pass for any runs that are not a pull request. For pull requests, the second clause must pass instead.

Coveralls
---------

Code Coverage statistics are reported to Coveralls, but repositories do not block pull requests if these go down.

(As documented in our :ref:`preferred-packages`.)