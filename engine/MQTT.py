import paho.mqtt.client as mqtt


class MQTT:
    def __init__(self, broker_ip, port, posizioni, comandi):
        self.broker_ip = broker_ip
        self.port = port
        self.posizioni = posizioni
        self.comandi = comandi
        self.setupMQTT()

    def setupMQTT(self):
        self.clientMQTT = mqtt.Client()
        self.clientMQTT.on_connect = self.on_connect
        self.clientMQTT.on_message = self.on_message
        print("Connecting...")
        self.clientMQTT.connect(self.broker_ip, self.port, 60)
        self.clientMQTT.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        for posizione in self.posizioni:
            for comando in self.comandi:
                self.clientMQTT.subscribe("finestre/%s/%s/" % (posizione, comando))

    def on_message(self, client, userdata, msg):
        print("Message received on topic: %s" % msg.topic)
        fields = msg.topic.split("/")
        posizione = fields[1]
        comando = fields[2]
        # TODO: scrivere sulla seriale dell'arduino degli attuatori per mandare il comando specifico alle finestre specifiche
        
    def publish_message(self, posizione, comando, ser=None):
        self.clientMQTT.publish("finestre/%s/%s/" % (posizione, comando))
