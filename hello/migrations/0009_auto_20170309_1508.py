# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-09 18:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20170308_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jogador',
            name='ue4guid',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='jogador1',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='jogador2',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='ue4guid',
        ),
        migrations.AddField(
            model_name='partida',
            name='ponto_coop',
            field=models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(2)]),
        ),
        migrations.AddField(
            model_name='partida',
            name='ponto_nao_coop',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(1)]),
        ),
    ]