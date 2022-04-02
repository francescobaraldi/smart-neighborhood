from rest_framework import serializers
from .models import *

class DatiAmbientaliSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatiAmbientali
        fields = ['potentiometer_value', 'photoresistor_value', 'thermometer_value']

class ChatTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatTelegram
        fields = ['chat_id']
