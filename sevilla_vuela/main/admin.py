from django.contrib import admin
from .models import Salida, Llegada, Aerolinea, Salida_comp, Llegada_comp

admin.site.register(Salida)
admin.site.register(Llegada)
admin.site.register(Aerolinea)
admin.site.register(Llegada_comp)
admin.site.register(Salida_comp)