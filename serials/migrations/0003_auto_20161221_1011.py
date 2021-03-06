# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('serials', '0002_episode_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='SerialWatching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serials.Serial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.IntegerField(null=True),
        ),
    ]
