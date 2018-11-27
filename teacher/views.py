#coding:utf-8
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
from login.auth.incepter import login_Check


# Create your views here.


# 教师主页
@login_Check
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
@login_Check
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
@login_Check
def upload_file(request):
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['filename']
            myremark = form.cleaned_data['remark']
            #visible = form.cleaned_data['visibleRange']
            # 上传文件
            filenamepath = handle_uploaded_file(f, 'reference')  # 这里处理一下，只进行上传
            # 保存到数据库
            # ##文件路径
            path = f.name
            suffix = path.split('.')[-1]
            r = ReferenceFile(filename=path, remark=myremark, path=filenamepath, suffix=suffix)
            r.save()
            # 【功能暂时关闭】这里发出上传文件的公告
            # a = Announcement(briefTitle='【新资料上传】', briefContent=f.name + '已经上传，请同学们及时查看并下载！',
            #                briefType='资源公告', )
            #
            # a.save()
        else:

            return HttpResponse('500！！')

    referencefile = ReferenceFile.objects.all().order_by('-uploadtime')
    return render(request, 'teacher/t_file.html', {'referencefile': referencefile})

@login_Check
def delete_file(request, tid):
    # 删除文件存储位置
    info = ReferenceFile.objects.get(id=tid)
    # filedir = os.path.dirname(__file__)
    # filedir = filedir.replace('\\', '/')  ## 这里会不会有问题。。。
    path = info.path
    os.remove(path)
    # 删除数据库
    ReferenceFile.objects.get(id=tid).delete()
    return redirect('/tea_file/')

@login_Check
# 上传试题【有bug！！！8-25调试中】
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

@login_Check
# 教师修改密码
def changepassword(request):
    return render(request, 'teacher/t_changepassword.html')

@login_Check
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
            # info.save() # 为安全起见、暂时注销

    return render(request, 'teacher/t_que_edit.html', {'info': info})


# 删除试题
@login_Check
def test_delete(request, tid):
    models.TestQuestion.objects.get(id=tid).delete()
    # 重定向返回本页面
    return HttpResponseRedirect('/tea_question/')


# 查看试题
@login_Check
def test_view(request, tid):
    info = Questionitem.objects.get(id=tid)
    dictChoice = {'A': 0, 'B': 0, 'C': 0, 'D': 0, '': 0}
    for i in dictChoice:
        try:
            dictChoice[i] = ErrorQue.objects.get(erroranswer=i, testid_id=info.id).count
        except:
            pass
    dictChoice['lost'] = dictChoice.pop('')
    try:
        dictChoice[info.answer] = QueAccurancy.objects.get(id_id=info.id).correctCount
    except:
        pass
    return render(request, 'teacher/t_que_view.html', {'info': info, 'dictChoice': dictChoice})


# 查看成绩
@login_Check
def grades(request):
    gradelist = Grade.objects.order_by('-time')

    return render(request, 'teacher/t_grades.html', {'gradelist': gradelist})

@login_Check
def gradedetails(request, tid):
    myGrade = Grade.objects.get(id=tid)
    # errorque = ErrorQue.objects.filter(gradeid=tid)
    queList = []
    idlist = myGrade.questionlist[1:-1].split(',')
    answerlist = myGrade.answerlist[1:-1].replace('\'', '').replace(' ', '').split(',')
    # print(idlist)
    # print(answerlist)
    num = 0

    for i in range(len(idlist)):
        num = num + 1
        try:
            item = Questionitem.objects.get(id=idlist[i])
            item.yourAnswer = answerlist[i]
            item.num = num
            queList.append(item)
        except:
            item.yourAnswer = answerlist[i]
            item.num = num
            queList.append('题目丢失')
    print(queList)
    return render(request, 'teacher/t_gradedetails.html', {'grade': myGrade, 'mychoice': queList, 'count': num})


# 重置密码
@login_Check
def repassword(request):
    import hashlib
    id = request.GET["id"]
    u =     User.objects.get(id = id)
    p_md5 = hashlib.md5("123456".encode(encoding='utf-8')).hexdigest()
    u.password = p_md5
    u.save()
    return render(request,'teacher/t_manage.html')
# 删除学生账号##################################################
@login_Check
def deleteStudent(request,id):
    return
