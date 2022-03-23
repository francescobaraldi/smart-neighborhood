import requests
from django.http import JsonResponse
from .MQTT import MQTTWriter
from .open_weather import OpenWeather
from .bot_telegram import send_notification


THRESHOLDS = {
    'potentiometer': 128,
    'photoresistor': 100,
    'temperature': 10,
    'weather': [3, 7, 8]
}

class Engine:
    def __init__(self, url):
        self.url = url
        self.mqtt = MQTTWriter("127.0.0.1", 1883)
        self.openweather = OpenWeather("Modena, Italia", "a4d0ee049787674041208b1744a3a95b")
    
    def update_windows_database(self, state):
        ret = requests.post(self.url+"window/all/%s/" % state)
        return ret

    # data: {'potentiometer': potentiometer_data, 'photoresistor': photoresistor_data}

    def process_data(self, data):
        data_openweather = self.openweather.get_data()
        data['temperature'] = data_openweather['main']['temp'] - 273.15
        data['weather_id'] = data_openweather['weather'][0]['id']
        open_conditions =  (data['weather_id'] // 100 in THRESHOLDS['weather']) + data['temperature'] >= THRESHOLDS['temperature'] + data['potentiometer'] <= THRESHOLDS['potentiometer'] + data['photoresistor'] >= THRESHOLDS['photoresistor']
        close_conditions = (data['weather_id'] // 100 not in THRESHOLDS['weather']) + data['temperature'] < THRESHOLDS['temperature'] + data['potentiometer'] > THRESHOLDS['potentiometer'] + data['photoresistor'] < THRESHOLDS['photoresistor']
        if open_conditions >= 2:
            self.mqtt.publish_general_message('open')
            send_notification('open')
            return self.update_windows_database('open')
        elif close_conditions >= 3:
            self.mqtt.publish_general_message('close')
            send_notification('close')
            return self.update_windows_database('closed')
    
    def move_window(self, device_name, pin, comando):
        self.mqtt.publish_specific_message(device_name, pin, comando)
