import paho.mqtt.client as mqtt


class MQTTReader: # serve al bridge interno per ricevere i messaggi
    def __init__(self, broker_ip, port, posizioni, comandi, arduino, sers): # arduino dict: {'id_arduino': ['pin', ...], ...}
        self.broker_ip = broker_ip
        self.port = port
        self.posizioni = posizioni
        self.comandi = comandi
        self.arduino = arduino
        self.sers = sers
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
        for id_arduino, pins in self.arduino.items():
            for pin in pins:
                for comando in self.comandi:
                    self.clientMQTT.subscribe("finestre/%s/%s/%s/" % (id_arduino, pin, comando))

    def on_message(self, client, userdata, msg):
        print("Message received on topic: %s" % msg.topic)
        fields = msg.topic.split("/")
        encode_name = {'close': 0, 'open': 1}
        if len(fields) == 3:
            comando = fields[2]
            for ser in self.sers:
                self.ser.write(bytes(encode_name[comando], 'utf-8'))
        elif len(fields) == 4:
            id_arduino = fields[1]
            pin = fields[2]
            comando = fields[3]
            for ser in self.sers:
                if ser.port == id_arduino:
                    self.ser.write(bytes(encode_name[pin], 'utf-8'))
                    self.ser.write(bytes(encode_name[comando], 'utf-8'))


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
