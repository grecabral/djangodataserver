# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from hello.choices import * 

# Create your models here.
class Jogador(models.Model):    
    id_jogador = models.CharField(
        max_length=200,
    )
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
        return "{0}".format(self.id_jogador)

    class Meta:
        verbose_name = 'Jogador'
        verbose_name_plural = 'Jogadores'

class Partida(models.Model): 
    numero_rodadas = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(120), MinValueValidator(3)],
    )
    dificuldade = models.IntegerField(
        default=FACIL,
        choices=DIFICULDADE_CHOICES,
    )
    quantidade_pontos_cooperacao = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    quantidade_pontos_nao_cooperacao = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    estrategia = models.IntegerField(
        default=ALEATORIO,
        choices=ESTRATEGIAS_CHOICES,
    )
    jogador1 = models.ForeignKey('hello.Jogador', related_name='partida_jogador_1', on_delete=models.CASCADE)
    jogador2 = models.ForeignKey('hello.Jogador', related_name='partida_jogador_2', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{3} x {4}, Estrategia = {0}, Numero de Rodadas = {1}, Dificuldade = {2}".format(self.estrategia, self.numero_rodadas, self.dificuldade, self.jogador1, self.jogador2)

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
        return "Partida = {0} | Rodada = {1} | {6} {2} x {3} {7} | {6} {4} x {5} {7}".format(self.id_partida, self.rodada, self.pontuacao_jogador1, self.pontuacao_jogador2, self.cooperacao_jogador1, self.cooperacao_jogador2, self.id_partida.jogador1, self.id_partida.jogador2)

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
