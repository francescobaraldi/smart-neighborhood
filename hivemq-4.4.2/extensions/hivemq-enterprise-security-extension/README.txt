= HiveMQ Enterprise Security Extension

The HiveMQ Enterprise Security Extension (ESE) expands the role, user, and permission-management capabilities of HiveMQ
Enterprise and Professional editions.
ESE allows you to use different sources of external authentication and authorization data to authenticate and authorize
MQTT clients.
In the ESE, you define realms to partition your server into protected areas that can each have their own authentication
and / or authorization scheme.
The ESE processes incoming client connections in highly configurable pipelines that offer customizable stages to handle
the authentication and authorization of your clients.

TIP: If you are unfamiliar with MQTT and HiveMQ security concepts, we highly recommend this article:
https://www.hivemq.com/mqtt-security-fundamentals/


== Requirements

* A running HiveMQ Professional or Enterprise Edition installation
** Versions 4.1.0 and higher for MQTT client security
** Versions 4.2.0 and higher for control-center security
* A running SQL database


== Installation

. Configure the HiveMQ Enterprise Security Extension in the `enterprise-security-extension.xml` file that is contained
  in this folder.
See the https://www.hivemq.com/docs/4.2/enterprise-extensions/ese.html[official documentation] for
  all possible configuration options.
. Move this folder into the `extensions` folder of your HiveMQ installation.

----
└─ <HiveMQ folder>
    ├─ bin
    ├─ config
    ├─ data
    ├─ extensions
    │   ├─ hivemq-enterprise-security-extension
    │   └─ ...
    ├─ license
    ├─ log
    └─ ...
----

CAUTION: To secure an entire HiveMQ cluster, the HiveMQ Enterprise Security Extension must be installed on every HiveMQ
broker node in the cluster.

To verify that the extension is installed and configured properly, check your HiveMQ logs.

TIP: If you want to change the configuration of the ESE, you can add a `DISABLED` file to the ESE folder to disable the
extension. To enable ESE once more, remove the `DISABLED` file that you added.


== Support

If you need help with the HiveMQ Enterprise Security Extension or have suggestions on how we can improve the extension,
please contact us at contact@hivemq.com.
