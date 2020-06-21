import smtplib
from email.mime.text import MIMEText
from time import strftime, localtime

# 邮件发送服务
class EmailService:
    mailserver = "smtp.163.com"
    
    def __init__(self,senderAddress,senderPwd,mailserver,receiveAddress):
        self.senderAddress = senderAddress
        self.senderPwd = senderPwd
        self.mailserver = mailserver
        self.receiveAddress = receiveAddress

    def sendMessage(self,message):
        try:
            smtp = smtplib.SMTP(self.mailserver,port=25) # 连接邮箱服务器，smtp的端口号是25
            smtp.login(self.senderAddress,self.senderPwd)  #登录邮箱
            mail = MIMEText(message)
            mail['Subject'] = '您关注的信息有新的概念事件，请查看'
            mail['From'] = self.senderAddress  #发件人
            mail['To'] = self.receiveAddress  #收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
            smtp.sendmail(self.senderAddress,self.receiveAddress,mail.as_string())# 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            smtp.quit() # 发送完毕后退出smtp
            print ('提醒发送成功:'+strftime("%Y-%m-%d %H:%M:%S", localtime()))
        except Exception as e:
            print(e)
            return False



        
        
        


