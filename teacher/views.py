from django.shortcuts import render
from  teacher.forms import *
from  teacher.util_tool import *
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from login.models import *
from student.models import *
from teacher.models import *
from django.http import *
import os
# Create your views here.


# 教师主页
def teacher(request):
    # 查询数据库
    user = User.objects.count()
    print(user)
    student = User.objects.filter(type=1).count()
    test = Questionitem.objects.count()
    grade = Grade.objects.all()[:10]
    return render(request, 'teacher/t_index.html',
                  {'user': user, 'student': student, 'grade': grade,
                   'test': test})


# 学生账号管理
# 上传学生名单
def manage(request):
    re_list = []
    if request.method == 'POST':
        form = TestingUpload(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['filename']
            # 上传文件并解析
            re_list = handle_uploaded_xls_student(f)
            # 为表单获取数据
    user = User.objects.all()
    return render(request, 'teacher/t_manage.html', {"user": user, "re_list": re_list})


# 上传资料 referenceFile
def upload_file(request):
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['filename']
            myremark = form.cleaned_data['remark']
            visible = form.cleaned_data['visibleRange']
            # 上传文件
            filenamepath = handle_uploaded_file(f, 'reference')  # 这里处理一下，只进行上传
            # 保存到数据库
            # ##文件路径
            path = f.name
            curTime = getCurrentTime('%Y-%m-%d %H:%M:%S')
            suffix = path.split('.')[-1]
            r = ReferenceFile(filename=path, remark=myremark, path=filenamepath, suffix=suffix, visible=visible)
            r.save()
            # 这里发出上传文件的公告
            a = Announcement(briefTitle='【新资料上传】', briefContent=f.name + '已经上传，请同学们及时查看并下载！', briefType='资源公告',
                             briefClass='校内')
            a.save()
            print('upload file success')
        else:
            return HttpResponse('Upload Error')

    referencefile = ReferenceFile.objects.all().order_by('-uploadtime')
    return render(request, 'teacher/t_file.html', {'referencefile': referencefile})


# 上传试题
def upload_test(request):
    # 上传试题时
    if request.method == 'POST':
        my_form = TestingUpload(request.POST, request.FILES)
        if my_form.is_valid():
            f = my_form.cleaned_data['filename']
            # 上传文件 验证是不是doc或者docx结尾
            ##########################################
            dox = f.name.split('.')[-1]
            if dox.lower() in ['doc', 'docx']:  # html直接处理
                # 处理上传word的具体逻辑
                filename = handle_uploaded_file(f, 'media')
                print(filename)
                # 识别html并写入数据库
                regexHTMLandWriteDB(filename, 'border=1')
                # 删除原来 html
                os.remove(filename)
            else:
                # 返回错误页面
                return HttpResponse('上传word后缀名错误')
                # #########【继续添加】然后跳转到直接处理html
                # 保存为html文件，但这里的顺序是不是优化下
                # saveAsHTML(f.name)
        # 这里的return 再考虑下
        return redirect('/tea_question/')
    # 访问网页时
    else:
        my_form = TestingUpload()
    # 返回表格内容
    testing = Questionitem.objects.all()
    return render(request, 'teacher/t_question.html', {'form': my_form, 'testing': testing})


# 教师修改密码
def changepassword(request):
    return render(request, 'teacher/t_changepassword.html')


# 编辑试题
def test_edit(request, tid):
    info = Questionitem.objects.get(id=tid)
    if request.method == 'POST':
        my_form = EditTest(request.POST)
        if my_form.is_valid():
            info.content = my_form.cleaned_data['content']
            info.A = my_form.cleaned_data['A']
            info.B = my_form.cleaned_data['B']
            info.C = my_form.cleaned_data['C']
            info.D = my_form.cleaned_data['D']
            info.difficult = my_form.cleaned_data['difficult']
            info.answer = my_form.cleaned_data['answer']
            info.chapter = my_form.cleaned_data['chapter']
            info.knowledge = my_form.cleaned_data['knowledge']
            info.save()

    return render(request, 'teacher/t_que_edit.html', {'info': info})


# 删除试题
def test_delete(request, tid):
    models.TestQuestion.objects.get(id=tid).delete()
    # 重定向返回本页面
    return HttpResponseRedirect('/tea_question/')


# 查看试题
def test_view(request, tid):
    info = Questionitem.objects.get(id=tid)
    return render(request, 'teacher/t_que_view.html', {'info': info})


# 查看成绩
def grades(request):
    gradelist = Grade.objects.order_by('-time')

    return render(request, 'teacher/t_grades.html', {'gradelist': gradelist})


def gradedetails(request, tid):
    grade = Grade.objects.get(id=tid)
    errorque = ErrorQue.objects.filter(gradeid=tid)
    return render(request, 'teacher/t_gradedetails.html', {'grade': grade, 'error': errorque})


# 教师声明主页
'''
def tea_annou(request):
    from student import models
    if request.method == 'POST':
        form = Announcement(request.POST)
        if form.is_valid():
            briefTitle = form.cleaned_data['briefTitle']
            briefContent = form.cleaned_data['briefContent']
            briefClass = form.cleaned_data['briefClass']
            briefType = form.cleaned_data['briefType']
            info = models.Announcement()
            info.briefTitle = briefTitle
            info.briefContent = briefContent
            for i in briefClass:
                info.briefClass += i + ','
                print(i)
            # info.briefClass = briefClass
            info.briefType = briefType
            info.save()
        else:
            print(request.POST.getlist('briefClass'))
        return redirect('/tea_ann/')
    else:
        form = Announcement()
        classes = Classes.objects.order_by('-id')
        announ = models.Announcement.objects.order_by('-briefReleaseTime')
        return render(request, 'teacher/t_annou.html', {'announ': announ, 'classes': classes, 'form': form})


# 修改公告
def tea_ann_edit(request, tid):
    from student.models import Announcement
    info = Announcement.objects.get(id=tid)
    return render(request, 'teacher/t_ann_edit.html', {'info': info})


# 删除公告
def tea_ann_delete(request, tid):
    from student.models import Announcement
    Announcement.objects.get(id=tid).delete()
    return redirect('/tea_ann/')
'''
