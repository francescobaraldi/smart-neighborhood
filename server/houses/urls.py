from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "houses"
urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('aggiorna_finestra/<int:finestra_id>', views.aggiorna_finestra, name="aggiorna_finestra"),
    path('new_data/', views.new_data, name="new_data"),
    path('update_windows/', views.update_windows, name="update_windows"),
]
