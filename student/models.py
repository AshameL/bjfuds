# coding=utf-8
from django.db import models
from login.models import User


# Create your models here.

class Chapter(models.Model):
    chaptername = models.CharField(max_length=50)
    chapterdescription = models.CharField(max_length=500, null=True, blank=True)


class Subchapter(models.Model):
    chapterid = models.ForeignKey(Chapter)
    subchaptername = models.CharField(max_length=50)


class Questionitem(models.Model):
    question = models.CharField(max_length=5000)
    A = models.CharField(max_length=1000, null=True, blank=True)
    B = models.CharField(max_length=1000, null=True, blank=True)
    C = models.CharField(max_length=1000, null=True, blank=True)
    D = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=4)
    difficulty = models.IntegerField(default=1)
    quiztime = models.CharField(max_length=20)
    visiable = models.CharField(max_length=2, default='1')  # 题目可见 1可见 0不可见
    courseid = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    frequency = models.FloatField(default=0)
    avetime = models.FloatField(default=0)
    uploader = models.IntegerField(default=1)
    subchapterid = models.ForeignKey(Subchapter)
    question_nature = models.IntegerField(default=0)
    question_resolution = models.CharField(max_length=5000)
    html = models.CharField(max_length=5000, null=True, blank=True)


# 成绩单
# 成绩单
class Grade(models.Model):
    userid = models.ForeignKey(User)
    subchapter = models.ForeignKey(Subchapter)  # 知识点，或者章节号
    accurancy = models.FloatField()
    questionlist = models.CharField(max_length=1000, null=True, blank=True)  # 题目的idlist
    answerlist = models.CharField(max_length=1000, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
