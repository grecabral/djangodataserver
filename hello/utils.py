# -*- coding: utf-8 -*-

from hello.models import *

def getStatistics(jogo):
    rounds = Rodada.objects.filter(jogo=jogo)
    my_dict = {}

    coop = 0
    no_coop = 0

    for item in rounds:
        print(item)

    return my_dict

def getStatistics(partida):
    rounds = Rodada.objects.filter(id_partida=partida)
    my_dict = {}
    coop_player1 = 0 
    coop_player2 = 0 
    no_coop_player1 = 0 
    no_coop_player2 = 0 
    for item in rounds:
        if item.cooperacao_jogador1:
            coop_player1 += item.pontuacao_jogador1
        else:
            no_coop_player1 += item.pontuacao_jogador1
        if item.cooperacao_jogador2:
            coop_player2 += item.pontuacao_jogador2
        else:
            no_coop_player2 += item.pontuacao_jogador2
    
    total_player1 = coop_player1 + no_coop_player1
    coop_rate_player1 = coop_player1 / total_player1
    no_coop_rate_player1 = 1 - coop_rate_player1

    total_player2 = coop_player2 + no_coop_player2
    coop_rate_player2 = coop_player2 / total_player2
    no_coop_rate_player2 = 1 - coop_rate_player2

    total_coop = coop_player1 + coop_player2
    total_no_coop = no_coop_player1 + no_coop_player2
    total_coop_rate = total_coop / (total_no_coop + total_coop)
    total_no_coop_rate = 1 - total_coop_rate

    my_dict["total_player1"] = total_player1
    my_dict["coop_player1"] = coop_player1
    my_dict["no_coop_player1"] = no_coop_player1
    my_dict["coop_rate_player1"] = coop_rate_player1
    my_dict["no_coop_rate_player1"] = no_coop_rate_player1

    my_dict["total_player2"] = total_player2
    my_dict["coop_player2"] = coop_player2
    my_dict["no_coop_player2"] = no_coop_player2
    my_dict["coop_rate_player2"] = coop_rate_player2
    my_dict["no_coop_rate_player2"] = no_coop_rate_player2

    my_dict["total_coop"] = total_coop
    my_dict["total_no_coop"] = total_no_coop
    my_dict["total_coop_rate"] = total_coop_rate
    my_dict["total_no_coop_rate"] = total_no_coop_rate

    return my_dict
