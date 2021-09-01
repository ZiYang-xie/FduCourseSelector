#coding=UTF-8
import smtplib
from email.mime.text import MIMEText

def sendEmail(info):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = ''  
    #密码(部分邮箱为授权码) 
    mail_pass = ''   
    sender = ''  
    receivers = ['']  

    #设置email信息
    #邮件内容设置
    message = MIMEText(info,'plain','utf-8')
    message['Subject'] = '【选课脚本通知】' 
    message['From'] = sender 
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender, receivers, message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误