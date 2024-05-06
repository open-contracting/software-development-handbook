Performance
===========

.. note::

   This page is a stub. This page presently only has reusable snippets.

.. seealso::

   :ref:`Django performance<django-performance>`

Software performance depends on many choices: language (like :doc:`../rust/index` versus Python), framework (like `FastAPI versus Django <https://www.techempower.com/benchmarks/>`__), architecture (e.g. map-reduce), networking (e.g. batch requests), etc. Many choices are costly to change at a later date (e.g. full rewrite).

Profiling
---------

Use profiling to:

-  Identify slow dependencies, in case faster alternatives can be easily swapped in
-  Find major hotspots, like a loop that runs in exponential time instead of quadratic time
-  Find minor hotspots, if changing language, etc. is too costly

Once a hotspot is found, the solution might be to:

-  Call it once, via refactoring: for example, traversing JSON once for all CoVE calculations, instead of once for each calculation, in `lib-cove <https://github.com/OpenDataServices/lib-cove/issues/65>`__
-  Call it less, via batching: for example, :ref:`reducing the number of SQL queries in Django projects<django-performance>`
-  Cache the results: for example, `caching mergers in Kingfisher Process <https://github.com/open-contracting/kingfisher-process/blob/c4b05204faf08d00ed7914a41c2fd0770e0f6b3e/process/processors/compiler.py#L52>`__
-  Process in parallel: for example, distributing work to multiple threads, like we do with :doc:`../services/rabbitmq`
-  Replace it entirely: for example, using the :ref:`orjson<format-json>` package instead of the ``json`` library

CPU
~~~

For example:

.. code-block:: shell

   cat packages.json | python -m cProfile -o code.prof ocdskit/__main__.py compile > /dev/null
   gprof2dot -f pstats code.prof | dot -Tpng -o output.png
   open output.png

To see where a running program is spending its time, use `py-spy top <https://github.com/benfred/py-spy>`__.

Memory
~~~~~~

For example:

.. code-block:: shell

   pip install memory_profiler matplotlib
   time mprof run libcoveoc4ids data.json
   mprof plot

Reference
---------

-  `High Performance Browser Networking <https://hpbn.co>`__
-  `Memray <https://bloomberg.github.io/memray/>`__ by Bloomberg
-  `Computer, Enhance! course by Casey Muratori <https://www.computerenhance.com>`__
