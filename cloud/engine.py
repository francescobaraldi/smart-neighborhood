import requests
import cloud.MQTT as MQTT
import cloud.open_weather as open_weather
import cloud.bot_telegram as bot_telegram
import cloud.config as config
import json


THRESHOLDS = {
    'potentiometer_low': 80,
    'potentiometer_high': 140,
    'photoresistor_low': 80,
    'photoresistor_high': 120,
    'temperature_low': 5,
    'temperature_high': 20,
    'weather_good': [7],  # Considerare anche il valore esatto 800
    'weather_bad': [2, 5, 6]
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
        data['temperature'] = data_openweather['main']['temp'] - 273.15
        data['weather_id'] = data_openweather['weather'][0]['id']
        open_conditions =  (data['weather_id'] // 100 in THRESHOLDS['weather_good'] or data['weather_id'] == 800) + (data['temperature'] >= THRESHOLDS['temperature_high']) + (data['potentiometer'] <= THRESHOLDS['potentiometer_low']) + (data['photoresistor'] >= THRESHOLDS['photoresistor_high'])
        close_conditions = (data['weather_id'] // 100 in THRESHOLDS['weather_bad']) + (data['temperature'] < THRESHOLDS['temperature_low']) + (data['potentiometer'] > THRESHOLDS['potentiometer_high']) + (data['photoresistor'] < THRESHOLDS['photoresistor_low'])
        if open_conditions >= 2:
            self.mqtt.publish_general_message('open')
            bot_telegram.send_notification('open')
            return self.update_windows_database('open')
        elif close_conditions >= 3:
            self.mqtt.publish_general_message('close')
            bot_telegram.send_notification('close')
            return self.update_windows_database('closed')
        else:  # Se entro qua sono in una situazione ambigua
            ret = requests.get(config.WEB_APP_URL + "window/changed")
            if ret.status_code != 200:
                raise Exception
            last_windows_changed = json.loads(ret.content)['windows']
            houses = []
            num_closed = 0
            num_open = 0
            for window in last_windows_changed:
                if window['casa'] not in houses:
                    houses.append(window['casa'])
                    if window['stato'] == 'closed':
                        num_closed += 1
                    elif window['stato'] == 'open':
                        num_open += 1
            
            if num_closed > 1 >= num_open:  # Almeno 2 vicini hanno chiuso le finestre nell'ultima ora -> chiudi le finestre
                self.mqtt.publish_general_message('close')
                bot_telegram.send_notification('close')
                return self.update_windows_database('closed')
            elif num_open > 1 >= num_closed:  # Almeno 2 vicini hanno aperto le finestre nell'ultima ora -> apro le finestre
                self.mqtt.publish_general_message('open')
                bot_telegram.send_notification('open')
                return self.update_windows_database('open')
            # else: significa che o num_closed = num_open -> non faccio niente,
            #       o ci sono meno di 2 vicini che hanno modificato le finestre nell'ultima ora -> non faccio niente
            
    
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
