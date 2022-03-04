import serial
import serial.tools.list_ports
import requests

class BridgeEsterno():
    
    def __init__(self, portname: str = None, port_description: str = "arduino", frequency: int = 9600, url="http://localhost:8000/"):
        self.url = url
        self.portname = portname
        self.port_description = port_description
        if self.portname is None:
            self.port_description = port_description
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if self.port_description.lower() in port.description.lower():
                    self.portname = port.device
        if self.portname is None:
            print(f"Connection failed: port {self.port_description} not found.")
            raise Exception
        try:
            self.serial = serial.Serial(self.portname, frequency, timeout=0)
        except:
            print(f"Connection failed: port {self.port_description} not found.")
            raise Exception
        print(f"Connecting to {self.portname}")
        self.inbuffer = []
    

    def loop(self):
        while (True):
            if self.serial is not None:
                if self.serial.in_waiting>0:
                    lastchar=self.serial.read(1)
                    if lastchar==b'\xfe':
                        print("Value received")
                        self.process_data()
                        self.inbuffer =[]
                    else:
                        self.inbuffer.append(lastchar)


    def process_data(self):
        if len(self.inbuffer) != 5 or self.inbuffer[0] != b'\xff':
            print("Errore: il pacchetto ricevuto non ha un formato corretto.")
            return False
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        if numval != 3:
            print("Errore: il pacchetto ricevuto non ha i dati corretti.")
            return False
        potentiometer_value = int.from_bytes(self.inbuffer[2], byteorder='little')
        photoresistor_value = int.from_bytes(self.inbuffer[3], byteorder='little')
        thermometer_value = int.from_bytes(self.inbuffer[4], byteorder='little')
        print("Potentiometer value: " + str(potentiometer_value))
        print("Photoresistor value: " + str(photoresistor_value))
        print("Thermometer value: " + str(thermometer_value))
        data = {'potentiometer': potentiometer_value, 'photoresistor': photoresistor_value, 'thermometer': thermometer_value}
        self.send_data(data)
        
    def send_data(self, data):
        ret = requests.post(self.url+"new_data/", json=data)
        if ret.status_code != 200:
            print("Errore: " + str(ret.content))
        print("Dati aggiornati correttamente")

if __name__ == '__main__':
    bridge = BridgeEsterno()
    bridge.loop()
