
class Engine:
    def __init__(self, potentiometer_value, photoresistor_value, thermometer_value):
        self.potentiometer_value = potentiometer_value
        self.photoresistor_value = photoresistor_value
        self.thermometer_value = thermometer_value
    
    # TODO: implementare funzioni per decidere se chiudere o no le finestre in base ai dati ricevuti
    # TODO: probabilmente non serve una classe ma bastano un set di funzioni
    # TODO: definire std per leggere quali finestre chiudere e di quali case (es: all: tutte, nord: solo nord, ...)
    