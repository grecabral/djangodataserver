# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-08 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_remove_rodada_ue4guid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jogador',
            old_name='UE4GUID',
            new_name='ue4guid',
        ),
        migrations.RenameField(
            model_name='partida',
            old_name='UE4GUID',
            new_name='ue4guid',
        ),
    ]
