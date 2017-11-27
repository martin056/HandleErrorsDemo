# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-27 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
            name='InvoicesPlusCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ThirdPartyDataStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='invoicespluscustomer',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices_plus_customers', to='demo.Organisation'),
        ),
        migrations.AddField(
            model_name='invoicespluscustomer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices_plus_customers', to='demo.User'),
        ),
        migrations.AlterUniqueTogether(
            name='invoicespluscustomer',
            unique_together=set([('organisation', 'member_id')]),
        ),
    ]
