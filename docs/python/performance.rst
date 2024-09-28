Performance
===========

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
   -  `Austin <https://pypi.org/project/austin-dist/>`__ for CPU and memory statistical profiling, including running processes
   -  `psrecord <https://pypi.org/project/psrecord/>`__ to chart CPU and memory usage, including running processes
   -  `psutil <https://pypi.org/project/psutil/>`__

CPU
~~~

-  `cProfile <https://docs.python.org/3/library/profile.html>`__ is a deterministic profiler, measures functions, and lacks support for threads. For example:

   .. code-block:: shell

      cat packages.json | python -m cProfile -o code.prof ocdskit/__main__.py compile > /dev/null
      gprof2dot -f pstats code.prof | dot -Tpng -o output.png
      open output.png

-  `py-spy <https://pypi.org/project/py-spy/>`__ is a statistical profiler, measures lines, and supports threads, subprocesses and native extensions. The ``top`` command can attach to a running process.
-  `pprofile <https://pypi.org/project/pprofile/>`__ is a statistical profiler (and `very slow deterministic profiler <https://github.com/vpelletier/pprofile/blob/2.2.0/README.rst#L55-L59>`__), measures lines, and supports threads and PyPy.
-  `vmprof <https://github.com/vmprof/vmprof-python>`__ is a statistic profiler, measures functions or lines, and supports threads and PyPy (and is aware of JIT).
-  `timeit <https://docs.python.org/3/library/timeit.html>`__ is a deterministic profiler for code snippets.

.. admonitions:: Other profilers

   -  `yappi <https://pypi.org/project/yappi/>`__ is a deterministic profiler, measures functions, supports threads and async, and has wall and CPU clocks.
   -  `pyinstrument <https://pypi.org/project/pyinstrument/>`__ is a `statistical profiler <https://pyinstrument.readthedocs.io/en/latest/how-it-works.html#statistical-profiling-not-tracing>`__, measures functions, and `supports async <https://pyinstrument.readthedocs.io/en/latest/how-it-works.html#async-profiling>`__ but `not threads <https://github.com/joerick/pyinstrument/issues/71>`__.
   -  `line-profiler <https://pypi.org/project/line-profiler/>`__ is a deterministic profiler, measures lines, requires decorators, and lacks support for threads.

Memory
~~~~~~

.. tip::

   When profiling a Django project, ensure ``DEBUG = False``: for example, by running ``env DJANGO_ENV=production``.

Memory profilers have two use cases: reduce memory consumption (like in data processing) and fix memory leaks (like in long-running processes). Tools for reducing memory consumption typically measure peaks and draw flamegraphs; that said, they also can be used for memory leaks, by `generating work that leaks memory <https://pythonspeed.com/articles/python-server-memory-leaks/>`__.

When evaluating memory usage in production, remember the differences between `heap memory and resident memory <https://bloomberg.github.io/memray/memory.html>`__. In particular, `resident memory is not freed immediately <https://bloomberg.github.io/memray/memory.html#memory-is-not-freed-immediately>`__.

-  `tracemalloc — Trace memory allocations <https://docs.python.org/3/library/tracemalloc.html>`__
-  `memray <https://bloomberg.github.io/memray/>`__ to diagnose peak memory, using `attach <https://bloomberg.github.io/memray/attach.html>`__ for a running process, including `live reporting <https://bloomberg.github.io/memray/live.html>`__
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

Optimizations
-------------

-  Set `__slots__ <https://docs.python.org/3/reference/datamodel.html#slots>`__ on classes or `slots=True <https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass>`__ on dataclasses that are instantiated frequently.

      "The space saved over using __dict__ can be significant. Attribute lookup speed can be significantly improved as well."

   .. Can search for class in:
      *.py,-commands/*,-migrations/*,-tests/*,-base_spiders/*,-spiders/*,-exceptions.py,-manage.py,-admin.py,-apps.py,-forms.py,-models.py,-routers.py,-views.py

Reference
---------

-  `High Performance Browser Networking <https://hpbn.co>`__
-  `Computer, Enhance! course by Casey Muratori <https://www.computerenhance.com>`__
