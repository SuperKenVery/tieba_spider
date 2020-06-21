import tkinter as tk
from tkinter import filedialog,scrolledtext
from tkinter import messagebox
from tkinter import *
import threading
import os
from tonghuashunSpider import Spider
from selenium import webdriver
import json
import time


class LoginApp(tk.Tk):
    config_driver = 'driver.txt'
    default_config_driver = 'default_driver.txt'
    def __init__(self):
            super().__init__()
            self.createLogin()

    def getDriverPath(self):
        if(os.path.exists(self.config_driver)):
            f = open(self.config_driver,"r")   #设置文件对象
            str = f.read()     #将txt文件的所有内容读入到字符串str中
            print(str)
            self.driverPath = str
            f.close()   #将文件关闭  
        else:
            f = open(self.default_config_driver,"r")   #设置文件对象
            str = f.read()     #将txt文件的所有内容读入到字符串str中
            print(str)
            self.driverPath = os.path.join(str)
            f.close()   #将文件关闭

        
                

    def createLogin(self):
        self.fm1 = tk.Frame(self)

        self.label = tk.Label(self.fm1)
        self.label.grid(row=0, stick=tk.W, pady=10)

        self.label1 = tk.Label(self.fm1,text = '账户: ')
        self.label1.grid(row=1, stick=tk.W, pady=10)

        self.entry1 = tk.Entry(self.fm1)
        self.entry1.grid(row=1, column=1, stick=tk.E)

        self.label2 = tk.Label(self.fm1,text = '密码: ')
        self.label2.grid(row=2, stick=tk.W, pady=10)

        self.entry2 = tk.Entry(self.fm1,show='*')
        self.entry2.grid(row=2, column=1, stick=tk.E)

        self.button1 = tk.Button(self.fm1, text='登录', command=self.login)
        self.button1.grid(row=3, stick=tk.W, pady=10)

        # self.button2 = tk.Button(self.fm1, text='退出', command=self.quit)
        # self.button2.grid(row=3, column=1, stick=tk.E)

        self.button3 = tk.Button(self.fm1, text='免登录', command=self.no_login)
        self.button3.grid(row=3, column=1, stick=tk.E)

        self.fm1.pack(side=tk.TOP)
        
        self.title("登录")
        width = 280
        height = 200
        screenwidth = self.winfo_screenwidth()  
        screenheight = self.winfo_screenheight() 
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
        self.geometry(alignstr)

    def login(self):
        try:
            username = self.entry1.get()
            password = self.entry2.get()
            if(len(username) == 0 or len(username) == 0):
                messagebox.showerror(title='提示信息', message='账户或密码不能为空')
                return
            self.getCookie(username,password)
            self.destroy()
            app = Application(TRUE)
            app.mainloop()
        except Exception as e:
            print(e)
            messagebox.showerror(title='提示信息', message='登录失败')
        
    def no_login(self):
        self.destroy()
        app = Application(FALSE)
        app.mainloop()

    def quit(self):
        self.destroy()

    def getCookie(self,name,pwd):
        self.getDriverPath()
        print(self.driverPath)
        browser = webdriver.Chrome(self.driverPath)
        url = 'http://upass.10jqka.com.cn/login?redir=HTTP_REFERER'
        browser.get(url)
        username = browser.find_elements_by_xpath('//input[@id="username"]')[0]
        password = browser.find_elements_by_xpath('//input[@id="password"]')[0]
        login = browser.find_elements_by_xpath('//input[@id="loginBtn"]')[0]
        username.send_keys(name)
        password.send_keys(pwd)
        login.click()
        cookies = browser.get_cookies()
        browser.close()
        print(cookies)
        path = 'cookies'+'_'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
        with open(path, "w") as fp:
            json.dump(cookies, fp)


class Application(tk.Tk):
    default_path = 'settings.txt'

    def __init__(self,login_status):
            super().__init__()
            self.login_status = login_status
            self.createUI()



    def createUI(self):
        self.fm1 = tk.Frame(self)

        self.label = tk.Label(self.fm1,text="接收邮箱地址:")
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.fm1)
        self.entry.pack(side=tk.LEFT)

        self.fm1.pack(side=tk.TOP)

        self.fm2 = tk.Frame(self)

        self.startButton = tk.Button(self.fm2, text="开始运行", command=lambda :self.thread_it(self.startAction))
        self.startButton.pack(side=tk.LEFT)

        self.fm2.pack(side=tk.TOP)

        self.fm3 = tk.Frame(self)
        # self.text = tk.Text(self.fm3)
        # self.text.pack(side=tk.LEFT)

        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD)     # wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
        self.text.pack(side=tk.LEFT)

        self.fm3.pack(side=tk.TOP)

        self.title("股票监控系统(作者:做一个俗人)")
        #窗口大小
        width ,height= 600, 600
        #窗口居中显示
        self.geometry('%dx%d+%d+%d' % (width,height,(self.winfo_screenwidth() - width ) / 2, (self.winfo_screenheight() - height) / 2))
        #窗口最大值
        self.maxsize(600,400)
        #窗口最小值
        self.minsize(300,200)
        settings = self.getSettings()
        if(settings != ''):
            self.entry.insert('end',settings)


    

    def getSettings(self):
        setting = ''
        if(os.path.exists(os.path.abspath(self.default_path))):
            with open(self.default_path,'r') as f:
                setting = f.read()
                f.close()
        return setting


    def saveSettings(self,path):
        with open(self.default_path,'w') as f:
            f.write(path) 
            f.close()

    def startAction(self):
        path = self.entry.get()
        print(path)
        if(len(path)==0):
            messagebox.showwarning(title='提示信息', message='请先填写接收邮箱')
            return
        settings = self.getSettings() 
        self.saveSettings(path)
        try:
            self.text.insert('end','实时监控中\n')
            spider = Spider(self,path,self.login_status)
        except Exception as e:
            print(e)
            messagebox.showerror(title='提示信息', message='监控异常')
    
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   
        t.start()  

path = 'cookies'+'_'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt'
if(os.path.exists(path)):
    root = Application(TRUE)
else:
    root = LoginApp()
root.mainloop()


# root.mainloop()