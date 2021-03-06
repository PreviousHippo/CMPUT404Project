# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('github', models.CharField(max_length=255)),
                ('avatar', models.ImageField(upload_to='/avatars/')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('friend_requests', models.ManyToManyField(related_name='_author_friend_requests_+', to='socialnet.Author')),
                ('friends', models.ManyToManyField(related_name='_author_friends_+', to='socialnet.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('published_date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnet.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateField(auto_now_add=True)),
                ('text', models.CharField(max_length=255)),
                ('public', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnet.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnet.Post'),
        ),
    ]
