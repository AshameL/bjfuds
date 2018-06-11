"""bjfuds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from login import views as login_views
from student import views as s_view
from teacher import views as t_view

urlpatterns = [

    url(r'^$', login_views.login),
    ###################学生功能#########################
    url(r'^index/$',s_view.index,name='index'),
    url(r'^questiontest$',s_view.questiontest,name='questiontest'),
    url(r'^exam/(\d+)/',s_view.exam,name='exam'),
    url(r'^calucate',s_view.calculationGrade,name = 'calculate'),
    ###################教师功能#########################
    url(r'^teacherindex$',t_view.index,name='tearhcer'),
    # admin
    url(r'^admin/', admin.site.urls),
    # 测试用
    url(r'^base/',s_view.base,name='base'),
]
