# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0017_auto_20161120_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pubdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]