from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .serializers import *
import json
import datetime
import sys
from django.conf import settings
import sys
sys.path.append(str(settings.ROOT_PROJECT))
from engine import engine
from threading import Timer


def turn_off_timeout(device_name, pin):
    return HttpResponseRedirect("/houses/window/turnoff/%s/%s/" % (device_name, pin))



################################################################################
# Views per interfaccia utente #
################################################################################


@login_required
def main_page(request):
    case = Casa.objects.filter(proprietario=request.user)
    return render(request, "houses/main_page.html", {'request': request, 'case': case})


@login_required
def turn_on_timeout_change_state_web(request, finestra_id):
    finestra = get_object_or_404(Finestra, pk=finestra_id)
    if request.user != finestra.casa.proprietario:
        return HttpResponse("Non sei il proprietario di questa finestra")
    if finestra.stato == "open":
        finestra.stato = "closed"
    else:
        finestra.stato = "open"
    finestra.timeout = True
    finestra.save()
    timer = Timer(1800, turn_off_timeout, [finestra.device_name, finestra.pin])
    timer.start()
    eng = engine.Engine()
    if finestra.stato == 'closed':
        eng.move_window(finestra.device_name, finestra.pin, 'close')
    else:
        eng.move_window(finestra.device_name, finestra.pin, 'open')
    return HttpResponseRedirect("/houses/")



################################################################################
# Views per software #
################################################################################


@csrf_exempt
def new_data(request):
    if request.method == "POST":
        # TODO: eliminare timestamp vecchi per non sovraccaricare il db?
        data = json.loads(request.body)
        eng = engine.Engine()
        eng.process_data(data)
        #ser = DatiAmbientaliSerializer(data=data)
        #if ser.is_valid():
            #new_dati_ambientali = ser.save(commit=False)
            #new_dati_ambientali.timestamp = datetime.datetime.now()
            #new_dati_ambientali.save()
            #return JsonResponse({'message': "Dati aggiornati correttamente"})
        return JsonResponse(data)


@csrf_exempt
def change_state_all_windows(request, stato):
    windows = get_list_or_404(Finestra)
    for window in windows:
        window.state = stato
        window.save()
    return JsonResponse({'message': "Finestre aggiornate correttamente"})

    
def get_window(request, device_name, pin):
    window = Finestra.objects.filter(device_name=device_name, pin=pin)
    if len(window) != 1:
        return JsonResponse({'error': "Errore"})
    return JsonResponse({'stato': window[0].stato})


def turn_on_timeout_change_state_button(request, device_name, pin, stato):
    window = Finestra.objects.filter(device_name=device_name, pin=pin)
    if len(window) != 1:
        return JsonResponse({'error': "Errore"})
    window = window[0]
    window.state = stato
    window.timeout = True
    window.save()
    return JsonResponse({'message': "Cambiato stato correttamente"})


def turn_off_timeout(request, device_name, pin):
    window = Finestra.objects.filter(device_name=device_name, pin=pin)
    if len(window) != 1:
        return JsonResponse({'error': "Errore"})
    window.timeout = False
    window.save()
    return JsonResponse({'message': "Timeout spento correttamente"})
