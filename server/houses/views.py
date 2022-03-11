from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import *
import json
import datetime
from django.utils import timezone
import sys
from django.conf import settings
import sys
sys.path.append(settings.ROOT_PROJECT)
from engine import engine


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
            engine.process_data(data)
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
