# -*- coding: utf-8 -*-
# Opções de Sexo
MASCULINO = 'M'
FEMININO = 'F'
SEXO_CHOICES = (
    (MASCULINO, 'Masculino'),
    (FEMININO, 'Feminino'),
)

# Opções de escola
PUBLICA = 0
PRIVADA = 1
ESCOLA_CHOICES = (
    (PUBLICA, 'Pública'),
    (PRIVADA, 'Privada'),
)

# Opções de dificuldade
FACIL = 0
MEDIO = 1
DIFICIL = 2
DIFICULDADE_CHOICES = (
    (FACIL, 'Fácil'),
    (MEDIO, 'Médio'),
    (DIFICIL, 'Difícil'),
)

# Opções de estratégias
SEMPRE_COOPERA = 0
NUNCA_COOPERA = 1
COOPERA_REPETE_ULTIMA = 2
COOPERA_REPETE_ULTIMA_DUAS_RODADAS = 3
ALEATORIO = 4
MULTIPLAYER = 5
ESTRATEGIAS_CHOICES = (
    (SEMPRE_COOPERA, 'Sempre Coopera'),
    (NUNCA_COOPERA, 'Nunca Coopera'),
    (COOPERA_REPETE_ULTIMA, 'Coopera e repete a última jogada'),
    (COOPERA_REPETE_ULTIMA_DUAS_RODADAS, 'Coopera e repete a última jogada, duas rodadas seguidas para não cooperar'),
    (ALEATORIO, 'Aleatório'),
    (MULTIPLAYER, 'Multiplayer'),
)

# Opções de Cooperação
NAO_COOPEROU = 0
COOPEROU = 1
NEUTRO = 2
COOPERACAO_CHOICES = (
    (NAO_COOPEROU, 'Cooperou'),
    (COOPEROU, 'Não Cooperou'),
    (NEUTRO, 'Jogada Neutra'),
)

# Opções de Jogos
PLATAFORMA = 0
ESTILINGUE = 1
GAME_FLAG = (
    (PLATAFORMA, 'Plataforma'),
    (ESTILINGUE, 'Slingshot Challenge'),
)