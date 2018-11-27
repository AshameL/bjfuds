#! python3
# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .forms import *
import hashlib
from .auth.auth import authenticate
from .auth.incepter import login_Check, isNeedRelogin
from .models import User


@isNeedRelogin
def login(request):
    if request.method == 'POST':  # 当表单提交的时候
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            p_md5 = hashlib.md5(p.encode(encoding='utf-8')).hexdigest()

            # 下面进行数据校验
            typeNum, loginName = authenticate(request, u, p_md5)
            if typeNum == -1:
                return render(request, 'login.html', {'errorMessages': loginName})
            elif typeNum == 0:
                return redirect('/teacherindex')
            else:
                return redirect('/questiontest/')

    return render(request, 'login.html')


def logout(request):
    del request.session["username"]  # 删除session
    del request.session["name"]
    del request.session["type"]
    print(request.session)
    return redirect('/')


@login_Check
def editpassword(request):
    if request.method == 'POST':
        username = request.session["username"]
        print(request.POST)
        oldpassword = request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        newpassword2 = request.POST['newpassword2']
        oldpassword_md5 = hashlib.md5(oldpassword.encode(encoding='utf-8')).hexdigest()
        p_md5 = hashlib.md5(newpassword.encode(encoding='utf-8')).hexdigest()
        user = User.objects.get(username=username)
        if oldpassword_md5 != user.password:
            errormessage = "原密码输入错误!"
            return edit_return(request, errormessage)
        if newpassword != newpassword2:
            errormessage = "两次密码不一致!"
            return edit_return(request, errormessage)
        user.password = p_md5
        user.save()
        return edit_return(request, "密码修改成功！")
    return edit_return(request, "")


def edit_return(request, errormessage):
    if request.session["type"] == 0:
        return render(request, 'teacher/t_index.html', {"errormessage": errormessage})
    else:
        return render(request, 'student/editpassword.html', {"errormessage": errormessage})
