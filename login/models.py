# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# 班级表
class Classes(models.Model):
    classname = models.CharField(max_length=32, unique=True)


# 用户表
class User(models.Model):
    username = models.CharField(max_length=16, unique=True)  # 用户表 学号
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)  # 用户名【主键】，密码 默认值：（data0structure1）
    myClass = models.ForeignKey(Classes, null=True)
    state = models.IntegerField(default=0)  # -1锁定 0离线 1在线
    type = models.IntegerField(default=1)  # type：0老师，1学生，2外校人员
    lastlogin = models.DateTimeField(blank=True, null=True)  # 最近登录时间


# 日活
class dateActivity(models.Model):
    user = models.ForeignKey(User)
    logintime = models.DateTimeField(auto_now=True)
    logouttime = models.DateTimeField(auto_now=True, blank=True, null=True)
