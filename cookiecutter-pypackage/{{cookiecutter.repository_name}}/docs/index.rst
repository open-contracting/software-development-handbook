{{ cookiecutter.human_name }} |release|
{{ '=' * cookiecutter.human_name|length() }}==========

.. include:: ../README.rst

.. toctree::
   :caption: Contents

   api/index
   contributing/index
   changelog

Copyright (c) {% now 'utc', '%Y' %} Open Contracting Partnership, released under the BSD license
