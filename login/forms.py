#coding:utf-8
from django import forms

#登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password',widget=forms.PasswordInput)