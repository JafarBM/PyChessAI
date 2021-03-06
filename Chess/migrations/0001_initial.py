# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=20)),
                ('password', models.CharField(default='', max_length=20)),
                ('email', models.EmailField(default='', max_length=254)),
                ('activation_key', models.IntegerField(default=1234)),
                ('activation_status', models.IntegerField(default=0)),
            ],
        ),
    ]
