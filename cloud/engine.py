import requests
import cloud.MQTT as MQTT
import cloud.open_weather as open_weather
import cloud.bot_telegram as bot_telegram
import cloud.config as config


THRESHOLDS = {
    'potentiometer': 128,
    'photoresistor': 200, # Cambiare a 100, messo a 200 per test
    'temperature': 10,
    'weather': [3, 7, 8]
}

class Engine:
    def __init__(self):
        self.mqtt = MQTT.MQTTWriter(config.SERVER_IP, 1883)
        self.openweather = open_weather.OpenWeather(config.LOCATION_OPENWEATHER, config.API_KEY_OPENWEATHER)
    
    def update_windows_database(self, state):
        ret = requests.post(config.WEB_APP_URL + "window/all/%s/" % state)
        return ret

    # data: {'potentiometer': potentiometer_data, 'photoresistor': photoresistor_data}

    def process_data(self, data):
        data_openweather = self.openweather.get_data()
        data['temperature'] = data_openweather['main']['temp'] - 273.15 - 5
        data['weather_id'] = data_openweather['weather'][0]['id']
        open_conditions =  (data['weather_id'] // 100 in THRESHOLDS['weather']) + (data['temperature'] >= THRESHOLDS['temperature']) + (data['potentiometer'] <= THRESHOLDS['potentiometer']) + (data['photoresistor'] >= THRESHOLDS['photoresistor'])
        close_conditions = (data['weather_id'] // 100 not in THRESHOLDS['weather']) + (data['temperature'] < THRESHOLDS['temperature']) + (data['potentiometer'] > THRESHOLDS['potentiometer']) + (data['photoresistor'] < THRESHOLDS['photoresistor'])
        if open_conditions >= 2:
            self.mqtt.publish_general_message('open')
            bot_telegram.send_notification('open')
            return self.update_windows_database('open')
        elif close_conditions >= 3:
            self.mqtt.publish_general_message('close')
            bot_telegram.send_notification('close')
            return self.update_windows_database('closed')
    
    def move_window(self, device_name, pin, comando):
        self.mqtt.publish_specific_message(device_name, pin, comando)

singleton = False
eng = None
def get_engine():
    global eng 
    global singleton
    if singleton == False:
        eng = Engine()
        singleton = True
    return eng
    
