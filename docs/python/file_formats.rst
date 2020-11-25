File formats
============

We read and write a lot of CSV and JSON files. Their format should be consistent.

JSON
----

Input
~~~~~

In most cases, simply use the `standard library <https://docs.python.org/3/library/json.html>`__.

.. code-block:: python

   with open(path) as f:
       data = json.load(f)

If (and only if) the code must support Python 3.5 or earlier, use:

.. code-block:: python

   from collections import OrderedDict

   with open(path) as f:
       data = json.load(f, object_pairs_hook=OrderedDict)

For critical paths involving small files, use `orjson <https://pypi.org/project/orjson/>`__.

.. note::

   We can switch to the Python bindings for simdjson: either `pysimdjson <https://github.com/TkTech/pysimdjson>`__ or `libpy_simdjson <https://github.com/gerrymanoim/libpy_simdjson>`__. For JSON documents with known structures, `JSON Link <https://github.com/beached/daw_json_link>`__ is fastest, but the files relevant to us have unknown structures.

For large files, use the `same techniques <https://ocdskit.readthedocs.io/en/latest/contributing.html#streaming>`__ as OCDS Kit to stream input using `ijson <https://pypi.org/project/ijson/>`__, stream output using `iterencode <https://docs.python.org/3/library/json.html#json.JSONEncoder.iterencode>`__, and postpone evaluation using iterators. See its `brief tutorial <https://ocdskit.readthedocs.io/en/latest/library.html#working-with-streams>`__ on streaming and re-use its `default method <https://ocdskit.readthedocs.io/en/latest/_modules/ocdskit/util.html>`__.

.. note::

   ijson uses `Yajl <http://lloyd.github.io/yajl/>`__. `simdjson <https://simdjson.org>`__ is faster, but is limited to `files smaller than 4 GB <https://github.com/simdjson/simdjson/issues/128>`__ and has no `streaming API <https://github.com/simdjson/simdjson/issues/670>`__.

Output
~~~~~~

Indent with 2 spaces, use UTF-8 characters, and preserve order of object pairs. Example:

.. code-block:: python

   with open(path, 'w') as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
       f.write('\n')

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

   with open(path, 'w') as f:
       writer = csv.DictWriter(f, fieldnames, lineterminator='\n')
       writer.writeheader()
       writer.writerows(rows)
