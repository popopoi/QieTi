
from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox #这个是消息框，对话框的关键
#from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import PIL
import os
import os.path
import Main
import imghdr

source_dirpath="/Users/tt/Desktop/t"
save_dirpath=" /Users/tt/Desktop/y"
showingimage_filepath = "/Users/tt/Desktop/test/test.jpg"
showingimage_index=0

artificialjudge="yes"
imagefilepaths = []
save_imagefilepaths = []

class mainapp:
    
    def __init__(self):
        root=Tk()
        root.title("自动切题系统")
        root.geometry('400x340')
        root.resizable(width=False, height=True) 
        self.v = StringVar()#绑定文本框的变量
        self.v.set("请选择文件夹...")
        ent = Entry(root, width=30,textvariable = self.v)
        ent.place(relx=0.4,rely=0.1,anchor=CENTER)
        button1 = Button(root, text='选择文件夹', command=self.choose_sourcedirpath)
        button1.place(relx=0.85,rely=0.1,anchor=CENTER)

        self.var = StringVar()#绑定listbox的列表值
        self.var.set((''))
        self.listbox = Listbox(root,width=40,listvariable = self.var).place(relx=0.5,rely=0.4,anchor=CENTER)
        self.button2=Button(root,text='开始切题',command=self.starter).place(relx=0.1,rely=0.7,anchor=CENTER)
        
        self.checkbutton=Checkbutton(root,text='是否人工校对结果',command = self.callCheckbutton)
        self.checkbutton.place(relx=0.8,rely=0.7,anchor=CENTER)
        self.checkbutton.select()
        self.lb = Label(root,text = '')
        self.lb.place(relx=0.2,rely=0.7,anchor=CENTER)
        
        self.v2 = StringVar()#绑定文本框的变量
        self.v2.set("请选择切题结果保存文件夹...")
        ent2 = Entry(root, width=30,textvariable = self.v2)
        ent2.place(relx=0.4,rely=0.8,anchor=CENTER)
        button3 = Button(root, text='选择文件夹', command=self.choose_savedirpath)
        button3.place(relx=0.85,rely=0.8,anchor=CENTER)
        root.mainloop()
    def callCheckbutton(self):
        #改变v的值，即改变Checkbutton的显示值
        global artificialjudge
        if(artificialjudge=="no"):
            artificialjudge='yes'
            #print(artificialjudge)
        elif(artificialjudge=="yes"):
            artificialjudge='no'
            #print(artificialjudge)
    def choose_sourcedirpath(self):
        self.v.set('')#清空文本框里内容
        self.var.set((('')))
        #filename = tkinter.filedialog.askopenfilename()
        global source_dirpath 
        source_dirpath = filedialog.askdirectory()
        print(source_dirpath)
        if source_dirpath :
            self.v.set(source_dirpath)
        self.getdir(source_dirpath)
    def choose_savedirpath(self):
        self.v2.set('')#清空文本框里内容
        global save_dirpath 
        save_dirpath  = filedialog.askdirectory()
        #print(dir(filedialog))
        print(save_dirpath )
        if save_dirpath  :
            self.v2.set(save_dirpath)
    def getdir(self,dirpath):
        #把目录中遍历出来的文件目录显示到列表框中
        fp = os.listdir(dirpath)
        self.var.set(fp)
    def starter(self):
        if(source_dirpath=="" or save_dirpath==""):
            tkinter.messagebox.showinfo('提示',"请先选择图库文件夹和保存文件夹的路径！")
            print("请先选择图库文件夹和保存文件夹的路径！")
            return 
        if(artificialjudge=="no"):
            tkinter.messagebox.showinfo('提示',"文件夹中的图片已经开始切题！请到指定文件夹中查看")
            return
        else:
            tkinter.messagebox.showinfo('提示',"请稍等，这可能需要几秒甚至几分钟！")
            showpic()
    
class showpic:
    def __init__(self):
        r1=Toplevel()
        r1.title('切题结果人工校对')
        r1.geometry('400x400')
        Label(r1,text='图片路径：').place(relx=0,rely=0.04)
        Label(r1,text=save_dirpath).place(relx=0.2,rely=0.04)
        
        #根据图库路径source_dirpath开始遍历识别，识别结果存储在save_dirpath文件夹
        self.startOcr(source_dirpath,save_dirpath)
        global save_imagefilepaths
        save_imagefilepaths=self.get_imagefilepaths_bydirpath(save_dirpath)
        if(len(save_imagefilepaths)!=0):
            showingimage_filepath=save_imagefilepaths[0]
        
        
        
        global imagefilepaths
        img_open=Image.open(showingimage_filepath)
        img_open.thumbnail((200,200))
        img=ImageTk.PhotoImage(img_open)
        self.l1=Label(r1,image=img)
        self.l1.place(relx=0,rely=0.18)
        
        self.button2=Button(r1,text='下一张',command=self.jumpimage).place(relx=0.1,rely=0.8,anchor=CENTER)
        self.button3=Button(r1,text='删除这张',command=self.deleteimage).place(relx=0.5,rely=0.8,anchor=CENTER)
        r1.mainloop()
    def startOcr(self,source_dirpath,save_dirpath):
        global imagefilepaths
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
        for filepath in imagefilepaths:
            Main.singleocr(filepath,save_dirpath,0)
        
    def is_img(self,ext):
         ext = imghdr.what(ext)
         #print(ext)
         if ext == 'jpg':
          return True
         elif ext == 'png':
          return True
         elif ext == 'jpeg':
          return True
         elif ext == 'gif':
          return True
         else:
          return False        
    def get_imagefilepaths_bydirpath(self,source_dirpath):  
        if not os.path.isdir(source_dirpath):
            #tkinter.messagebox.showinfo('提示',"这不是一个文件夹")
            print("这不是一个文件夹")
            return
        global files
        files = os.listdir(source_dirpath) 
        imagefilepaths=[]
        for index in range(len(files)):
            path = "%s/%s" %(source_dirpath,files[index])   
            if os.path.isdir(path):
                files[index] = ""#将文件夹对象设为空
            else:
                if(self.is_img(source_dirpath+"/"+files[index])==True):
                    imagefilepaths.append(source_dirpath+"/"+files[index])
        return imagefilepaths 
    def jumpimage(self): #跳过
        global showingimage_filepath
        global save_imagefilepaths
        global showingimage_index
        '''print("jump前")
        print("showingimage_filepath is ",showingimage_filepath)'''
        
        showingimage_index=showingimage_index+1
        if(len(save_imagefilepaths)==showingimage_index):
            tkinter.messagebox.showinfo('提示',"已经遍历完结果")
            return
        showingimage_filepath=save_imagefilepaths[showingimage_index]
        '''print("jump后")
        print("showingimage_filepath is ",showingimage_filepath)'''
        self.newimage = ImageTk.PhotoImage(file=showingimage_filepath) #需要储存为实例属性，否则会被垃圾回收
        self.l1.configure(image=self.newimage)##
        
    def deleteimage(self):   #删除
        global showingimage_filepath
        delete_path=showingimage_filepath
        tkinter.messagebox.showinfo('提示',"确定要删除吗")
        jump()
        os.remove(delete_path)
        
mainapp()