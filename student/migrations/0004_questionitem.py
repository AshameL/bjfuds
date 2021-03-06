# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-03 03:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_delete_questionitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='questionitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=5000)),
                ('A', models.CharField(blank=True, max_length=1000, null=True)),
                ('B', models.CharField(blank=True, max_length=1000, null=True)),
                ('C', models.CharField(blank=True, max_length=1000, null=True)),
                ('D', models.CharField(blank=True, max_length=1000, null=True)),
                ('answer', models.CharField(max_length=4)),
                ('difficulty', models.IntegerField(default=1)),
                ('quiztime', models.CharField(max_length=20)),
                ('accuracy', models.FloatField(default=0)),
                ('uploader', models.IntegerField(default=1)),
                ('questionNature', models.IntegerField(default=0)),
                ('questionResolution', models.CharField(max_length=5000)),
                ('html', models.CharField(blank=True, max_length=5000, null=True)),
                ('subchapterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.subchapter')),
            ],
        ),
    ]
