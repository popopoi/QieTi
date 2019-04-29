
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
import _thread
import time

source_dirpath=""
save_dirpath=""
showingimage_filepath = ""

#再次进行开始识别时需要init的全局变量
showingimage_index=0
imagefilepaths = []
save_imagefilepaths = []
save_imagenumber=0
deleted_imagenumber=0

artificialjudge="yes"
imagefilepaths = []
save_imagefilepaths = []

save_imagenumber=0
deleted_imagenumber=0

startocr_finished=False
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
        self.consolelabel=Label(root,text = '...')
        self.consolelabel.place(relx=0.2,rely=0.7,anchor=CENTER)
        
        
        self.checkbutton=Checkbutton(root,text='是否人工校对结果',command = self.callCheckbutton)
        self.checkbutton.place(relx=0.8,rely=0.7,anchor=CENTER)
        self.checkbutton.select()
        #self.lb = Label(root,text = '')
        #self.lb.place(relx=0.2,rely=0.7,anchor=CENTER)
        
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
    def global_init1(self):
        global showingimage_index
        global imagefilepaths
        global save_imagefilepaths
        global save_imagenumber
        global deleted_imagenumber
        showingimage_index=0
        imagefilepaths = []
        save_imagefilepaths = []
        save_imagenumber=0
        deleted_imagenumber=0
    def starter(self):
        if(source_dirpath=="" or save_dirpath==""):
            tkinter.messagebox.showinfo('提示',"请先选择图库文件夹和保存文件夹的路径！")
            print("请先选择图库文件夹和保存文件夹的路径！")
            return 
        else:
            self.global_init1()
        if(artificialjudge=="no"):
            tkinter.messagebox.showinfo('提示',"文件夹中的图片已经开始切题！请稍后到指定文件夹中查看")
            self.startOcr(source_dirpath,save_dirpath)
        else:   
            #_thread.start_new_thread(tkinter.messagebox.askokcancel,('确认开始切题吗？',"这可能需要几秒甚至几分钟！"))
            b=tkinter.messagebox.askyesno('确认要切题吗？',"这可能需要几秒甚至几分钟！")
            if(b==True):
                #_thread.start_new_thread(tkinter.messagebox.showinfo,('正在为您切题',"请稍等..."))
                tkinter.messagebox.showinfo('点击ok键开始运行',"点击ok键后开始...切题需要几秒甚至几分钟请稍等")
                #_thread.start_new_thread(self.startOcr,(source_dirpath,save_dirpath))
                self.startOcr(source_dirpath,save_dirpath)
                global startocr_finished
                while(startocr_finished==False):
                    if(startocr_finished==True):
                        time.sleep(1)
                        break;
                showpic()
    def startOcr(self,source_dirpath,save_dirpath):
        global imagefilepaths
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
            return
        imagenumber=1
        for filepath in imagefilepaths:
            print("#####################################")
            print("ocr controller:start ocr for ",filepath)
            #consolemessage="正在处理第"+str(imagenumber)+"张..."
            #self.consolelabel.configure(text=consolemessage)
            Main.singleocr(filepath,save_dirpath,0)
            imagenumber=imagenumber+1
        global startocr_finished
        startocr_finished=True
        return
    def changeconsole(self,consolemessage):
        self.consolelabel.configure(text=consolemessage)
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
class showpic:
    def __init__(self):
        r1=Toplevel()
        r1.title('切题结果人工校对')
        r1.geometry('600x400')

        
        #根据图库路径source_dirpath开始遍历识别，识别结果存储在save_dirpath文件夹
        #self.startOcr(source_dirpath,save_dirpath)
        #_thread.start_new_thread(self.startOcr,(source_dirpath,save_dirpath))
        global save_imagefilepaths
        save_imagefilepaths=self.get_imagefilepaths_bydirpath(save_dirpath)
        global showingimage_filepath
        global save_imagenumber
        save_imagenumber=len(save_imagefilepaths)
        if(save_imagenumber!=0):
            showingimage_filepath=save_imagefilepaths[0]

        self.label=Label(r1,text='图片路径：')
        self.label.place(relx=0,rely=0.04)
        self.pathlabel=Label(r1,text=showingimage_filepath)
        self.pathlabel.place(relx=0.2,rely=0.04)
        
        
        global imagefilepaths
        img_open=Image.open(showingimage_filepath)
        img_open.thumbnail((500,500))
        img=ImageTk.PhotoImage(img_open)
        self.l1=Label(r1,image=img)
        self.l1.place(relx=0,rely=0.18)
        
        self.button2=Button(r1,text='下一张',command=self.jumpimage)
        self.button2.place(relx=0.1,rely=0.8,anchor=CENTER)
        self.button3=Button(r1,text='删除这张',command=self.deleteimage)
        self.button3.place(relx=0.5,rely=0.8,anchor=CENTER)
        r1.mainloop()
    def startOcr(self,source_dirpath,save_dirpath):
        global imagefilepaths
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
            return 
        for filepath in imagefilepaths:
            print("ocr contoller:start ocr for ",showingimage_filepath)
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
        global save_imagenumber
        global deleted_imagenumber
        showingimage_index=showingimage_index+1
        if((save_imagenumber+deleted_imagenumber)<=showingimage_index):
            self.pathlabel.configure(text="已经没有下一张了")
            tkinter.messagebox.showinfo('提示',"已经遍历完结果")
            img_open=Image.open("./111.JPG")
            img_open.thumbnail((600,600))
            global lastimage#定义成全局变量才显示得出来！！！！！
            lastimage = ImageTk.PhotoImage(img_open) #需要储存为实例属性，否则会被垃圾回收
            self.l1.configure(image=lastimage)
            self.button2.configure(state=DISABLED)
            self.button3.configure(state=DISABLED)
            return
            
        showingimage_filepath=save_imagefilepaths[showingimage_index]
        self.pathlabel.configure(text=showingimage_filepath)
        
        '''print("jump后")
        print("showingimage_filepath is ",showingimage_filepath)'''
        

        print("test board:showing ",showingimage_filepath)
        img_open=Image.open(showingimage_filepath)
        img_open.thumbnail((500,500))
        '''这里有踩过的坑'''
        global newimage#定义成全局变量才显示得出来！！！！！
        newimage = ImageTk.PhotoImage(img_open) #需要储存为实例属性，否则会被垃圾回收
        self.l1.configure(image=newimage)##

    def deleteimage(self):   #删除
        global showingimage_filepath
        delete_path=showingimage_filepath
        a=tkinter.messagebox.askyesno('提示',"确定要删除吗")
        if(a==False):
            return
        print("test board:delete*** ",showingimage_filepath)
        global save_imagenumber
        global deleted_imagenumber
        save_imagenumber=save_imagenumber-1
        deleted_imagenumber=deleted_imagenumber+1
        self.jumpimage()
        os.remove(delete_path)
        tkinter.messagebox.showinfo('提示',"删除成功")
        
        
mainapp()