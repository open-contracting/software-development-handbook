Services
========

PostgreSQL
----------

Database administrators need to identify the sources of queries, in order to notify developers of inefficient queries or alert users whose queries will be interrupted by maintenance. For example:

-  Django appplications set the `application_name <https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME>`__ query string parameter in the PostgreSQL `connection URI <https://www.postgresql.org/docs/11/libpq-connect.html#id-1.7.3.8.3.6>`__
-  Kingfisher Summarize uses the psycopg2 package, and adds ``/* kingfisher-summarize {identifier} */`` as a comment to expensive queries
-  Kingfisher Colab uses the ipython-sql package, and adds the Google Colaboratory notebook URL as a comment to all queries
