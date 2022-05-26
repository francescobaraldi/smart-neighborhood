= HiveMQ Enterprise Extension for Kafka

The HiveMQ Enterprise Extension for Kafka implements the native Kafka protocol inside the HiveMQ broker.
This allows the seamless integration of MQTT messages with one or multiple Kafka clusters.

== Requirements

To run the HiveMQ Enterprise Extension for Kafka the following requirements must be met:

* A running HiveMQ Professional or Enterprise Edition installation (versions 4.1.0 and higher)
* A running Kafka Cluster (versions 0.10.2 and higher)
* A valid kafka-extension license (otherwise the extension will be disabled after 5 hours,)

== Installation

* To install the HiveMQ Enterprise Extension for Kafka move this folder into the `extensions` folder of your HiveMQ installation.
* Place the license for the kafka-extension in the `license` folder of HiveMQ.

----
 |- <HiveMQ folder>
   |- bin
   |- config
   |- extensions
     |- hivemq-kafka-extension
   |- data
 ...
----

CAUTION: The HiveMQ Enterprise Extension for Kafka must be installed on all HiveMQ broker nodes in a HiveMQ cluster to function properly.

* The extension is now installed and needs to be configured for your individual Kafka cluster(s) and topics.
An example configuration file can be found inside this folder, it is named `kafka-configuration.example.xml`.
See the https://www.hivemq.com/docs/latest/enterprise-extensions/kafka.html#configuration[configuration chapter in the official documentation] for all possible configuration options.

You can check if the extension is installed and configured properly by checking the HiveMQ Logs and the then created Kafka tab of the HiveMQ Control Center.

== Support

In case you need any help with the HiveMQ Enterprise Extension for Kafka or have any suggestions for improvement please contact support@hivemq.com.
