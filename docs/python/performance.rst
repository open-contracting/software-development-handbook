Performance
===========

This page presently only has reusable snippets.

CPU profiling
-------------

For example:

.. code-block:: shell

   cat packages.json | python -m cProfile -o code.prof ocdskit/cli/__main__.py compile > /dev/null
   gprof2dot -f pstats code.prof | dot -Tpng -o output.png
   open output.png

To see where a running program is spending its time, use `py-spy top <https://github.com/benfred/py-spy>`__.

Memory profiling
----------------

For example:

.. code-block:: shell

   pip install memory_profiler matplotlib
   time mprof run libcoveoc4ids data.json
   mprof plot
