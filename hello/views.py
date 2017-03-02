# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import collections

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
        models_list = json.loads(request.body)
        # received_json_data É um DICT
        od = collections.OrderedDict(sorted(models_list.items()))
        # Ordenando a lista

        jogadores = []
        partida = None
        for pos, model_item in od.iteritems():
            # Value aqui também é um dict
            # as keys sao as posicoes do array feito no json
            models_type = model_item['model']
            fields = model_item['fields']
            if models_type == "Jogador":
                try:
                    m = Jogador.objects.get(id_jogador=fields['id_jogador'])
                except Jogador.DoesNotExist:
                    m = Jogador(**fields)
                    m.save()
                jogadores.append(m)
            if models_type == "Partida":
                numero_rodadas = fields["numero_rodadas"]
                dificuldade = fields["dificuldade"]
                quantidade_pontos_cooperacao = fields["quantidade_pontos_cooperacao"]
                quantidade_pontos_nao_cooperacao = fields["quantidade_pontos_nao_cooperacao"]
                estrategia = fields["estrategia"]
                jogador1 = jogadores[0]
                if jogadores.count == 2:
                    jogador2 = jogadores[1]
                else:
                    jogador2 = None
                p = Partida(numero_rodadas=numero_rodadas, 
                    dificuldade=dificuldade, 
                    quantidade_pontos_cooperacao=quantidade_pontos_cooperacao, 
                    quantidade_pontos_nao_cooperacao=quantidade_pontos_nao_cooperacao, 
                    estrategia=estrategia, 
                    jogador1=jogador1, 
                    jogador2=jogador2)
                partida = p
                p.save()
            if models_type == "Rodada":
                id_partida = partida
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
        return HttpResponse('JSON RECEIVED')
        # return StreamingHttpResponse('it was post request: '+str(received_json_data))
    return HttpResponse('it was GET request')
