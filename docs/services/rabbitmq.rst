RabbitMQ
========

The shortest explanation of RabbitMQ is the `AMQP 0-9-1 Model in Brief <https://www.rabbitmq.com/tutorials/amqp-concepts.html#amqp-model>`__:

-  Multiple *publishers* can publish messages to *exchanges*
-  An *exchange* routes the messages it receives to one or more *queues*, using rules called *bindings*
-  Multiple *consumers* can subscribe to one or more *queues*

It is recommended to be familiar with all `RabbitMQ tutorials <https://www.rabbitmq.com/getstarted.html>`__.

.. seealso::

   -  `AMQP 0-9-1 Model Explained <https://www.rabbitmq.com/tutorials/amqp-concepts.html>`__
   -  `Reliability Guide <https://www.rabbitmq.com/reliability.html>`__
   -  `Full documentation <https://www.rabbitmq.com/documentation.html>`__

Development
-----------

1. Install RabbitMQ. On macOS:

   .. code-block:: shell

      brew install rabbitmq

1. Enable the `management plugin <https://www.rabbitmq.com/management.html>`__:

   .. code-block:: shell

      rabbitmq-plugins enable rabbitmq_management

1. Access the management plugin at http://127.0.0.1:15672 (user: ``guest``, password: ``guest``)

In Python, use `pika <https://pika.readthedocs.io/en/stable/>`__ to interact with RabbitMQ directly. Don't use Celery, because its abstractions adds inefficiencies, requiring `complex workarounds <http://blog.untrod.com/2015/03/how-celery-chord-synchronization-works.html>`__. See pika's examples `in its documentation <https://pika.readthedocs.io/en/stable/examples.html>`__ and `on GitHub <https://github.com/pika/pika/tree/master/examples>`__.

Heartbeat
---------

If a consumer takes too long to process a message, the heartbeat might timeout, causing the connection to RabbitMQ to drop (for Python, see pika's `readme <https://github.com/pika/pika/#requesting-message-acknowledgements-from-another-thread>`__ and `example <https://pika.readthedocs.io/en/latest/examples/heartbeat_and_blocked_timeouts.html>`__).

Disabling the heartbeat is `discouraged <https://stackoverflow.com/a/51755383/244258>`__ by RabbitMQ developers. The solution is to process the message in a separate thread (`see Python example <https://github.com/pika/pika/blob/master/examples/basic_consumer_threaded.py>`__).

That said, from Datlab's experience, the RabbitMQ connection can be unreliable, regardless of the connection settings. In any case, for the Data Registry, all consumers are asynchronous and use two threads: one to manage the connection, another to process the message.

Acknowledgements
----------------

In some cases, messages are acknowledged when a point-of-no-return is reached, before the messages are processed. For example, when importing data from Kingfisher into Pelican, messages for the next phase are already published for the yet-unfinished job; it is not simple to go back if processing fails.

.. https://github.com/open-contracting/data-registry/issues/140

Unused features
---------------

Multicast routing
~~~~~~~~~~~~~~~~~

In a direct exchange, it's possible for a queue to have multiple bindings to an exchange, in order to route messages with different routing keys to it. For now, each of our queues has a single binding, such that our exchange behaves like the `default exchange <https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-default>`__.

Topic exchanges
~~~~~~~~~~~~~~~

A `topic exchange <https://www.rabbitmq.com/tutorials/tutorial-five-python.html>`__ can be used to allow routing on multiple criteria. We don't have a clear use case for this yet.

A topic exchange could support collection-specific queues, but `priority queues <https://www.rabbitmq.com/priority.html>`__ appear to be a simpler way to prioritize collections.

Publisher confirms
~~~~~~~~~~~~~~~~~~

It's possible to ensure message delivery (`see Python example <https://github.com/pika/pika/blob/master/docs/examples/blocking_publish_mandatory.rst>`__) by using `publisher confirms <https://www.rabbitmq.com/confirms.html#publisher-confirms>`__ and setting the `mandatory flag <https://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.publish>`__.

However, for simplicity, in Python, we're using `pika <https://pika.readthedocs.io/>`__'s `BlockingConnection <https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html>`__, which would use a "publish-and-wait" strategy for publisher confirms, which is `officially discouraged <https://www.rabbitmq.com/publishers.html#publisher-confirm-strategies>`__, because it would wait for each message to be `persisted to disk <https://www.rabbitmq.com/confirms.html#when-publishes-are-confirmed>`__.

The cases that publisher confirms protect against are, in Python:

-  `pika.exceptions.UnroutableError <https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html#pika.adapters.blocking_connection.BlockingChannel.basic_publish>`__: The message can't be routed to any queue.
-  `pika.exceptions.NackError <https://www.rabbitmq.com/confirms.html#server-sent-nacks>`__: An internal error occurs in the process responsible for the queue.
-  `More complex scenarios <https://www.rabbitmq.com/confirms.html#publisher-confirms-and-guaranteed-delivery>`__.

All these are unlikely. To ensure messages are routable, before publishing a message, we make sure a queue exists and is bound to the exchange such that the message goes to that queue.
