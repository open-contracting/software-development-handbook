File formats
============

We read and write a lot of CSV and JSON files. Their format should be consistent.

.. _format-json:

JSON
----

Input
~~~~~

In most cases, simply use the `standard library <https://docs.python.org/3/library/json.html>`__.

.. code-block:: python

   with open(path) as f:
       data = json.load(f)

For critical paths involving *small files*, use `orjson <https://pypi.org/project/orjson/>`__.

.. note::

   We can switch to the `Python bindings for simdjson <https://pypi.org/project/cysimdjson/>`__. Read the *Trade-offs* section.

For *large files*, use the `same techniques <https://ocdskit.readthedocs.io/en/latest/contributing.html#streaming>`__ as OCDS Kit to stream input using `ijson <https://pypi.org/project/ijson/>`__, stream output using `iterencode <https://docs.python.org/3/library/json.html#json.JSONEncoder.iterencode>`__, and postpone evaluation using iterators. See its `brief tutorial <https://ocdskit.readthedocs.io/en/latest/library.html#working-with-streams>`__ on streaming and reuse its `default method <https://ocdskit.readthedocs.io/en/latest/_modules/ocdskit/util.html>`__.

.. note::

   ijson uses `YAJL <https://lloyd.github.io/yajl/>`__. `simdjson <https://simdjson.org>`__ is limited to `files smaller than 4 GB <https://github.com/simdjson/simdjson/issues/128>`__ and has no `streaming API <https://github.com/simdjson/simdjson/issues/670>`__.

Output
~~~~~~

Indent with 2 spaces and use UTF-8 characters. Example:

.. code-block:: python

   with open(path, "w") as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
       f.write("\n")

Or, in a compact format:

.. code-block:: python

   with open(path, "w") as f:
       json.dump(data, f, separators=(",", ":"))

CSV
---

Input
~~~~~

.. code-block:: python

   with open(path) as f:
       reader = csv.DictReader(f)
       fieldnames = reader.fieldnames
       rows = [row for row in reader]

Output
~~~~~~

Use LF (``\n``) as the line terminator. Example:

.. code-block:: python

   with open(path, "w") as f:
       writer = csv.DictWriter(f, fieldnames, lineterminator="\n")
       writer.writeheader()
       writer.writerows(rows)
