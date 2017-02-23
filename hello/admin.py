from django.contrib import admin

# Register your models here.
from .models import Jogador, Partida, Rodada

# Register your models here.
admin.site.register(Jogador)
admin.site.register(Partida)
admin.site.register(Rodada)
