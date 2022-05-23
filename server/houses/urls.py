from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "houses"
urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('window/changed/', views.get_last_changes, name='get_last_changes'),
    path('window/<int:finestra_id>/', views.turn_on_timeout_change_state_web, name="turn_on_timeout_change_state_web"),
    path('data/', views.new_data, name="new_data"),
    path('window/all/<slug:stato>/', views.change_state_all_windows, name="change_state_all_windows"),
    path('window/<slug:device_name>/<slug:pin>/', views.get_window, name="get_window"),
    path('window/turnoff/<slug:device_name>/<slug:pin>/', views.turn_off_timeout, name="turn_off_timeout"),
    path('window/<slug:device_name>/<slug:pin>/<slug:stato>/', views.turn_on_timeout_change_state_button, name="turn_on_timeout_change_state_button"),
    path('chat/add/', views.add_chat_telegram, name="add_chat_telegram"),
    path('chat/all/', views.get_chats_telegram, name="get_chats_telegram"),
    path('chat/update/<slug:chat_id>/', views.update_chat, name="update_chat"),
]
