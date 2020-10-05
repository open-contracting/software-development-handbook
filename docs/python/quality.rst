Quality Assurance
=================

Automated testing
-----------------

pytest is preferred, as documented at :ref:`preferred-packages`.

**How To:** Run tests in :ref:`packages<packages-testing>`.

Continuous testing
------------------

GitHub Actions is preferred, as documented at :doc:`../general/preferences`.

**Setup:** Most repositories use a ``.github/workflows/ci.yml`` workflow to run automated tests.

Code style
~~~~~~~~~~

See :ref:`style-guide`.

**Setup:** Most repositories use a ``.github/workflows/lint.yml`` workflow to run style checks, as documented in `standard-maintenance-scripts <https://github.com/open-contracting/standard-maintenance-scripts#tests>`__.

Code coverage
~~~~~~~~~~~~~

Coveralls is preferred, as documented at :ref:`preferred-packages`.

**Setup:** On Coveralls, add the repository, access its settings page, and copy the repo token. On GitHub, add a secret, and set its name to ``COVERALLS_REPO_TOKEN`` and its value to the copied token. Then, append the following to ``.github/workflows/ci.yml``, commit and push:

.. code:: yaml

       - env:
           COVERALLS_REPO_TOKEN: ${{ secrets.COVERALLS_REPO_TOKEN }}
         run: coveralls

i18n coverage
~~~~~~~~~~~~~

Repositories that support multiple locales should test that translations are complete.

This test is run on `pull request <https://docs.github.com/en/free-pro-team@latest/actions/reference/events-that-trigger-workflows#pull_request>`__ events, not `push <https://docs.github.com/en/free-pro-team@latest/actions/reference/events-that-trigger-workflows#push>`__ events, to allow developers to see test results on feature branches, before creating a pull request.

For example, `cove-ocds <https://github.com/open-contracting/cove-ocds/blob/master/.github/workflows/ci.yml>`__ runs:

.. code:: yaml

   - run: sudo apt install gettext translate-toolkit
   - run: python manage.py makemessages -l es
   - run: "[ \"$GITHUB_EVENT_NAME\" != \"pull_request\" ] || [ \"`pocount --incomplete cove_ocds/locale/es/LC_MESSAGES/django.po`\" = \"\" ]"

In other words, either the event isn't a pull request, or the ``pocount`` command's output is empty.

Branch protection
~~~~~~~~~~~~~~~~~

See :ref:`branch-protection`.

**Setup:** A Rake task is used to protect default branches and to require automated tests and style checks to pass before merging on GitHub, as documented at :ref:`branch-protection`.
