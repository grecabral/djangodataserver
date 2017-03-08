# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import collections
import uuid

from .models import Jogador, Partida, Rodada

# Create your views here.
def index(request):
    context = {
    }
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', context)

@csrf_exempt
def json_post(request):
    if request.method=='POST':
        print(request.body)
        models_list = json.loads(request.body)
        # received_json_data É um DICT
        od = collections.OrderedDict(sorted(models_list.items()))
        # Ordenando a lista
        for pos, model_item in od.iteritems():
            # Value aqui também é um dict
            # as keys sao as posicoes do array feito no json
            models_type = model_item['model']
            fields = model_item['fields']
            if models_type == "Jogador":
                try:
                    m = Jogador.objects.get(ue4guid=fields['ue4guid'])
                except Jogador.DoesNotExist:
                    m = Jogador(**fields)
                    m.save()
            if models_type == "Partida":
                try:
                    p = Partida.objects.get(ue4guid=fields['ue4guid'])
                except Partida.DoesNotExist:
                    numero_rodadas = fields["numero_rodadas"]
                    dificuldade = fields["dificuldade"]
                    estrategia = fields["estrategia"]
                    j1 = Jogador.objects.get(ue4guid=fields["jogador1"])
                    if fields["jogador2"]:
                        j2 = Jogador.objects.get(ue4guid=fields["jogador2"])
                    else:
                        j2 = None
                    p = Partida(numero_rodadas=numero_rodadas, 
                        dificuldade=dificuldade, 
                        estrategia=estrategia, 
                        jogador1=j1, 
                        jogador2=j2)
                    p.save()
            if models_type == "Rodada":
                try:
                    id_partida = Partida.objects.get(ue4guid=fields["ue4guid_partida"])
                    rodada = fields["rodada"]
                    pontuacao_jogador1 = fields["pontuacao_jogador1"]
                    pontuacao_jogador2 = fields["pontuacao_jogador2"]
                    cooperacao_jogador1 = fields["cooperacao_jogador1"]
                    cooperacao_jogador2 = fields["cooperacao_jogador2"]
                    r = Rodada(id_partida=id_partida, 
                        rodada=rodada, 
                        pontuacao_jogador1=pontuacao_jogador1, 
                        pontuacao_jogador2=pontuacao_jogador2, 
                        cooperacao_jogador1=cooperacao_jogador1, 
                        cooperacao_jogador2=cooperacao_jogador2)
                    r.save()
                except Partida.DoesNotExist:
                    return
        return HttpResponse('JSON RECEIVED')
        # return StreamingHttpResponse('it was post request: '+str(received_json_data))
    return HttpResponse('it was GET request')
