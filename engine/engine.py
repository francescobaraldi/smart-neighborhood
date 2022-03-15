import requests
from django.http import JsonResponse
from .MQTT import MQTTWriter


THRESHOLDS = {
    'potentiometer': 128,
    'photoresistor': 100,
    'temperature': 10,
}

class Engine:
    def __init__(self, url, comandi):
        self.url = url
        self.comandi = comandi
        self.mqtt = MQTTWriter("127.0.0.1", 1883)
    
    def manage_windows(self, state):
        data = {'state': state}
        ret = requests.post(self.url+"update_windows/", data=data)
        return ret

    # data: {'potentiometer': potentiometer_data, 'photoresistor': photoresistor_data, 'temperature': temperature_data}

    def process_potentiometer_data(self, data):
        if data['potentiometer'] >= THRESHOLDS['potentiometer']:
            # chiudi le finestre
            self.mqtt.publish_general_message('close')
            return self.manage_windows("closed")
        elif data['potentiometer'] < THRESHOLDS['potentiometer']:
            # apri le finestre
            self.mqtt.publish_general_message('open')
            return self.manage_windows("open")
        return JsonResponse({'message': "Finestre aggiornate correttamente"})

    def process_photoresistor_data(self, data):
        if data['photoresistor'] <= THRESHOLDS['photoresistor']:
            # chiudi le finestre
            self.mqtt.publish_general_message('close')
            return self.manage_windows("closed")
        else:
            # apri le finestre
            self.mqtt.publish_general_message('open')
            return self.manage_windows("open")

    def process_temperature_data(self, data):
        if data['temperature'] <= THRESHOLDS['temperature']:
            # chiudi le finestre
            self.mqtt.publish_general_message('close')
            return self.manage_windows("closed")
        else:
            # apri le finestre
            self.mqtt.publish_general_message('open')
            return self.manage_windows("open")

    def process_data(self, data):
        # TODO: gestire le priorità: quale sensore ha priorità più alta nella decisione?
        ret_potentiometer = self.process_potentiometer_data(data)
        ret_photoresistor = self.process_photoresistor_data(data)
        ret_thermometer = self.process_thermometer_data(data)
        if ret_potentiometer.status_code != 200:
            return ret_potentiometer
        elif ret_photoresistor != 200:
            return ret_photoresistor
        elif ret_thermometer != 200:
            return ret_thermometer
        return ret_potentiometer
    
    def update_window(self, device_name, pin, comando):
        self.mqtt.publish_specific_message(device_name, pin, comando)
