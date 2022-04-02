from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATI_FINESTRE = [("open", "Aperta"), ("closed", "Chiusa")]

class Casa(models.Model):
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE)
    via = models.CharField(max_length=50)
    numero_civico = models.IntegerField()
    
    def __str__(self):
        return "Casa in via %s, %d" % (self.via, self.numero_civico)
    
class Finestra(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    stato = models.CharField(max_length=10, choices=STATI_FINESTRE)
    descrizione = models.CharField(max_length=50)
    device_name = models.CharField(max_length=100, default="000")
    pin = models.CharField(max_length=10, default="A0")
    timeout = models.BooleanField(default=False)
    
    def __str__(self):
        return "Finestra %s" % (self.descrizione)


class DatiAmbientali(models.Model):
    timestamp = models.DateTimeField()
    potentiometer_value = models.FloatField()
    photoresistor_value = models.FloatField()
    thermometer_value = models.FloatField()

class ChatTelegram(models.Model):
    chat_id = models.CharField(max_length=255)
    
    def __str__(self):
        return "Chat id: " + self.chat_id
