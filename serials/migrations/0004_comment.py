# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serials', '0003_auto_20161221_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=500)),
            ],
        ),
    ]
