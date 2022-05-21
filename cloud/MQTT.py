import paho.mqtt.client as mqtt
import requests
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.append(str(root))
import cloud.config as config
import json

"""
    Two types of topic:
    1) General (all the windows) -> /finestre/{command}/
    2) Specific for one windows -> /finestre/{device_name}/{pin}/{command}/
"""


class MQTTReader:  # serve al bridge interno per ricevere i messaggi
    def __init__(self, broker_ip, port, serials):
        self.broker_ip = broker_ip
        self.port = port
        self.serials = serials
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
        self.clientMQTT.subscribe("finestre/#")
        for serial in self.serials:
            self.clientMQTT.subscribe("finestre/%s/#" % serial.port)

    def on_message(self, client, userdata, msg):
        print("Message received on topic: %s" % msg.topic)
        fields = msg.topic.split("/")
        # fields.pop()  # remove last item of the list (empty string)
        encode_name = {'close': '0', 'open': '1'}
        if len(fields) == 2:
            comando = fields[1]
            for serial in self.serials:
                ret = requests.get(config.WEB_APP_URL + "window/%s/?/" % serial.portname)
                if ret.status_code != 200:
                    raise Exception
                windows = json.loads(ret.content)['windows']
                for window in windows:
                    if not window['timeout']:    
                        serial.write(bytes(window['pin'], 'utf-8'))
                        serial.write(bytes(encode_name[comando], 'utf-8'))
        elif len(fields) == 4:
            device_name = fields[1]
            pin = fields[2]
            comando = fields[3]
            for serial in self.serials:
                if serial.port == device_name:
                    serial.write(bytes(pin, 'utf-8'))
                    serial.write(bytes(encode_name[comando], 'utf-8'))


class MQTTWriter:  # serve all'engine per mandare i messaggi
    def __init__(self, broker_ip, port):
        self.broker_ip = broker_ip
        self.port = port
        self.setupMQTT()

    def setupMQTT(self):
        self.clientMQTT = mqtt.Client()
        self.clientMQTT.on_connect = self.on_connect
        print("Connecting...")
        self.clientMQTT.connect(self.broker_ip, self.port, 60)
        self.clientMQTT.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def publish_general_message(self, comando):
        self.clientMQTT.publish("finestre/%s" % comando)

    def publish_specific_message(self, device_name, pin, comando):
        self.clientMQTT.publish("finestre/%s/%s/%s" % (device_name, pin, comando))
