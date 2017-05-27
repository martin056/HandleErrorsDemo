# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsyncActionReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('ok', 'ok'), ('failed', 'failed')], default='pending', max_length=7)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('error_traceback', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThirdPartyDataStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
