from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "houses"
urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('window/<int:finestra_id>', views.turn_on_timeout_change_state_web, name="turn_on_timeout_change_state_web"),
    path('new_data/', views.new_data, name="new_data"),
    path('update_windows/', views.update_all_windows, name="update_all_windows"),
    path('window/<slug:device_name>/<slug:pin>/', views.get_window, name="get_window"),
    path('window/<slug:device_name>/<slug:pin>/<slug:stato>/', views.turn_on_timeout_change_state_button, name="turn_on_timeout_change_state_button"),
    path('window/turnoff/<slug:device_name>/<slug:pin>/', views.turn_off_timeout, name="turn_off_timeout"),
]
