import os
import sys
import logging

lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
sys.path.append(lib_path)

# Third-party libraries
from kafka import KafkaProducer
from kafka.errors import KafkaError
from splunklib.searchcommands import (
    dispatch,
    StreamingCommand,
    Configuration,
    Option,
    validators,
)

# Initialize logging
logging.basicConfig(level=logging.INFO)


@Configuration()
class SplunkToKafka(StreamingCommand):
    """
    Send Splunk events to a specified Kafka topic.

    Syntax:
    | splunktokafka bootstrap_servers=<bootstrapserver_list> topic=<topic> [client_id=<client_id>] [field=<field>]
    """

    bootstrap_servers = Option(
        name='bootstrap_servers',
        doc='List of Kafka bootstrap servers',
        require=True
    )
    client_id = Option(
        name='client_id',
        doc='Kafka client identifier',
        require=False,
        default="kafka_splunk_producer"
    )
    field = Option(
        name='field',
        doc='Field in the event to send to Kafka',
        require=False,
        default="_raw"
    )
    topic = Option(
        name='topic',
        doc='Kafka topic to send events to',
        require=True
    )
    timeout = Option(
        name='timeout',
        doc='Timeout for sending a message to Kafka (in seconds)',
        require=False,
        default=10,
        validate=validators.Integer()
    )

    def stream(self, events):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, client_id=self.client_id)
        try:
            for event in events:
                try:
                    msg = event[self.field]
                    future = producer.send(self.topic, bytes(msg, encoding='utf8'))
                    record_metadata = future.get(timeout=self.timeout)

                except KafkaError as e:
                    logging.error(f"Failed to send message to Kafka: {e}")

                yield event
        finally:
            producer.close()


if __name__ == "__main__":
    dispatch(SplunkToKafka, sys.argv, sys.stdin, sys.stdout, __name__)
