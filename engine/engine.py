import requests
from django.http import JsonResponse
from .MQTT import MQTTWriter


THRESHOLDS = {
    'potentiometer': 25,
    'photoresistor': 100,
    'thermometer': 10,
}

class Engine:
    def __init__(self, url, posizioni, comandi):
        self.url = url
        self.posizioni = posizioni
        self.comandi = comandi
        self.mqtt = MQTTWriter("127.0.0.1", 1883)
    
    def manage_windows(self, state, position):
        data = {'posizione': position, 'state': state}
        ret = requests.post(self.url+"update_windows/", data=data)
        return ret

    # data: {'value': newdata, 'old_value': olddata}

    def process_potentiometer_data(self, data):
        delta_value = data['value'] - data['old_value']
        if delta_value < 0 and delta_value > -THRESHOLDS['potentiometer']: # se negativo suppongo direzione del vento sud->nord
            # chiudi le finestre a sud
            self.mqtt.publish_general_message('sud', 'close')
            return self.manage_windows("closed", "sud")
        elif delta_value > 0 and delta_value > THRESHOLDS['potentiometer']: # se positivo suppongo direzione dlel vento nord->sud
            # chiudi le finestre a nord
            self.mqtt.publish_general_message('nord', 'close')
            return self.manage_windows("closed", "nord")
        return JsonResponse({'message': "Finestre aggiornate correttamente"})

    def process_photoresistor_data(self, data):
        if data['value'] <= THRESHOLDS['photoresistor']:
            # chiudi le finestre
            self.mqtt.publish_general_message('nord', 'close')
            self.mqtt.publish_general_message('sud', 'close')
            return self.manage_windows("closed", "all")
        else:
            # apri le finestre
            self.mqtt.publish_general_message('nord', 'open')
            self.mqtt.publish_general_message('sud', 'open')
            return self.manage_windows("open", "all")

    def process_thermometer_data(self, data):
        if data['value'] <= THRESHOLDS['thermometer']:
            # chiudi le finestre
            self.mqtt.publish_general_message('nord', 'close')
            self.mqtt.publish_general_message('sud', 'close')
            return self.manage_windows("closed", "all")
        else:
            # apri le finestre
            self.mqtt.publish_general_message('nord', 'open')
            self.mqtt.publish_general_message('sud', 'open')
            return self.manage_windows("open", "all")

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
    
    def update_window(self, id_arduino, pin, comando):
        self.mqtt.publish_specific_message(id_arduino, pin, comando)
