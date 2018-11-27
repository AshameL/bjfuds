#coding:utf-8

from django.shortcuts import render, redirect


def login_Check(func):
    def inner(request, *args, **kwargs):
        v = request.session.get('name')
        if not v:
            return redirect('/')
        else:
            re = func(request, *args, **kwargs)
            return re
    return inner


def isNeedRelogin(func):
    def inner(request, *args, **kwargs):
        v = request.session.get('type')
        print(v)
        if not v:
            re = func(request, *args, **kwargs)
            return re
        elif v == '0': # 老师
            return redirect('/teacherindex')
        else:
            return redirect('/questiontest')
    return inner
