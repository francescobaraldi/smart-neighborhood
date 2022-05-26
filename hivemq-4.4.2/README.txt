HiveMQ
======

HiveMQ contains the following packages:
- HiveMQ Enterprise Edition
- HiveMQ Enterprise Security Extension
- HiveMQ Enterprise Extension for Kafka
- HiveMQ Enterprise Bridge Extension
- MQTT CLI
- HiveMQ Kubernetes Operator

All extensions are disabled by default. See the guide of each extension for instructions on how to enable them.

For further information of the extension configurations see the HiveMQ User Guide:
https://www.hivemq.com/docs/hivemq/latest/enterprise-extensions/introduction.html

Quickstart HiveMQ
=================

Linux/Unix/MacOSX
-----------------
cd <hivemq_install_directory>/bin
./run.sh


Windows
-------
right click on <hivemq_install_directory>\bin\run.bat
select "Run as administrator"


HiveMQ Enterprise Security Extension
====================================

A detailed documentation can be found here:
https://www.hivemq.com/docs/ese/latest/enterprise-security-extension/ese-intro.html

Linux/Unix/MacOSX
-----------------
cd <hivemq_install_directory>/extensions/hivemq-enterprise-security-extension
rm -rf DISABLED


Windows
-------
right click on <hivemq_install_directory>\extensions\hivemq-enterprise-security-extension\DISABLED
select "delete"


HiveMQ Enterprise Extension for Kafka
=====================================

A detailed documentation can be found here:
https://www.hivemq.com/docs/kafka/latest/enterprise-extension-for-kafka/kafka.html

Linux/Unix/MacOSX
-----------------
cd <hivemq_install_directory>/extensions/hivemq-kafka-extension
rm -rf DISABLED


Windows
-------
right click on <hivemq_install_directory>\extensions\hivemq-kafka-extension\DISABLED
select "delete"


HiveMQ Enterprise Bridge Extension
==================================

Linux/Unix/MacOSX
-----------------
cd <hivemq_install_directory>/extensions/hivemq-bridge-extension
rm -rf DISABLED


Windows
-------
right click on <hivemq_install_directory>\extensions\hivemq-bridge-extension\DISABLED
select "delete"


HiveMQ MQTT CLI
===============

A detailed documentation can be found here:
https://hivemq.github.io/mqtt-cli/

Linux/Unix/MacOSX
-----------------
cd <hivemq_install_directory>/tools/mqtt-cli/bin
./mqtt-cli


Windows
-------

open the Command Prompt
cd <hivemq_install_directory>\tools\mqtt-cli\bin
mqtt-cli.bat


Quickstart HiveMQ Kubernetes Operator
=====================================

To run the HiveMQ Kubernetes Operator please read our documentation at:
https://www.hivemq.com/docs/operator/latest/kubernetes-operator/operator-intro.html#quick-start