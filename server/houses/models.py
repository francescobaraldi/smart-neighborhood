from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATI_FINESTRE = [("open", "Aperta"), ("closed", "Chiusa")]
POSIZIONI_FINESTRE = [("nord", "Nord"), ("sud", "Sud")]

class Casa(models.Model):
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE)
    via = models.CharField(max_length=50)
    numero_civico = models.IntegerField()
    
    def __str__(self):
        return "Casa in via %s, $d" % (self.via, self.numero_civico)
    
class Finestra(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    stato = models.CharField(max_length=10, choices=STATI_FINESTRE)
    posizione = models.CharField(max_length=10, choices=POSIZIONI_FINESTRE)
    descrizione = models.CharField(max_length=50)
    
    def __str__(self):
        return "Finestra %s" % self.posizione
