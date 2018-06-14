# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-03 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20180603_0353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionitem',
            old_name='questionNature',
            new_name='question_nature',
        ),
        migrations.RenameField(
            model_name='questionitem',
            old_name='questionResolution',
            new_name='question_resolution',
        ),
        migrations.AddField(
            model_name='questionitem',
            name='avetime',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='questionitem',
            name='chapterid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionitem',
            name='courseid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionitem',
            name='frequency',
            field=models.FloatField(default=0),
        ),
    ]