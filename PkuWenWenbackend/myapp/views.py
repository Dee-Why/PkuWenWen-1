from django.shortcuts import render
from . import models
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
import json
import requests
import json
from django.core.mail import send_mail
from django.conf import settings
import re
import random
import json
import dateutil.parser

# Create your views here.

@csrf_exempt
def patient_register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', '未注册')

    realName = request.POST.get('realName','xxx')
    phoneNumber = request.POST.get('phoneNumber','xxx')
    idCardNumber = request.POST.get('idCardNumber','xxx')
    gender = request.POST.get('gender','x')
    birthday = dateutil.parser.parse(request.POST.get('birthday','2000-01-01'))



    res = {'retCode': 0, 'message': ''}

    obj = models.Patient.objects.filter(userName=userName)
    if obj.count() == 0:

        models.Patient.objects.create(
            userName=userName, password=password,email=email,realName=realName,
            gender=gender,birthday=birthday,idCardNumber=idCardNumber,phoneNumber=phoneNumber
        )
        obj = models.Patient.objects.get(userName=userName)
        # obj.collectList.remove('-1')
        obj.save()
        res['retCode'] = 1
        res['message'] = '注册成功'

    else:
        res['retCode'] = 0
        res['message'] = '用户名已注册'

    return JsonResponse(res)

@csrf_exempt
def docter_register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', '未注册')

    realName = request.POST.get('realName','xxx')
    phoneNumber = request.POST.get('phoneNumber','xxx')
    idCardNumber = request.POST.get('idCardNumber','xxx')
    gender = request.POST.get('gender','x')
    birthday = dateutil.parser.parse(request.POST.get('birthday','2000-01-01'))

    college = request.POST.get('college','Peking')
    degree = request.POST.get('degree','Peking')
    office_name = request.POST.get('office','x')
    is_leader = int(request.POST.get('leader',0))

    res = {'retCode': 0, 'message': ''}

    obj = models.Doctor.objects.filter(userName=userName)
    if obj.count() == 0:
        office = models.Office.objects.filter(name=office_name)
        if office.count() == 0:
            office = None
        else:
            office = office[0]
            if is_leader == True:
                office.leader_username = userName
                office.save()

        models.Doctor.objects.create(
            userName=userName, password=password,email=email,realName=realName,
            gender=gender,birthday=birthday,idCardNumber=idCardNumber,phoneNumber=phoneNumber,
            college=college,degree=degree,office=office,is_leader=is_leader

        )
        obj = models.Doctor.objects.get(userName=userName)
        # obj.collectList.remove('-1')
        obj.save()
        res['retCode'] = 1
        res['message'] = '注册成功'

    else:
        res['retCode'] = 0
        res['message'] = '用户名已注册'

    return JsonResponse(res)


# 注册（使用了Django内助的邮箱验证功能）
@csrf_exempt
def register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', 'undefined')
    userType = request.POST.get('userType', 'patient')
    res = {'retCode': 0, 'message': ''}

    obj = models.UserModel.objects.filter(userName=userName)
    objmail = models.UserModel.objects.filter(email=email)

    if obj.count() == 0 and objmail.count() == 0:
        mailret = send_mail('PkuHospital注册', '您正在进行PkuHospital注册，如果不是您亲自操作，请及时联系本邮箱',
                            'se_5group@163.com', [email], fail_silently=False)

        if mailret == 1:
            if userType == 'patient':
                models.PatientModel.objects.create(userName=userName, password=password,email=email)
                obj = models.PatientModel.objects.get(userName=userName)
            elif userType == 'doctor':
                models.DoctorModel.objects.create(userName=userName, password=password,email=email)
                obj = models.DoctorModel.objects.get(userName=userName)
            obj.save()
            res['retCode'] = 1
            res['message'] = '注册成功'

        else:
            res['retCode'] = 2
            res['message'] = '请输入正确的邮箱地址'

    else:
        res['retCode'] = 0
        res['message'] = '用户名或邮箱已注册'

    return JsonResponse({'register': res})

# 登录：登录之后会自动跳转到OfficeIndex页
@csrf_exempt
def login(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    res = {'retCode': 0, 'message': ''}
    print("userName = {}, password = {}".format(userName,password))
    obj = models.UserModel.objects.filter(userName=userName)

    if obj.count() == 0:
        res['retCode'] = 0
        res['message'] = '用户不存在'
        print('用户不存在')
    else:
        obj = models.UserModel.objects.get(userName=userName)
        if obj.password == password:
            res['retCode'] = 1
            res['message'] = '成功登录'
            print("登陆成功")
        else:
            res['retCode'] = 2
            res['message'] = '密码错误'
            print("密码错误")
    return JsonResponse({'login': res})
    # return HttpResponse(json.dumps({'login': res}))
@csrf_exempt
def getOfficeIndex(request):
    retdata = {}
    offices = models.Office.objects.values()
    office_list = list(offices)
    res_list = list()
    for office in office_list:
        doctor_num = len(models.Office.objects.raw('SELECT * FROM myapp_work WHERE office_name = %s', [office['office_name']]))
        res_list.append({'office_name': office['office_name'], 'doctor_num': doctor_num})
    retdata['Officelist'] = res_list
    return JsonResponse(retdata)

@csrf_exempt
def getCourseIndex(request):
    SchoolName = request.POST.get('schoolname')
    print(SchoolName)
    which_school = models.School.objects.get(school_name = SchoolName)
    courses = models.Course.objects.filter(sid = which_school.id).values()
    retdata = {}
    retdata['courselist'] = list(courses)
    return JsonResponse(retdata)

@csrf_exempt
def getQuestionIndex(request):
    CourseName = request.POST.get('coursename')
    print(CourseName)
    which_course = models.Course.objects.get(course_name = CourseName)
    questions = models.Question.objects.filter(cid = which_course.id).values()
    retdata = {}
    retdata['questionlist'] = list(questions)
    return JsonResponse(retdata)

@csrf_exempt
def addQuestion(request):
    CourseName = request.POST.get('coursename')
    which_course = models.Course.objects.get(course_name = CourseName)
    q_publisher = request.POST.get('publisher')
    q_title = request.POST.get('title')
    q_content = request.POST.get('content')
    q1 = models.Question(cid = which_course.id, publisher = q_publisher, title = q_title, content = q_content)
    q1.save()
    res = {'retCode': 0, 'message': ''}
    if(q1.id > 0 ):
        res['retCode'] = 0
        res['message'] = '成功添加问题'
    else:
        res['retCode'] = 1
        res['message'] = '添加问题失败'
    return JsonResponse({'addQuestion':res})

@csrf_exempt
def addReply(request):
    rep = request.POST.get('replyer')
    ct = request.POST.get('reply_content')
    Qid = request.POST.get('qid')
    p1 = models.Reply(proNum = 0, conNum = 0, replyer = rep, qid = Qid, content = ct)
    p1.save()

    res = {'retCode': 0, 'message': ''}
    if(p1.id > 0 ):
        res['retCode'] = 0
        res['message'] = '成功添加回复'
    else:
        res['retCode'] = 1
        res['message'] = '添加回复失败'
    return JsonResponse(res)

@csrf_exempt
def getAnswerList(request):#返回answerList和当前问题的内容
    Qid = request.POST.get('question_id')
    ques =  models.Question.objects.get(id = Qid)
    replys = models.Reply.objects.filter(qid = Qid).values()
    retdata = {}
    retdata['answerlist'] = list(replys)
    retdata['question'] = {'title':ques.title, 'content':ques.content}

    return JsonResponse(retdata)

@csrf_exempt
def likeAnswer(request):
    rid = request.POST.get('answer_id')
    rep = models.Reply.objects.get(id = rid)
    rep.proNum = rep.proNum +1
    rep.save()
    res = {'retCode': 0, 'message': 'OK'}
    return JsonResponse(res)

@csrf_exempt
def dislikeAnswer(request):
    CourseName = request.POST.get('coursename')
    which_course = models.Course.objects.get(course_name = CourseName)
    q_publisher = request.POST.get('publisher')
    q_title = request.POST.get('title')
    q_content = request.POST.get('content')
    q1 = models.Question(cid = which_course.id, publisher = q_publisher, title = q_title, content = q_content)
    q1.save()
    res = {'retCode': 0, 'message': ''}
    if(q1.id > 0 ):
        res['retCode'] = 0
        res['message'] = '成功添加问题'
    else:
        res['retCode'] = 1
        res['message'] = '添加问题失败'
    return JsonResponse({'addQuestion':res})

@csrf_exempt
def openSchool(request):
    schoolName = request.POST.get('school', '信息科学技术学院')
    courses = [ {'date': '更新于 2021-06-03 15:56:00', 'title': 'course1 from backend openSchool'}, {'date': '更新于 2021-06-03 15:56:00', 'title': 'course2 from backend openSchool'} ]
    courses = json.JSONEncoder(ensure_ascii=False).encode(courses)
    print("将courses发回前端")
    return JsonResponse({'retCode': 1, 'courses': courses})


@csrf_exempt
def openCourse(request):
    courseName = request.POST.get('course', '软件工程')
    questions = [
        {'date': '更新于 2021-06-03 15:56:00', 'title': 'Question1 from backend', 'content': 'c1', 'stars': 58, 'link': 'l1'},
        {'date': '更新于 2021-06-03 15:56:00', 'title': 'Question2 from backend', 'content': 'c2', 'stars': 66, 'link': 'l2'},
        ]
    questions = json.JSONEncoder(ensure_ascii=False).encode(questions)
    return JsonResponse({'retCode': 1, 'questions': questions})


@csrf_exempt
def openQuestion(request):
    courseName = request.POST.get('question', '默认问题')

    curQuestion = { 'publisher': 'alice', 'title': 'ahhhhhhh', 'detail': '咆哮啊啊啊', 'proNum': 2, 'conNum': 1, 'subscribeNum': 3,}
    curQuestion = json.JSONEncoder(ensure_ascii=False).encode(curQuestion)
    curAnswer = { 'publisher': 'bob', 'title': 'hahahahahaha', 'detail': '哈哈哈哈哈', 'proNum': 6, 'conNum': 6, 'subscribeNum': 12,}
    # 现在只显示一个问题和一个答案, 如果我们想要看一个问题的所有答案, 只需要搞成list of dict 就可以了 暂时不实现
    curAnswer = json.JSONEncoder(ensure_ascii=False).encode(curAnswer)

    return JsonResponse({'retCode': 1, 'curQuestion': curQuestion, 'curAnswer': curAnswer})


@csrf_exempt
def submitQuestion(request):
    questionTitle = request.POST.get('title', '缺少标题')
    questionDate1 = request.POST.get('date1', '0000-00-00')
    questionDate2 = request.POST.get('date2', '00:00:00')
    questionDetail = request.POST.get('detail', '缺少问题描述')
    # 此处应该把问题存到数据库里
    return JsonResponse({'retCode': 1, 'title': questionTitle, 'detail': questionDetail})

'''
这个关注课程功能不仅不重要而且很麻烦我先不写了。
@csrf_exempt
def AddFollowCourse(request):
    course_name = request.POST.get('course_name')
    user_name = request.POST.get('userName')
    user_obj = models.UserModel.objects.get(userName = user_name)
    user_obj.
'''
