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

.. seealso::

   -  `Scalene <https://pypi.org/project/scalene/>`__ for CPU, GPU and memory statistical profiling
   -  `Austin <https://github.com/P403n1x87/austin>`__ for CPU and memory statistical profiling
   -  `psrecord <https://pypi.org/project/psrecord/>`__ to chart CPU and memory usage, in a running program
   -  `psutil <https://pypi.org/project/psutil/>`__

CPU
~~~

-  `The Python Profilers <https://docs.python.org/3/library/profile.html>`__ for deterministing profiling, for example:

   .. code-block:: shell

      cat packages.json | python -m cProfile -o code.prof ocdskit/__main__.py compile > /dev/null
      gprof2dot -f pstats code.prof | dot -Tpng -o output.png
      open output.png

-  `yappi <https://pypi.org/project/yappi/>`__ for deterministing profiling of multiple threads or asynchronous code
-  `py-spy <https://github.com/benfred/py-spy>`__'s ``top`` to measure lines, instead of functions, in a running program
-  `line-profiler <https://pypi.org/project/line-profiler/>`__ to measure lines, instead of functions
-  `timeit <https://docs.python.org/3/library/timeit.html>`__ to measure a code snippet
-  `pyinstrument <https://pypi.org/project/pyinstrument/>`__ for `statistical profiling <https://pyinstrument.readthedocs.io/en/latest/how-it-works.html>`__

.. pprofile not updated since 2021. https://pypi.org/project/pprofile/

Memory
~~~~~~

.. tip::

   When profiling a Django project, ensure ``DEBUG = False``: for example, by running ``env DJANGO_ENV=production``.

There are broadly two use cases: reduce memory consumption (like in data processing) and fix memory leaks (like in long-running processes). Tools for reducing memory consumption typically measure peaks and draw flamegraphs; that said, they also can be used for memory leaks, by `generating work that leaks memory <https://pythonspeed.com/articles/python-server-memory-leaks/>`__.

-  `tracemalloc — Trace memory allocations <https://docs.python.org/3/library/tracemalloc.html>`__
-  `memray <https://bloomberg.github.io/memray/>`__
-  `filprofiler <https://pypi.org/project/filprofiler/>`__ to diagnose peak memory

..

   `memory-profiler <https://pypi.org/project/memory-profiler/>`__ is unmaintained. Use psrecord instead, unless profiling individual functions.

   These are maintained, but not developed:

   -  `pympler <https://pypi.org/project/Pympler/>`__'s `muppy <https://pympler.readthedocs.io/en/latest/muppy.html#muppy>`__ provides information like gc, tracemalloc and weakref
   -  `guppy3 <https://pypi.org/project/guppy3/>`__ provides information like gc, tracemalloc and weakref, but has limited documentation
   -  `objgraph <https://pypi.org/project/objgraph/>`__, to plot memory references, in order to find memory leaks

.. seealso::

   -  `gc — Garbage Collector interface <https://docs.python.org/3/library/gc.html>`__
   -  `weakref — Weak references <https://docs.python.org/3/library/weakref.html>`__

Reference
---------

-  `High Performance Browser Networking <https://hpbn.co>`__
-  `Computer, Enhance! course by Casey Muratori <https://www.computerenhance.com>`__
