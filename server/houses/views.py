from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
# from .serializers import *
import json

@csrf_exempt
def new_data(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse(data)
