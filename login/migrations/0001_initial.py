# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-19 03:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=32)),
                ('isActive', models.BooleanField()),
                ('type', models.IntegerField()),
                ('myClass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.Classes')),
            ],
        ),
    ]