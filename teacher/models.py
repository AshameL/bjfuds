# coding:utf-8
from django.db import models

from student.models import *


# Create your models here.

# 公告表
class Announcement(models.Model):
    briefTitle = models.CharField(max_length=64)  # 标题
    briefContent = models.CharField(max_length=1024)  # 内容
    briefReleaseTime = models.DateTimeField(auto_now=True)  # 时间类型，看在数据库中怎样保存### 时区是这样的吗
    briefType = models.CharField(max_length=16)  # 资源公告，作业公告，其他公告，等等


# 上传资料表 参考资料
class ReferenceFile(models.Model):
    filename = models.CharField(max_length=32)  # 文件名
    uploadtime = models.DateTimeField(auto_now_add=True)  # 上传时间
    remark = models.CharField(max_length=64, null=True, blank=True)  # 备注
    path = models.CharField(max_length=128)
    suffix = models.CharField(max_length=12, null=True)  # 文件后缀名
    visible = models.CharField(max_length=12, null=True)
    chapter = models.ForeignKey(Chapter, null=True, blank=True)  # 章节可以为空，标识范围不限制


# 错题表
# 错题表 记录错题的错选项
class ErrorQue(models.Model):
    testid = models.ForeignKey(Questionitem)
    correct = models.CharField(max_length=4)
    erroranswer = models.CharField(max_length=4)
    count = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

# 题目正误率
class QueAccurancy(models.Model):
    id = models.ForeignKey(Questionitem, primary_key=True)
    correctCount = models.IntegerField(default=0)
    wrongCount = models.IntegerField(default=0)
