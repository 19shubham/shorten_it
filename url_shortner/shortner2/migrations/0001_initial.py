# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-02 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import shortner2.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SjURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=220, unique=True, validators=[shortner2.validators.validate_url, shortner2.validators.validate_dot_com])),
                ('shortcode', models.CharField(blank=True, default='abcdef', max_length=15, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.BooleanField(default=True)),
            ],
        ),
    ]
