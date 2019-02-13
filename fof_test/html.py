# encoding:utf-8
import unittest
from util import HTMLTestRunner
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 用于返回最新生成的测试报告
def new_file(father_path):
    # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
    lists = os.listdir(father_path)
    # 按照文件的创建时间对lists进行排序
    lists.sort(key=lambda fn: os.path.getmtime(father_path + '/' + fn))
    # oc.path.join() 方法用于将文件目录与文件名进行拼接
    file_path = os.path.join(father_path , lists[-1])
    #print lists[-1]
    #L=file_path.split('\\')
    #file_path='\\\\'.join(L)
    #return file_path
    return lists[-1]

# 用于发送最新产生的测试报告
def send_email(newfile):

    f = open(newfile, 'rb')
    mail_body = f.read()
    #print mail_body
    f.close()
    
    smtpserver = 'smtp.qq.com' #设置服务器，qq邮箱端口465
    user = '1769957847@qq.com' #用户名
    password = 'pvvqyrlghxjubgih' #口令
    sender = '1769957847@qq.com' #发送者
    
    receiver = ['zxl_73@126.com', '2103201937@qq.com'] #接收者
    subject = '自动定时发送测试报告' #邮件主题
    msg = MIMEMultipart('mixed') #创建一个带附件的邮件实例
    msg_html1 = MIMEText(mail_body, 'html', 'utf-8') #创建一个实例，这里设置为html格式邮件
    msg.attach(msg_html1) #邮件内容添加
    msg_html = MIMEText(mail_body, 'html', 'utf-8')
    msg_html["Content-Disposition"] = 'attachment; filename = test_report.html'
    msg.attach(msg_html) #邮件附件内容添加
    msg['From'] = '张现龙<1769957847@qq.com>'
    msg['To'] = ";".join(receiver)
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    #smtp.connect(smtpserver, 465) #连接到指定的smtp服务器
    smtp.login(user, password) #登录smtp服务器
    smtp.sendmail(sender, receiver, msg.as_string()) #发送邮件（发送者、接收者、发送消息）
    smtp.quit() #断开与smtp服务器的连接

if __name__ == '__main__':
    print '=====AutoTest Start======'

    #获取当前脚本的绝对路径
    #pwd = os.path.abspath('..')
    pwd = os.getcwd()
    #print pwd
    #获取测试case的绝对路径
    case_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    #获取test路径
    test_path = os.path.abspath(os.path.join(os.path.dirname('html.py'),os.path.pardir))
    print test_path
    #获取test_result路径
    test_result_path = test_path + '//test_result'
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test_*.py')
    now = time.strftime('%Y-%m-%d-%H_%M_%S_')
    filename = test_result_path + '//' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')
    runner.run(discover)
    fp.close()
    new_report = new_file('father_path')
    print new_report
    send_email(filename)    
    print '=====AutoTest Over======'
