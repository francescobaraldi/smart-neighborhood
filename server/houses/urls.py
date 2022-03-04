from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "houses"
urlpatterns = [
    path('new_data/', views.new_data, name="new_data"),
]
