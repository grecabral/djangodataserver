# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import collections
import uuid

import unicodecsv as csv
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from hello.choices import * 


from .models import Jogador, Partida, Rodada

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def generate_csv(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    mode = "Jogadores"
    # mode = "Partidas"
    # mode = "Rodadas"
    if mode == "Jogadores":
        content = [("Idade", "Sexo", "Localidade", "Escola", "Jogo")]
        players = Jogador.objects.all()
        for p in players:
            content.append((p.idade, dict(SEXO_CHOICES)[p.sexo], p.localidade, dict(ESCOLA_CHOICES)[p.escola], dict(GAME_FLAG)[p.jogo]))
    
    elif mode == "Partidas":
        content = [("Idade", "Sexo", "Localidade", "Escola", "Jogo")]
        players = Jogador.objects.all()
        for p in players:
            content.append((p.idade, dict(SEXO_CHOICES)[p.sexo], p.localidade, dict(ESCOLA_CHOICES)[p.escola], dict(GAME_FLAG)[p.jogo]))
   
    else:
        content = [("Idade", "Sexo", "Localidade", "Escola", "Jogo")]
        players = Jogador.objects.all()
        for p in players:
            content.append((p.idade, dict(SEXO_CHOICES)[p.sexo], p.localidade, dict(ESCOLA_CHOICES)[p.escola], dict(GAME_FLAG)[p.jogo]))

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, encoding='utf-8')
    response = StreamingHttpResponse((writer.writerow(row) for row in content), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

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
            gameFlag = models_list['gameFlag']
            jogadores = models_list['players']
            j1 = None
            j2 = None
            for item in jogadores:
                m = Jogador(
                    idade=item["age"],
                    sexo=item["sex"],
                    localidade=item["locality"],
                    escola=item["school"],
                    jogo=gameFlag
                    )
                m.save()
                if j1:
                    j2 = m
                else:
                    j1 = m
            p = Partida(
                numero_rodadas=models_list["number_of_rounds"],
                ponto_coop=models_list["coop_points"], 
                ponto_nao_coop=models_list["no_coop_points"], 
                dificuldade=models_list["difficulty"], 
                estrategia=models_list["strategy"],
                jogador1=j1,
                jogador2=j2,
                jogo=gameFlag
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
                    cooperacao_jogador2=item['player2Coop'],
                    jogo=gameFlag
                    )
                r.save()
        except ValueError:
            print("{}\n".format(request.body))
            return HttpResponse('NOT A JSON')
        return HttpResponse('JSON RECEIVED')
    return HttpResponse('it was GET request')
