import serial
import serial.tools.list_ports
import requests
from threading import Timer
from engine.MQTT import MQTTReader


class BridgeInterno():    
    def __init__(self, portname: str = None, port_description: str = ["arduino"], frequency: int = 9600, url="http://localhost:8000/"):
        self.url = url
        self.portname = portname
        self.port_description = port_description
        if self.portname is None:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if self.port_description.lower() in port.description.lower():
                    self.portname = port.device
        try:
            self.serial = serial.Serial(self.portname, frequency, timeout=0)
        except:
            print(f"Connection failed: port {self.port_description} not found.")
            raise Exception
        print(f"Connecting to {self.portname}")
        self.inbuffer = []
        self.mqtt = MQTTReader("127.0.0.1", 1883, [self.serial])
    
    def loop(self):
        while (True):
            if self.serial is not None:
                if self.serial.in_waiting > 0:
                    lastchar = self.serial.read(1)
                    if lastchar == b'\xfe':
                        print("Value received")
                        self.process_data()
                        self.inbuffer =[]
                    else:
                        self.inbuffer.append(lastchar)
                        
    def turn_off_timeout(self, device_name, pin):
        ret = requests.get(self.url+"houses/window/turnoff/%s/%s/" % (device_name, pin))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))

    def process_data(self):
        if len(self.inbuffer) != 3 or self.inbuffer[0] != b'\xff':
            print("Errore: il pacchetto ricevuto non ha un formato corretto.")
            return False
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if numval != 1:
            print("Errore: il pacchetto ricevuto non ha i dati corretti.")
            return False
        window_pin = int.from_bytes(self.inbuffer[2], byteorder='little') # Ricevo il pin della finestra il cui stato è stato cambiato dall'utente tramite il bottone
        ret = requests.get(self.url+"houses/window/%s/%s/" % (self.portname, str(window_pin)))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
        stato = ret.content['stato']
        ret = requests.get(self.url+"houses/%s/%s/%s/" % (self.portname, window_pin, stato))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
        timer = Timer(1800, self.turn_off_timeout, [self.portname, window_pin])
        timer.start()
        
    # TODO: gestire messaggi da MQTT (quindi da decisioni su dati climatici e non manuali) e conseguente azionamento finestre (e scrivere su seriale)
    # TODO: gestire nell'MQTTReader la scrittura del pin anche nel caso generale


if __name__ == '__main__':
    bridge = BridgeInterno()
    bridge.loop()
