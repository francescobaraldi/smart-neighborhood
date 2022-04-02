import serial
import serial.tools.list_ports
import requests
from threading import Timer
from cloud.MQTT import MQTTReader
from cloud.config import WEB_APP_URL, SERVER_IP
import json


class BridgeInterno:
    def __init__(self, portname: str = None, port_description: str = "Dispositivo seriale USB (COM5)", frequency: int = 9600, url="http://localhost:8000/"):
        self.url = url
        self.portname = portname
        self.port_description = port_description
        if self.portname is None:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if self.port_description.lower() in port.description.lower():
                    self.portname = port.device
        try:
            self.serial = serial.Serial(self.portname, frequency, timeout=0)  # fa partire la setup() di Arduino
            # comunichiamo al db che chiudiamo le finestre (perchè la funzione setup() di Arduino chiude le finestre)
            ret = requests.get(self.url + "window/%s/%s/%s/" % (self.portname, 8, 'closed'))
            if ret.status_code != 200:
                print("Errore: " + str(ret.content))
                raise Exception
            self.turn_off_timeout(self.portname, 8)
            ret = requests.get(self.url + "window/%s/%s/%s/" % (self.portname, 9, 'closed'))
            if ret.status_code != 200:
                print("Errore: " + str(ret.content))
                raise Exception
            self.turn_off_timeout(self.portname, 9)
        except:
            print(f"Connection failed: port {self.port_description} not found.")
            raise Exception
        print(f"Connecting to {self.portname}")
        self.inbuffer = []
        self.mqtt = MQTTReader(SERVER_IP, 1883, [self.serial])
    
    def loop(self):
        while True:
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
        ret = requests.get(self.url+"window/turnoff/%s/%s/" % (device_name, pin))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
            raise Exception

    def process_data(self):
        if len(self.inbuffer) != 3 or self.inbuffer[0] != b'\xff':
            print("Errore: il pacchetto ricevuto non ha un formato corretto.")
            return False
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if numval != 1:
            print("Errore: il pacchetto ricevuto non ha i dati corretti.")
            return False
        window_pin = int.from_bytes(self.inbuffer[2], byteorder='little')  # Ricevo il pin della finestra il cui stato è stato cambiato dall'utente tramite il bottone
        ret = requests.get(self.url+"window/%s/%s/" % (self.portname, window_pin))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
            raise Exception
        stato = json.loads(ret.content)['stato']
        if stato == 'open':
            stato = 'closed'
        else:
            stato = 'open'
        ret = requests.get(self.url+"window/%s/%s/%s/" % (self.portname, window_pin, stato))
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
            raise Exception
        timer = Timer(1800, self.turn_off_timeout, [self.portname, window_pin])  # 1800s = 30 min
        timer.start()


if __name__ == '__main__':
    bridge = BridgeInterno(url="http://" + WEB_APP_URL)
    bridge.loop()
