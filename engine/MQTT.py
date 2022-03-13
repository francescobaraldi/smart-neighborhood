import paho.mqtt.client as mqtt


class MQTTReader: # serve al bridge interno per ricevere i messaggi
    def __init__(self, broker_ip, port, posizioni, comandi, arduino, ser): # arduino dict: {'id_arduino': ['pin', ...], ...}
        self.broker_ip = broker_ip
        self.port = port
        self.posizioni = posizioni
        self.comandi = comandi
        self.arduino = arduino
        self.ser = ser
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
        for key, pins in self.arduino.items():
            for pin in pins:
                for comando in self.comandi:
                    self.clientMQTT.subscribe("finestre/%s/%s/%s/" % (key, pin, comando))

    def on_message(self, client, userdata, msg):
        print("Message received on topic: %s" % msg.topic)
        fields = msg.topic.split("/")
        if len(fields) == 3:
            posizione = fields[1]
            comando = fields[2]
            # TODO: scrivere sulla seriale dell'arduino degli attuatori per mandare il comando specifico alle finestre specifiche
        elif len(fields) == 4:
            id_arduino = fields[1]
            pin = fields[2]
            comando = fields[3]
            # TODO: scrivere sulla seriale ma in questo caso non su tutti gli arduino ma solo su quello specificato e sul pin speicifcato



class MQTTWriter: # serve all'engine per mandare i messaggi
    def __init__(self, broker_ip, port):
        self.broker_ip = broker_ip
        self.port = port
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
        
    def publish_general_message(self, posizione, comando):
        self.clientMQTT.publish("finestre/%s/%s/" % (posizione, comando))
    
    def publish_specific_message(self, id_arduino, pin, comando):
        self.clientMQTT.publish("finestre/%s/%s/%s/" % (id_arduino, pin, comando))
