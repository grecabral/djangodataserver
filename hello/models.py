# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from hello.choices import * 
import uuid

# Create your models here.
class Jogador(models.Model):
    idade = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(120), MinValueValidator(3)],
    )
    sexo = models.CharField(
        max_length=2,
        choices=SEXO_CHOICES,
        default=NAODEFINIDO,
    )
    localidade = models.CharField(
        max_length=500,
    )
    escola = models.IntegerField(
        choices=ESCOLA_CHOICES,
        default=PUBLICA,
    )

    def __str__(self):
        return "Idade: {0}, Sexo: {1}, Localidade: {2}, Escola: {3}".format(self.idade, self.sexo, self.localidade, self.escola)

    class Meta:
        verbose_name = 'Jogador'
        verbose_name_plural = 'Jogadores'

class Partida(models.Model):
    numero_rodadas = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(120), MinValueValidator(3)],
    )
    ponto_coop = models.IntegerField(
        default=2,
        validators=[MaxValueValidator(120), MinValueValidator(2)],
    )
    ponto_nao_coop = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(120), MinValueValidator(1)],
    )
    dificuldade = models.IntegerField(
        default=FACIL,
        choices=DIFICULDADE_CHOICES,
    )
    estrategia = models.IntegerField(
        default=ALEATORIO,
        choices=ESTRATEGIAS_CHOICES,
    )

    def __str__(self):
        return "Partida {0} -> Estrategia: {1}, Numero de Rodadas: {2}, Dificuldade: {3}, Pontos_COOP: {4}, Pontos_NCOOP: {5}".format(self.id, self.estrategia, self.numero_rodadas, self.dificuldade, self.ponto_coop, self.ponto_nao_coop)

    class Meta:
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'



class Rodada(models.Model):
    id_partida = models.ForeignKey('hello.Partida', on_delete=models.CASCADE)
    rodada = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    pontuacao_jogador1 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    pontuacao_jogador2 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    cooperacao_jogador1 = models.IntegerField(
        default=NAO_COOPEROU,
        choices=COOPERACAO_CHOICES,
    )
    cooperacao_jogador2 = models.IntegerField(
        default=NAO_COOPEROU,
        choices=COOPERACAO_CHOICES,
    )

    def __str__(self):
        return "{0} | Rodada = {1} | {2} x {3} | {4} x {5}".format(self.id_partida, self.rodada, self.pontuacao_jogador1, self.pontuacao_jogador2, self.cooperacao_jogador1, self.cooperacao_jogador2)

    class Meta:
        verbose_name = 'Rodada'
        verbose_name_plural = 'Rodadas'
        
    def canAdd(self):
        count = Rodada.objects.filter(id_partida=self.id_partida).count()
        return count

    def save(self, *args, **kwargs):
        max_rounds = self.id_partida.numero_rodadas
        count = self.canAdd()
        if count < max_rounds:
            self.rodada = count+1
            super(Rodada, self).save(*args, **kwargs)
