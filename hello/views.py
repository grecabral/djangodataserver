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
        print("{}\n".format(request.body))
        try:
            models_list = json.loads(request.body)
            jogadores = models_list['players']
            for item in jogadores:
                m = Jogador(
                    idade=item["age"],
                    sexo=item["sex"],
                    localidade=item["locality"],
                    escola=item["school"],
                    )
                m.save()

            p = Partida(
                numero_rodadas=models_list["number_of_rounds"],
                ponto_coop=models_list["coop_points"], 
                ponto_nao_coop=models_list["no_coop_points"], 
                dificuldade=models_list["difficulty"], 
                estrategia=models_list["strategy"]
                )
            p.save()

            rodadas = models_list["rounds"]
            for item in rodadas:
                r = Rodada(
                    id_partida=p, 
                    rodada=item['round'], 
                    pontuacao_jogador1=item['player1Score'], 
                    pontuacao_jogador2=item['player2Score'], 
                    cooperacao_jogador1=item['player1Coop'], 
                    cooperacao_jogador2=item['player2Coop']
                    )
                r.save()
        except ValueError:
            print("{}\n".format(request.body))
            return HttpResponse('NOT A JSON')
        return HttpResponse('JSON RECEIVED')
    return HttpResponse('it was GET request')
