from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog as filedialog

import os

import sys

sys.path.append(r'C:\Users\嗯哼哈吼嘻\AppData\Local\Programs\Python\Python37\Lib\site-packages')

filepath = ""


class mainapp:

    def __init__(self):
        root = Tk()
        root.title("自动切题系统")
        root.geometry('400x340')
        root.resizable(width=False, height=False)
        self.v = StringVar()  # 绑定文本框的变量
        self.v.set("请选择文件夹...")
        ent = Entry(root, width=36, textvariable=self.v).place(relx=0.38, rely=0.1, anchor=CENTER)
        button1 = Button(root, text='选择文件夹', command=self.choosedir).place(relx=0.85, rely=0.1, anchor=CENTER)

        self.var = StringVar()  # 绑定listbox的列表值
        self.var.set((''))
        listbox = Listbox(root, width=50, listvariable=self.var).place(relx=0.5, rely=0.42, anchor=CENTER)
        button2 = Button(root, text='开始切题', command=self.starter).place(relx=0.13, rely=0.75, anchor=CENTER)

        self.checkbutton=Checkbutton(root,text='是否人工校对结果',command = self.callCheckbutton)
        self.checkbutton.place(relx=0.8,rely=0.75,anchor=CENTER)
        self.checkbutton.select()
        #self.lb = Label(root, text='')
        #self.lb.place(relx=0.2, rely=0.7, anchor=CENTER)
        root.mainloop()

    def callCheckbutton(self):
        #改变v的值，即改变Checkbutton的值
        global artificialjudge
        if(artificialjudge=="no"):
            artificialjudge='yes'
            #print(artificialjudge)
        elif(artificialjudge=="yes"):
            artificialjudge='no'
            #print(artificialjudge)

    def choosedir(self):
        self.v.set('')  # 清空文本框里内容
        self.var.set((('')))
        # filename = tkinter.filedialog.askopenfilename()
        global filepath
        filepath = filedialog.askdirectory()
        # print(dir(filedialog))
        print(filepath)
        if filepath:
            self.v.set(filepath)
        self.getdir(filepath)

    def getdir(self, filepath):
        # 把目录中遍历出来的文件目录显示到列表框中
        fp = os.listdir(filepath)
        self.var.set(fp)

    def starter(self):
        showpic()


class showpic:
    def __init__(self):
        r1 = Toplevel()
        r1.title('切题结果人工校对')
        r1.geometry('400x400')
        Label(r1, text='图片路径：').place(relx=0, rely=0.04)
        e1 = Entry(r1)
        e1.place(relx=0.15, rely=0.04)
        Button(r1, text='选择图片').place(relx=0.52, rely=0.02)
        Label(r1, text="所选择的图片：").place(relx=0, rely=0.13)
        img_open = Image.open('/Users/tt/Desktop/test/test.jpg')
        img_open.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img_open)
        l1 = Label(r1, image=img)
        l1.place(relx=0, rely=0.18)
        r1.mainloop()


class fanzhuan:
    def __init__(self):
        r2 = Tk()
        r2.mainloop()


mainapp()