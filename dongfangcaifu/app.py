import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from excelUtil import ExcelUtil
import threading


class Application(tk.Tk):
    def __init__(self):
            super().__init__()
            self.createUI()

    def createUI(self):
        self.fm1 = tk.Frame(self)

        self.label = tk.Label(self.fm1,text="文件保存路径:")
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.fm1)
        self.entry.pack(side=tk.LEFT)

        self.entry1 = tk.Entry(self.fm1)
        self.entry1.pack(side=tk.LEFT)

        self.fm1.pack(side=tk.TOP)

        self.fm2 = tk.Frame(self)
        self.selectButton = tk.Button(self.fm2, text="选择文件夹", command=self.selectFile)
        self.selectButton.pack(side=tk.LEFT)

        self.startButton = tk.Button(self.fm2, text="开始爬取", command=lambda :self.thread_it(self.startAction))
        self.startButton.pack(side=tk.LEFT)

        self.fm2.pack(side=tk.TOP)

        self.fm3 = tk.Frame(self)
        self.text = tk.Text(self.fm3)
        self.text.pack(side=tk.LEFT)

        self.fm3.pack(side=tk.TOP)

        self.title("财经新闻采集系统(作者:做一个俗人)")
        #窗口大小
        width ,height= 600, 600
        #窗口居中显示
        self.geometry('%dx%d+%d+%d' % (width,height,(self.winfo_screenwidth() - width ) / 2, (self.winfo_screenheight() - height) / 2))
        #窗口最大值
        self.maxsize(600,400)
        #窗口最小值
        self.minsize(300,200)

    def selectFile(self):
        Folderpath = filedialog.askdirectory() #获得选择好的文件夹
        # Filepath = filedialog.askopenfilename() #获得选择好的文件
        print('Folderpath:',Folderpath)
        # print('Filepath:',Filepath)
        self.entry.insert('end',Folderpath)

    def startAction(self):
        path = self.entry.get()
        print(path)
        if(len(path)==0):
            messagebox.showwarning(title='提示信息', message='未选择文件夹')
            return
        print('开始采集')
        excelUtil = ExcelUtil(path)
        try:
            self.text.insert('end','采集中,请稍候')
            excelUtil.start_spider()
            messagebox.showinfo(title='提示信息', message='采集完成')
        except Exception as e:
            print(e)
            messagebox.showerror(title='提示信息', message='采集失败')
    
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   
        t.start()  


app = Application()
app.mainloop()

# root.mainloop()