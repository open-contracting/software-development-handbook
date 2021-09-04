Services
========

PostgreSQL
----------

Database administrators need to identify the sources of queries, in order to notify developers of inefficient queries or alert users whose queries will be interrupted by maintenance. For example:

-  Django appplications set the `application_name <https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME>`__ query string parameter in the PostgreSQL `connection URI <https://www.postgresql.org/docs/11/libpq-connect.html#id-1.7.3.8.3.6>`__
-  Kingfisher Summarize uses the psycopg2 package, and adds ``/* kingfisher-summarize {identifier} */`` as a comment to expensive queries
-  Kingfisher Colab uses the ipython-sql package, and adds the Google Colaboratory notebook URL as a comment to all queries

RabbitMQ
--------

Heartbeat
~~~~~~~~~

If a consumer takes too long to process a message, the heartbeat might timeout, causing the connection to RabbitMQ to drop (see pika `readme <https://github.com/pika/pika/#requesting-message-acknowledgements-from-another-thread>`__ and `example <https://pika.readthedocs.io/en/latest/examples/heartbeat_and_blocked_timeouts.html>`__).

Disabling the heartbeat is `discouraged <https://stackoverflow.com/a/51755383/244258>`__ by RabbitMQ developers. The solution is to process the message in a separate thread (`see example <https://github.com/pika/pika/blob/master/examples/basic_consumer_threaded.py>`__).

That said, from Datlab's experience, the RabbitMQ connection can be unreliable, regardless of the connection settings. In any case, for the Data Registry, all consumers are asynchronous and use two threads: one to manage the connection, another to process the message.

Acknowledgements
~~~~~~~~~~~~~~~~

In some cases, messages are acknowledged when a point-of-no-return is reached, before the messages are processed. For example, when importing data from Kingfisher into Pelican, messages for the next phase are already published for the yet-unfinished job; it is not simple to go back if processing fails.

.. https://github.com/open-contracting/data-registry/issues/140
