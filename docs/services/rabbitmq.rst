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

#. Install RabbitMQ. On macOS:

   .. code-block:: shell

      brew install rabbitmq

#. Enable the `management plugin <https://www.rabbitmq.com/management.html>`__:

   .. code-block:: shell

      rabbitmq-plugins enable rabbitmq_management

#. Access the management plugin at http://127.0.0.1:15672 (user: ``guest``, password: ``guest``)

In Python, use `pika <https://pika.readthedocs.io/en/stable/>`__ to interact with RabbitMQ: see examples `in its documentation <https://pika.readthedocs.io/en/stable/examples.html>`__ and `on GitHub <https://github.com/pika/pika/tree/master/examples>`__. Don't use Celery, because its abstractions add inefficiencies, requiring `complex workarounds <http://blog.untrod.com/2015/03/how-celery-chord-synchronization-works.html>`__.

Code style
----------

Connect to the broker using a connection string stored in the ``RABBIT_URL`` environment variable.

In Python:

.. code-block:: python

   import pika

   RABBIT_URL = os.getenv("RABBIT_URL", "amqp://localhost")

   connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))

To add query string parameters:

.. code-block:: python

   from urllib.parse import parse_qs, urlencode, urlsplit

   import pika

   RABBIT_URL = os.getenv("RABBIT_URL", "amqp://localhost")

   parsed = urlsplit(RABBIT_URL)
   query = parse_qs(parsed.query)
   query.update({"blocked_connection_timeout": 600, "heartbeat": 300})

   connection = pika.BlockingConnection(pika.URLParameters(parsed._replace(query=urlencode(query)).geturl()))

Design decisions
----------------

Bindings
~~~~~~~~

*Consumers declare and bind queues, not publishers*. To reduce coupling, a publisher does not control how its messages are routed: it simply sets the routing key. Each consumer then declares its own queue to read from, and it sets the routing keys that the queue binds to. As such, any number of consumers can read a publisher's messages; if no consumer reads the messages, they are undelivered, by design. This pattern makes it easier to re-order, add or remove consumers.

Heartbeat
~~~~~~~~~

If a consumer takes too long to process a message, the heartbeat might timeout, causing the connection to RabbitMQ to drop (for Python, see pika's `readme <https://github.com/pika/pika/#requesting-message-acknowledgements-from-another-thread>`__ and `example <https://pika.readthedocs.io/en/latest/examples/heartbeat_and_blocked_timeouts.html>`__).

Disabling heartbeats is `highly discouraged <https://www.rabbitmq.com/heartbeats.html>`__. The solution is to process the message in a separate thread (`see Python example <https://github.com/pika/pika/blob/master/examples/basic_consumer_threaded.py>`__).

That said, from Datlab's experience, the RabbitMQ connection can be unreliable, regardless of the connection settings. In any case, for the Data Registry, most consumers are asynchronous and use two threads: one to manage the connection, another to process the message.

Acknowledgements
~~~~~~~~~~~~~~~~

If a consumer is interrupted or fails before a message is ack'd, the broker `automatically requeues <https://www.rabbitmq.com/confirms.html#automatic-requeueing>`__ the message, once either the `acknowledgement timeout <https://www.rabbitmq.com/consumers.html#acknowledgement-timeout>`__ (30 minutes by default) or the `heartbeat timeout <https://www.rabbitmq.com/heartbeats.html>`__ is reached, at which time the consumer is considered buggy, stuck or unavailable by the broker.

Now, what to do about the unacknowledged message?

-  If the message is processable, either the consumer can `negatively acknowledge <https://www.rabbitmq.com/nack.html>`__ the message, or the consumer can do nothing. Sometime later, a consumer will receive it again, process it and acknowledge it.

   .. note::

      In Python, pika's `basic_nack <https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_nack>`__ method sets ``requeue=True`` by default.

-  If the message is unprocessable:

   -  If this case is expected to occur, or if there's no consequence to ignoring the message (like causing a silent failure), the consumer should handle the error, write to a log, and acknowledge the message.
   -  If this case isn't expected to occur and it's unknown whether it can safely be ignored, the consumer can do nothing, in which case administrative action is required (e.g. purging the queue).

   Whether the error is expected or not, you need to decide whether the consumer should publish an output message based on the input message: in other words, you need to decide whether processing stops or continues.

Whether the messages is processable or not, you need to decide whether the consumer should continue to receive messages.

In some cases, a message is acknowledged once a point-of-no-return is reached, *before* its processing is completed. For example, when importing data from Kingfisher into Pelican, each message identifies a collection to import. After some initial processing, the consumer performs database operations to import data and publish messages. If an operation fails, the consumer cannot easily "retry" the original message, without encountering integrity errors and creating duplicate work. As such, the message is acknowledge at this point-of-no-return.

.. note::

   If a message is not ack'd on a channel within the acknowledgement timeout, the broker closes the channel. This might cause unexpected errors the next time the consumer uses the channel.

.. seealso::

   *Message acknowledgment* under `Work Queues tutorial <https://www.rabbitmq.com/tutorials/tutorial-two-python.html>`__

.. https://github.com/open-contracting/data-registry/issues/140

Consumer prefetch
~~~~~~~~~~~~~~~~~

In our projects, `prefetch count <https://www.rabbitmq.com/confirms.html#channel-qos-prefetch>`__ is set to 1, which is the `most conservative <https://www.rabbitmq.com/confirms.html#channel-qos-prefetch-throughput>`__ option. Since consumers are slow compared to RabbitMQ, using a less conservative option is not expected to yield a performance improvement.

Unused features
---------------

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
