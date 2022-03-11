from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from houses.forms import *

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/houses/")

def register_page(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "register_page.html", {'form': form, 'error': None})
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if len(password) < 3:
                return render(request, "register_page.html", {'form': form, 'error': 'Password troppo corta'})
            user = User.objects.filter(username=username)
            if len(user) != 0:
                return render(request, "register_page.html", {'form': form, 'error': 'Esiste già un account con questo username'})
            user = User.objects.create(username=username, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect("/houses/")
        return render(request, "register_page.html", {'form': form, 'error': 'Dati non validi'})
