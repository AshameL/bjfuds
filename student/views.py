from django.shortcuts import render
from .models import Chapter, Subchapter, Questionitem, Grade
from teacher.models import QueAccurancy
from django.http import HttpResponseRedirect


# Create your views here.

def index(request):
    return render(request, "student/index.html")


def base(request):
    return render(request, 'student/base.html')


def questiontest(request):
    chapteritem = Chapter.objects.all()
    arr = []
    for i in chapteritem:
        subchapteritem = Subchapter.objects.filter(chapterid=i.id)
        arr.append({'chapter': i, 'subchapteritem': subchapteritem})
    return render(request, 'student/questiontest.html', {'arr': arr})


# 考试页面
def exam(request, subid):
    questionlist = Questionitem.objects.filter(subchapterid=subid, visiable='1')
    num = 1
    for i in questionlist:
        i.num = num
        num = num + 1
    return render(request, 'student/exam.html', {'questionlist': questionlist,
                                                 'count': num, 'subid': subid, })


# 计算成绩
def calculationGrade(request):
    if request.method == "POST":
        subid = request.POST['subid']
        questionlist = Questionitem.objects.filter(subchapterid=subid)
        num, correct = 0, 0
        questionIdList, answerList = [], []
        for i in questionlist:
            num = num + 1
            try:
                yourAnswer = request.POST['Radios' + str(num)]
            except:
                yourAnswer = ''
            questionIdList.append(i.id)
            answerList.append(yourAnswer)
            # 尝试记录错题
            try:
                qa = QueAccurancy.objects.get(id_id=i.id)
            except:
                qa = QueAccurancy(id_id=i.id)
            # 对问答进行正误判断
            if i.answer == yourAnswer:
                # 回答正确
                correct = correct + 1
                qa.correctCount = qa.correctCount + 1
                qa.save()
            else:
                qa.wrongCount = qa.wrongCount + 1
                qa.save()
                from teacher.models import ErrorQue
                # 回答错误
                # 错题录入如果存在,count++；不存在，新建。
                if yourAnswer == '':
                    pass
                else:
                    try:
                        tmp = ErrorQue.objects.get(testid_id=34, erroranswer=yourAnswer)
                        tmp.count = tmp.count + 1
                        tmp.save()
                    except:
                        tmp = ErrorQue()
                        tmp.testid_id = i.id
                        tmp.correct = i.answer
                        tmp.erroranswer = yourAnswer
                        tmp.count = 1
                        tmp.save()
        # 计算正确率
        accurancy = round(correct / num, 4) * 100
        # 保存成绩单到数据库

        # 临时写死
        # userid = request.session['userid']
        userid = 1
        myGrade = Grade()
        myGrade.userid_id = userid
        myGrade.accurancy = accurancy
        myGrade.subchapter_id = subid
        myGrade.questionlist = questionIdList
        myGrade.answerlist = answerList
        myGrade.save()
        gradeid = myGrade.id
        return render(request, 'student/showGrade.html',
                      {'accurancy': accurancy, 'errcount': (num - correct), 'gradeid': gradeid})
    return HttpResponseRedirect('/index')


# 显示解析内容
def showAnalysis(request, gradeid):
    myGrade = Grade.objects.get(id=gradeid)
    queList = []
    idlist = myGrade.questionlist[1:-1].split(',')
    answerlist = myGrade.answerlist[1:-1].replace('\'', '').replace(' ', '').split(',')
    print(idlist)
    print(answerlist)
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

    return render(request, 'student/analysis.html', {"questionlist": queList, 'count': num})


def scorelist(request):
    # userid = request.session['userid']
    userid = 1
    gradelist = Grade.objects.filter(userid_id=userid)
    num = 1
    for i in gradelist:
        i.num = num
        num = num + 1
    return render(request, 'student/scorelist.html', {'gradelist': gradelist})
