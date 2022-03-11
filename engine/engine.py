import requests
from django.http import JsonResponse

url = "http://localhost:8000/houses/"

THRESHOLDS = {
    'potentioemter': 25,
    'photoresistor': 100,
    'thermometer': 10,
}

def manage_windows(state, position):
    data = {'posizione': position, 'state': state}
    ret = requests.post(url+"update_windows/", data=data)
    return ret

# data: {'value': newdata, 'old_value': olddata}
# TODO: oltre ad aggiornare il database con i nuovi stati delle finestre (già fatto)
# bisogna mandare i comandi all'arduino degli attuatori tramite MQTT (da implementare)

def process_potentiometer_data(data):
    delta_value = data['value'] - data['old_value']
    if delta_value < 0 and delta_value > -THRESHOLDS['potentioemter']: # se negativo suppongo direzione del vento sud->nord
        # chiudi le finestre a sud
        return manage_windows("closed", "sud")
    elif delta_value > 0 and delta_value > THRESHOLDS['potentiometer']: # se positivo suppongo direzione dlel vento nord->sud
        # chiudi le finestre a nord
        return manage_windows("closed", "nord")
    return JsonResponse({'message': "Finestre aggiornate correttamente"})

def process_photoresistor_data(data):
    if data['value'] <= THRESHOLDS['photoresistor']:
        # chiudi le finestre
        return manage_windows("closed", "all")
    else:
        # apri le finestre
        return manage_windows("open", "all")

def process_thermometer_data(data):
    if data['value'] <= THRESHOLDS['thermometer']:
        # chiudi le finestre
        return manage_windows("closed", "all")
    else:
        # apri le finestre
        return manage_windows("open", "all")


def process_data(data):
    # TODO: gestire le priorità: quale sensore ha priorità più alta nella decisione?
    ret_potentiometer = process_potentiometer_data(data)
    ret_photoresistor = process_photoresistor_data(data)
    ret_thermometer = process_thermometer_data(data)
    if ret_potentiometer.status_code != 200:
        return ret_potentiometer
    elif ret_photoresistor != 200:
        return ret_photoresistor
    elif ret_thermometer != 200:
        return ret_thermometer
    return ret_potentiometer
