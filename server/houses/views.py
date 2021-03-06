from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
from cloud import engine
from threading import Timer


def turn_off_timeout(device_name, pin):
    return HttpResponseRedirect("/houses/window/turnoff/%s/%s/" % (device_name, pin))



################################################################################
# Views per interfaccia utente #
################################################################################


@csrf_exempt
@login_required
def main_page(request):
    case = Casa.objects.filter(proprietario=request.user)
    return render(request, "houses/main_page.html", {'request': request, 'case': case})


@csrf_exempt
@login_required
def turn_on_timeout_change_state_web(request, finestra_id):
    finestra = get_object_or_404(Finestra, pk=finestra_id)
    if request.user != finestra.casa.proprietario:
        return HttpResponse("Non sei il proprietario di questa finestra")
    if finestra.stato == "open":
        finestra.stato = "closed"
    else:
        finestra.stato = "open"
    finestra.ultima_modifica = timezone.now()
    finestra.timeout = True
    finestra.save()
    timer = Timer(1800, turn_off_timeout, [finestra.device_name, finestra.pin])
    timer.start()
    eng = engine.get_engine()
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
        data = json.loads(request.body)
        print(data)
        eng = engine.get_engine()
        eng.process_data(data)
        return JsonResponse(data)


@csrf_exempt
def change_state_all_windows(request, stato):
    windows = get_list_or_404(Finestra)
    for window in windows:
        if not window.timeout:
            window.stato = stato
            # Qui non aggiorno la data di ultima modifica perch?? la decisione ?? presa dall'engine: aggiorno solo se la decisione la prende l'utente
            window.save()
    return JsonResponse({'message': "Finestre aggiornate correttamente"})


@csrf_exempt
def get_window(request, device_name, pin):
    if pin == "all":
        windows = Finestra.objects.filter(device_name=device_name)
    else:
        windows = Finestra.objects.filter(device_name=device_name, pin=pin)
        if len(windows) != 1:
            return JsonResponse({'error': "Errore"})
    data = []
    for window in windows:
        data.append({'stato': window.stato, 'timeout': window.timeout, 'pin': window.pin})
    return JsonResponse({'windows': data})


@csrf_exempt
def turn_on_timeout_change_state_button(request, device_name, pin, stato):
    window = Finestra.objects.filter(device_name=device_name, pin=pin)
    if len(window) != 1:
        return JsonResponse({'error': "Errore"}, status=400)
    window = window[0]
    window.stato = stato
    window.ultima_modifica = timezone.now()
    window.timeout = True
    window.save()
    timer = Timer(1800, turn_off_timeout, [window.device_name, window.pin])
    timer.start()
    return JsonResponse({'message': "Cambiato stato correttamente"})


@csrf_exempt
def turn_off_timeout(request, device_name, pin):
    window = Finestra.objects.filter(device_name=device_name, pin=pin)
    if len(window) != 1:
        return JsonResponse({'error': "Errore"}, status=400)
    window = window[0]
    window.timeout = False
    window.save()
    return JsonResponse({'message': "Timeout spento correttamente"})

@csrf_exempt
def add_chat_telegram(request):
    data = json.loads(request.body)
    ser = ChatTelegramSerializer(data=data)
    if ser.is_valid():
        ser.save()
        return JsonResponse({'message': "Chat telegram inserita correttamente"})
    return JsonResponse(ser.errors, status=400)


@csrf_exempt
def get_chats_telegram(request):
    chats = ChatTelegram.objects.all()
    data = {}
    dataChats = []
    for chat in chats:
        ser = ChatTelegramSerializer(instance=chat)
        dataChats.append(ser.data)
    data['chats'] = dataChats
    return JsonResponse(data)

@csrf_exempt
def update_chat(request, chat_id):
    chats = ChatTelegram.objects.filter(chat_id=chat_id)
    if len(chats) != 1:
        return JsonResponse({'error': "Errore"})
    chats[0].ultimo_messaggio = timezone.now()
    chats[0].save()
    return JsonResponse({'message': 'Chat aggiornata correttamente'})


@csrf_exempt
def get_last_changes(request):
    one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
    windows = Finestra.objects.filter(ultima_modifica__gt=one_hour_ago)
    data = {}
    dataFinestre = []
    for window in windows:
        ser = FinestraSerializer(instance=window)
        dataFinestre.append(ser.data)
    data['windows'] = dataFinestre
    return JsonResponse(data)
