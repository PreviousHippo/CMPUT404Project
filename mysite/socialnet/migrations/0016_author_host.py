# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0015_auto_20161117_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='host',
            field=models.URLField(default='http://127.0.0.1:8000'),
        ),
    ]