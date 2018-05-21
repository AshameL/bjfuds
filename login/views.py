#! python3
# coding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .forms import *
import hashlib
from .auth.auth import authenticate

def login(request):
	if request.method == 'POST': # 当表单提交的时候
		form = LoginForm(request.POST)
		if form.is_valid():
			u = form.cleaned_data['username']
			p = form.cleaned_data['password']
			p_md5 = hashlib.md5(p.encode(encoding='utf-8')).hexdigest()

			# 下面进行数据校验
			typeNum,loginName = authenticate(request,u,p_md5)
			print(loginName)
			if typeNum == -1:
				return render(request,'login.html',{'errorMessages':loginName})
			elif typeNum == 0:
				return redirect('/teacherindex/')
			else :
				return redirect('/index/')

	return render(request, 'login.html')
