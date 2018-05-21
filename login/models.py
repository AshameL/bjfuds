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
    isActive = models.BooleanField() # 是否可用
    type = models.IntegerField() # type：0老师，1学生，2外校人员