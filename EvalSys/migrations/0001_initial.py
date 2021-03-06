# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-16 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Qualia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(max_length=50)),
                ('qualevalue', models.CharField(max_length=500)),
                ('post', models.BooleanField(default=False)),
                ('qualename', models.CharField(default='Telic', max_length=20)),
                ('sb_annotations', models.BooleanField(default=False)),
                ('cb_annotations', models.BooleanField(default=False)),
            ],
        ),
    ]
