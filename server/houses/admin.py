from django.contrib import admin
from .models import *

# Register your models here.

class FinestraInline(admin.StackedInline):
    model = Finestra
    extra = 2

class CasaAdmin(admin.ModelAdmin):
    inlines = [FinestraInline]
    
admin.site.register(Casa, CasaAdmin)
