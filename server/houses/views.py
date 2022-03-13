from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from telegram import LoginUrl
from .models import *
from .forms import *
from .serializers import *
import json
import datetime
from django.utils import timezone
import sys
from django.conf import settings
import sys
sys.path.append(str(settings.ROOT_PROJECT))
from engine import engine


@login_required
def main_page(request):
    case = Casa.objects.filter(proprietario=request.user)
    return render(request, "houses/main_page.html", {'request': request, 'case': case})

@login_required
def aggiorna_finestra(request, finestra_id):
    finestra = get_object_or_404(Finestra, pk=finestra_id)
    if request.user != finestra.casa.proprietario:
        return HttpResponse("Non sei il proprietario di questa finestra")
    if finestra.stato == "open":
        finestra.stato = "closed"
    else:
        finestra.stato = "open"
    finestra.save()
    eng = engine.Engine("http://localhost:8000/houses/", [pos[0] for pos in POSIZIONI_FINESTRE], ['close', 'open'])
    
    # ERRORE: in questo modo aggiorno tutte le finestre con la posizione 'finestra.posizione'
    # necessario implementare lato MQTT messaggi specifici per ogni servo motore
    # Possibilità di inserire nel model della finestra il coidce univoco dell'arduino a cui è associato il servomotore e creare topic
    # separati per comandi specifici per una sola finestra, ma se con un arduino gestiamo più finestre questo approccio non va bene
    if finestra.stato == 'closed':
        eng.update_window(finestra.posizione, 'close')
    else:
        eng.update_window(finestra.posizione, 'open')  
    # TODO: Mandare il comando all'arduino per chiudere/aprire davvero la finestra tramite MQTT (da implementare)
    return HttpResponseRedirect("/houses/")

@csrf_exempt
def new_data(request):
    if request.method == "POST":
        # TODO: eliminare timestamp vecchi per non sovraccaricare il db?
        data = json.loads(request.body)
        ser = DatiAmbientaliSerializer(data=data)
        if ser.is_valid():
            new_dati_ambientali = ser.save(commit=False)
            new_dati_ambientali.timestamp = datetime.now()
            new_dati_ambientali.save()
            eng = engine.Engine("http://localhost:8000/houses/", [pos[0] for pos in POSIZIONI_FINESTRE], ['close', 'open'])
            eng.process_data(data)
            return JsonResponse({'message': "Dati aggiornati correttamente"})
        return JsonResponse(ser.errors)

@csrf_exempt
def update_windows(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data['posizione'] == "all":
            windows = get_list_or_404(Finestra)
        else:
            # windows = Finestra.objects.filter(posizione=data['posizione'])
            windows = get_list_or_404(Finestra, posizione=data['posizione'])
        for window in windows:
            window.state = data['state']
            window.save()
        return JsonResponse({'message': "Finestre aggiornate correttamente"})
