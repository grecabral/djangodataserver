# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
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

from datetime import datetime

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
    now = "{}".format(datetime.now().strftime('%m-%d-%Y--%Hh%Mm%Ss'))
    if request.method == "GET":
        return redirect('/')

    game = request.POST.get('game_select')
    print(game)
    mode = request.POST.get('csv_type')

    if not game:
        game = GAME_FLAG[0]

    if not mode:
        mode = "Jogadores"

    if mode == "Jogadores":
        content = [("ID","Idade", "Sexo", "Localidade", "Escola", "Jogo")]
        players = Jogador.objects.filter(jogo=game)
        for p in players:
            if not p.sexo:
                p.sexo = "M"
            content.append(
                (
                    p.id,
                    p.idade,
                    dict(SEXO_CHOICES)[p.sexo],
                    p.localidade,
                    dict(ESCOLA_CHOICES)[p.escola],
                    dict(GAME_FLAG)[p.jogo]))
    
    elif mode == "Partidas":
        if(game == "Plataforma"):
            content = [("ID","Número de Rodadas", "Pontos por Cooperação", "Pontos por não Cooperação", "Estratégia", "ID do Jogador1", "ID do Jogador2", "Jogo")]
        else:
            content = [("ID","Número de Rodadas", "Pontos por Cooperação", "Pontos por não Cooperação", "Dificuldade", "Estratégia", "ID do Jogador1", "ID do Jogador2", "Jogo")]
        matches = Partida.objects.filter(jogo=game)
        for m in matches:
            try:
                j2_id = m.jogador2.id
            except AttributeError:
                j2_id = "-"

            if(game == "Plataforma"):
                content.append(
                    (
                        m.id,
                        m.numero_rodadas,
                        m.ponto_coop,
                        m.ponto_nao_coop,
                        dict(ESTRATEGIAS_CHOICES)[m.estrategia],
                        m.jogador1.id,
                        j2_id,
                        dict(GAME_FLAG)[m.jogo]))
            else:
                content.append(
                    (
                        m.id,
                        m.numero_rodadas,
                        m.ponto_coop,
                        m.ponto_nao_coop,
                        dict(DIFICULDADE_CHOICES)[m.dificuldade],
                        dict(ESTRATEGIAS_CHOICES)[m.estrategia],
                        m.jogador1.id,
                        j2_id,
                        dict(GAME_FLAG)[m.jogo]))
    
    elif mode == "Rodadas":
        content = [("ID", "Número da Rodada", "Pontuação do Jogador1", "Pontuação do Jogador2", "Cooperação do Jogador1", "Cooperação do Jogador2", "Jogo")]
        rounds = Rodada.objects.filter(jogo=game)
        for r in rounds:
            content.append(
                (
                    r.id, r.rodada,
                    r.pontuacao_jogador1,
                    r.pontuacao_jogador2,
                    dict(COOPERACAO_CHOICES)[r.cooperacao_jogador1],
                    dict(COOPERACAO_CHOICES)[r.cooperacao_jogador2],
                    dict(GAME_FLAG)[r.jogo]))

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, encoding='utf-8')
    response = StreamingHttpResponse((writer.writerow(row) for row in content), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{}--{}--{}.csv"'.format(dict(GAME_FLAG)[int(game)], mode, now)
    return response

def index(request):
    context = {
        "gameFlag": GAME_FLAG,
    }
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html', context)

@csrf_exempt
def json_post(request):
    if request.method=='POST':
        print("{}\n".format(request.body))
        ue4guid = request.META['HTTP_UE4GUID']
        print("{}\n".format(ue4guid))
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
            print("Not A JSON\n{}\n".format(request.body))
            return HttpResponse('NOT A JSON')
        return HttpResponse('{}'.format(ue4guid))
    return HttpResponse('it was GET request')
