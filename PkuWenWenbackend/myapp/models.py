from django.db import models
import json
# Create your models here.


# 患者类
class Patient(models.Model):
    # 默认生成一个名为id的自增列，该id为主键
    # userName不可变
    userName = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=50,default='x')
    email = models.CharField(max_length=32,default="未注册")

    realName = models.CharField(max_length=32,default='x')
    gender = models.CharField(max_length=2,default='x')
    birthday = models.DateField(null=True)
    idCardNumber = models.CharField(max_length=18,unique=True,default='x')
    phoneNumber = models.CharField(max_length=11,unique=True,default='x')


# 医生类
class Doctor(models.Model):
    # 默认生成一个名为id的自增列，该id为主键
    # userName不可变
    userName = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=50,default='x')
    email = models.CharField(max_length=32,default="未注册")

    realName = models.CharField(max_length=32,default='x')
    gender = models.CharField(max_length=2,default='x')
    birthday = models.DateField(null=True)
    idCardNumber = models.CharField(max_length=18,unique=True,default='x')
    phoneNumber = models.CharField(max_length=11,unique=True,default='x')
    college = models.CharField(max_length=32, default='Peking')
    degree = models.CharField(max_length=32, default='Peking')

    office = models.ForeignKey('Office',on_delete=models.CASCADE,null=True)
    is_leader = models.BooleanField()


# 预约表
class Appointment(models.Model):
    pName = models.CharField(max_length=32)
    dName = models.CharField(max_length=32)
    date = models.DateField()


# 处方表
class Prescription(models.Model):
    pName = models.CharField(max_length=32)
    dName = models.CharField(max_length=32)
    date = models.DateField()
    medical = models.CharField(max_length=32)


# 病历表，一个病历代表一次治疗，一次治疗会有一个处方,查询能通过病历的外码找到相应处方
class MedicalRecord(models.Model):
    pName = models.CharField(max_length=32)
    dName = models.CharField(max_length=32)
    date = models.DateField()
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)


# 院系
class Office(models.Model):
    name = models.CharField(max_length=30)  # 科室名
    leader_username = models.CharField(max_length=32, null=True, default='default_leader')
    description = models.CharField(max_length=100, null=True, default='default_description')

    def __str__(self):
        return self.name


# # 科室表
# class Office(models.Model):
#     # 科室以名称区分
#     name = models.CharField(max_length=32,primary_key=True)
#     leader_username = models.CharField(max_length=32,null=True, default='default_leader')
#     description = models.CharField(max_length=100,null=True, default='default_description')
#
#     def __str__(self):
#         return self.name


class Note(models.Model):
    note = models.CharField(max_length=180)


class UserModel(models.Model):
    userName = models.CharField(max_length=32, default='userName')  # 用户名
    password = models.CharField(max_length=50, default='000000')  # 密码
    major = models.CharField(max_length=20, default='undefined')  # 专业
    email = models.CharField(max_length=50, default='emailaddress')  # 电子邮件
    phoneNumber = models.CharField(max_length=32, default='phonenumber')  # 电话号码

    def __str__(self):
        return self.userName


class PatientModel(UserModel):
    pid = models.IntegerField()  # 标明患者的唯一id


class DoctorModel(UserModel):
    did = models.IntegerField()  # 标明医生的唯一id
    rank = models.CharField(max_length=20, default='general')  # 职级：general or chief


# 问题回复
class Reply(models.Model): 
    proNum = models.IntegerField(default=0)  # 点赞数
    conNum = models.IntegerField(default=0)  # 点踩数
    replyer = models.CharField(max_length=32)  # 用户名，在后台记录，在前台匿名
    qid = models.IntegerField()  # 这个回复所属的问题在数据库里的id
    content = models.TextField() 


# 问题
class Question(models.Model):
    publisher = models.CharField(max_length=32, default='userName') # 提问者：用户名
    # 采用匿名提问的方式，后台记录提问者，但前台不显示提问者相关信息
    title = models.CharField(max_length=50, default='xxx')  # 提问的题目

    content = models.TextField(default = '...') # 提问的内容

    cid = models.IntegerField() # 问题所属的课程在数据库里的id


# 课程
class Course(models.Model):
    sid = models.IntegerField() # 课程所属院系
    course_id = models.CharField(max_length=25, default = '0000') #课程号
    course_name = models.CharField(max_length=25)  # 课程名

    def __str__(self):
        return self.course_name




class Work(models.Model):
    doctor_name = models.CharField(max_length=32)
    office_name = models.CharField(max_length=30)

    def __str__(self):
        return self.doctor_name + ' ' + self.office_name
