## Overview

This app provides a custom command - *splunktokafka* - which pushes Splunk search results to a Kafka topic.


## Installation

- Log in to Splunk Web and navigate to "Apps » Manage Apps" via the app dropdown at the top left of Splunk's user interface
- Click the "install app from file" button
- Upload the file by clicking "Choose file" and selecting the app
- Click upload
- Restart Splunk if a dialog asks you to


## Usage

### Syntax

```
splunktokafka bootstrap_servers=<bootstrapserver_list> topic=<topic_name> client_id=<client_id> field=<field> timeout=<timeout>
```

### Description

- bootstrap_servers - specifies the list of kafka servers in the target cluster.
- topic - specifies the kafka topic to send the search results to. The topic must exist in the Kafka cluster.
- client_id - identifies the client at the kafka broker to help with troubleshooting (default=kafka_splunk_producer).
- field - specifies the name of the field containing the data you wish to send to Kafka (default=_raw).
- timeout - indicates the maximum number of seconds to wait for the Kafka servers to respond (default=10s).

## Examples

### Send \_raw field values (i.e. entire event) to test topic

| splunktokafka bootstrap_servers="192.168.0.1:9092,192.168.0.2:9092" topic=test

### Send error field values to order_errors topic

```
| splunktokafka bootstrap_servers="192.168.0.1:9092,192.168.0.2:9092" topic=order_errors field=error
```

## License

This software is licensed under the Apache License 2.0. Details can be found in
the file LICENSE.