Performance
===========

Profiling
---------

For example:

.. code:: bash

   cat packages.json | python -m cProfile -o code.prof ocdskit/cli/__main__.py compile > /dev/null
   gprof2dot -f pstats code.prof | dot -Tpng -o output.png
   open output.png
