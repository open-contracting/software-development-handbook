RabbitMQ
========

The shortest explanation of RabbitMQ is the `AMQP 0-9-1 Model in Brief <https://www.rabbitmq.com/tutorials/amqp-concepts#amqp-model>`__:

-  Multiple *publishers* can publish messages to *exchanges*
-  An *exchange* routes the messages it receives to one or more *queues*, using rules called *bindings*
-  Multiple *consumers* can subscribe to one or more *queues*

It is recommended to be familiar with all `RabbitMQ tutorials <https://www.rabbitmq.com/tutorials>`__.

.. seealso::

   -  `AMQP 0-9-1 Model Explained <https://www.rabbitmq.com/tutorials/amqp-concepts>`__
   -  `Reliability Guide <https://www.rabbitmq.com/docs/reliability>`__
   -  `Full documentation <https://www.rabbitmq.com/docs>`__

Development
-----------

#. Install RabbitMQ. On macOS:

   .. code-block:: shell

      brew install rabbitmq

#. Enable the `management plugin <https://www.rabbitmq.com/docs/management>`__:

   .. code-block:: shell

      rabbitmq-plugins enable rabbitmq_management

#. Access the management plugin at http://127.0.0.1:15672 (user: ``guest``, password: ``guest``)

In Python, use and contribute to `yapw <https://yapw.readthedocs.io/en/latest/>`__, our wrapper around `Pika <https://pika.readthedocs.io/en/stable/>`__, to interact with RabbitMQ, because implementing threads, error handling, signal handling, etc. in every project is repetitive and non-trivial. That said, if you need to use Pika directly, see the examples `in its documentation <https://pika.readthedocs.io/en/stable/examples.html>`__ and `on GitHub <https://github.com/pika/pika/tree/main/examples>`__. Don't use Celery, because its abstractions are inefficient, requiring `complex workarounds <https://blog.untrod.com/2015/03/how-celery-chord-synchronization-works.html>`__.

Environment variables
---------------------

Connect to the broker using a connection string stored in the ``RABBIT_URL`` environment variable.

Store the exchange name in the ``RABBIT_EXCHANGE_NAME`` environment variable - following the format ``{project}_{environment}`` or ``{project}_{service}_{environment}`` – and prefix routing keys by the exchange name. This makes it easy to create distinct exchanges for local development and test environments.

Design decisions
----------------

Bindings
~~~~~~~~

*Consumers declare and bind queues, not publishers*. To reduce coupling, a publisher does not control how its messages are routed: it simply sets the routing key. Each consumer then declares its own queue to read from, and it sets the routing keys that the queue binds to. As such, any number of consumers can read a publisher's messages; if no consumer reads the messages, they are undelivered, by design. This pattern makes it easier to re-order, add or remove consumers.

.. _rabbitmq-heartbeat:

Heartbeat
~~~~~~~~~

If a consumer processes a message in the same thread as the `heartbeat <https://www.rabbitmq.com/docs/heartbeats>`__, the heartbeat can timeout if the processing is slow, causing the connection to RabbitMQ to drop (for Python, see Pika's `readme <https://github.com/pika/pika/#requesting-message-acknowledgements-from-another-thread>`__).

The solution is to process the message in a separate thread (`see Python example <https://github.com/pika/pika/blob/main/examples/basic_consumer_threaded.py>`__), like when using `yapw <https://yapw.readthedocs.io/en/latest/>`__. Disabling heartbeats is `highly discouraged <https://www.rabbitmq.com/docs/heartbeats>`__.

.. https://github.com/open-contracting/data-registry/issues/140

.. seealso::

   :ref:`Acknowledgement timeouts<rabbitmq-acknowledgment>`, if processing is slow before acknowledgement.

Consumer prefetch
~~~~~~~~~~~~~~~~~

In an early production environment, `prefetch count <https://www.rabbitmq.com/docs/confirms#channel-qos-prefetch>`__ is set to 1, which is the `most conservative <https://www.rabbitmq.com/docs/confirms#channel-qos-prefetch-throughput>`__ option. In a mature production environment, it is set to 20, in order to scale first by using more threads before using more processes, based on this `blog post <https://www.rabbitmq.com/blog/2012/04/25/rabbitmq-performance-measurements-part-2>`__.

Idempotence
~~~~~~~~~~~

Messages can be redelivered, and consumers must handle message redelivery gracefully. It is `recommended <https://www.rabbitmq.com/docs/reliability#consumer-side>`__ to design consumers to be idempotent, rather than to explicitly perform deduplication.

To limit cascading redelivery – that is, where a consumer publishes messages but fails before acknowledging the received message, then receives the redelivered message and publishes messages, again – publish messages immediately before acknowledging the received message: that is, after any potential failure.

To be idempotent, make state changes as late as possible: for example, write to the database immediately before publishing any messages and acknowledging the message. The worker should be as **stateless** as possible. It should not make changes to its internal state that carry over between received messages, since messages can arrive in any order.

The simplest form of deduplication is to delete previously written rows before writing new rows to the database.

Messages about the same row can also be processed *concurrently*, in case of multiple workers or a prefetch count above 1. To be idempotent, use `optimistic locking <https://en.wikipedia.org/wiki/Optimistic_concurrency_control>`__: ``UPDATE`` the row conditional on its current value, and do the work only if the ``UPDATE`` matched a row. Otherwise, ack the message.

Database commits
~~~~~~~~~~~~~~~~

If the consumer callback performs database operations, then all database operations before each message publication should be performed in a transaction. This ensures that, if the database operations fail and the incoming message is not acknowledged, then they have a chance to succeed when that message is redelivered, since no partial work had been committed. This guidance applies to *each* message publication, so that work is committed before the related message is published for further processing.

The message publication should not be within the transaction block, if using a ``with`` statement with `psycopg <https://www.psycopg.org/psycopg3/docs/basic/transactions.html#transaction-contexts>`__ or `Django <https://docs.djangoproject.com/en/stable/topics/db/transactions/#django.db.transaction.atomic>`__. This ensures that the commit completes (e.g. without integrity errors), before a message is published for further processing.

.. _rabbitmq-acknowledgment:

Acknowledgements
~~~~~~~~~~~~~~~~

Usually, a message is ack'd once processing is complete. In some cases, a message is ack'd *before* its processing is complete:

-  *When processing is long*: If a message is not ack'd on a channel within the `acknowledgement timeout <https://www.rabbitmq.com/docs/consumers#acknowledgement-timeout>`__ (30 minutes by default), the broker closes the channel and requeues its deliveries. This might cause unexpected errors the next time the consumer uses the channel.
-  *When processing isn't atomic*: After some initial work, a consumer might perform work and publish messages in chunks, like when implementing the `Splitter pattern <https://www.enterpriseintegrationpatterns.com/patterns/messaging/Sequencer.html>`__. If it encounters an error in one chunk, the consumer cannot easily "retry" the original message, without encountering integrity errors and publishing duplicate messages. As such, the message is ack'd after the initial work ("point-of-no-return").

.. note::

   As of RabbitMQ 4.3, only `quorum queues <https://www.rabbitmq.com/docs/quorum-queues>`__ evaluate the acknowledgement timeout. On a `classic queue <https://www.rabbitmq.com/docs/classic-queues>`__, a slow/stuck consumer is never interrupted, the node-wide ``consumer_timeout`` setting is ignored, and the ``x-consumer-timeout`` queue argument is rejected. Manually stopping the consumer requeues its unacknowledged messages.

If a consumer is interrupted or fails before a message is ack'd, the broker `automatically requeues <https://www.rabbitmq.com/docs/confirms#automatic-requeueing>`__ the message, once either the acknowledgement timeout or the :ref:`heartbeat timeout<rabbitmq-heartbeat>` is reached, at which time the consumer is considered buggy, stuck or unavailable by the broker.

When an exception is raised:

-  If the error is expected to occur (e.g. an integrity error due to a duplicate message), or if there's no consequence to ignoring the message (avoid causing a silent failure), the consumer should catch the error, write to a log, and ack the message.
-  If the error isn't expected to occur and the message is unprocessable, the consumer should catch the error, write to a log, and `nack <https://www.rabbitmq.com/docs/nack>`__ the message.

   .. note::

      In Python, Pika's `basic_nack <https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_nack>`__ method sets ``requeue=True`` by default. Set ``requeue=False`` instead.

-  If the error isn't expected to occur and it's unknown whether it can safely be ignored, the consumer can do nothing (e.g. allow the exception to be raised), in which case administrative action is required (e.g. purging the queue or changing the code).

Acking and nacking without requeueing both remove the message from the queue. However, if a `dead-letter exchange <https://www.rabbitmq.com/docs/dlx>`__ is configured, only the nack'd message is preserved, with an ``x-death`` header recording its original queue and routing key, allowing it to be reprocessed once the cause of the error is fixed (which can be in the consumer, if it hadn't been updated for a new message format).

.. seealso::

   *Message acknowledgment* under `Work Queues tutorial <https://www.rabbitmq.com/tutorials/tutorial-two-python>`__

Unused features
---------------

Topic exchanges
~~~~~~~~~~~~~~~

A `topic exchange <https://www.rabbitmq.com/tutorials/tutorial-five-python>`__ can be used to allow routing on multiple criteria. We don't have a clear use case for this yet.

A topic exchange could support collection-specific queues, but `priority queues <https://www.rabbitmq.com/docs/priority>`__ appear to be a simpler way to prioritize collections.

Publisher confirms
~~~~~~~~~~~~~~~~~~

It's possible to ensure message delivery (`see Python example <https://github.com/pika/pika/blob/main/docs/examples/blocking_publish_mandatory.md>`__) by using `publisher confirms <https://www.rabbitmq.com/docs/confirms#publisher-confirms>`__ and setting the `mandatory flag <https://www.rabbitmq.com/amqp-0-9-1-reference#basic.publish>`__.

However, for simplicity, in Python, we're using `Pika <https://pika.readthedocs.io/en/stable/>`__'s `BlockingConnection <https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html>`__, which would use a "publish-and-wait" strategy for publisher confirms, which is `officially discouraged <https://www.rabbitmq.com/docs/publishers#publisher-confirm-strategies>`__, because it would wait for each message to be `persisted to disk <https://www.rabbitmq.com/docs/confirms#when-publishes-are-confirmed>`__.

The cases that publisher confirms protect against are, in Python:

-  `pika.exceptions.UnroutableError <https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html#pika.adapters.blocking_connection.BlockingChannel.basic_publish>`__: The message can't be routed to any queue.
-  `pika.exceptions.NackError <https://www.rabbitmq.com/docs/confirms#server-sent-nacks>`__: An internal error occurs in the process responsible for the queue.
-  `More complex scenarios <https://www.rabbitmq.com/docs/confirms#publisher-confirms-and-guaranteed-delivery>`__.

All these are unlikely. To ensure messages are routable, before publishing a message, we make sure a queue exists and is bound to the exchange such that the message goes to that queue.
