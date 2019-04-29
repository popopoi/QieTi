from tkinter import *
import tkinter.filedialog
import os
import os.path
from PIL import Image


root = Tk()
files = []
f_files = []
cut_files = []

img_showing = ""
cut_img_showing = ""
file_path=""
delete_path = ""



def xz():
    #file_path = tkinter.filedialog.askopenfilename()
    global file_path 
    file_path = tkinter.filedialog.askdirectory()
    if file_path != '':
        lb.config(text = "您选择的文件夹是："+file_path);
        print(file_path)
    else:
        lb.config(text = "您没有选择任何文件夹");

def get_files():  #读取文件目录
    if not os.path.isdir(file_path):
        print("这不是一个文件夹")
        return
    global files
    files = os.listdir(file_path) 
    for index in range(len(files)):
        path = "%s/%s" %(file_path,files[index])
        if os.path.isdir(path):
            files[index] = ""#将文件夹对象设为空
        else:
            f_files.append(file_path+"/"+files[index])
            #调用函数
    #设置第一个查看的img
    for index in range(len(files)):
        if(files[index]):
            global img_showing
            img_showing = index
            break
     
    print(files)
    print(f_files)
    print(img_showing)
    return files 

def get_cuted_file(): #读取切图目录
    p_path = file_path+"/"+files[img_showing]
    d_path=p_path.split(".")[0]
    print(d_path)
    options  = os.listdir(d_path)
    global cut_img_showing
    cut_img_showing = 0
    for index in range(len(options)):
        cut_files.append(d_path+"/"+options[index])
    print(cut_files)
    print(cut_img_showing)
    return cut_files

  #读取所有切图：私以为可以在切换大图片时运行get_cuted_file来进行更新


def jump(): #跳过
    global img_showing
    global cut_img_showing
    print("JUMP:")
    print("jump前")
    print(img_showing)
    print(cut_img_showing)
    global delete_path
    d_path = (file_path+"/"+files[img_showing]).split(".")[0]
    options = os.listdir(d_path)
    delete_path = d_path+"/"+options[cut_img_showing]
    if options[cut_img_showing+1]:
        cut_img_showing=cut_img_showing+1
    else:
        while(img_showing<len(files)):
            img_showing = img_showing+1
            cut_img_showing=0
            if(files[img_showing+1]):
                break
            if(img_showing==len(files)):
                return -1 #表示已经遍历完成
    print("jump后")
    print(img_showing)
    print(cut_img_showing)

def delete():   #删除
    jump()
    os.remove(delete_path)
                        
                    

lb = Label(root,text = '')
lb.pack()
btn = Button(root,text="弹出选择文件对话框",command=xz)
btn1 = Button(root,text="get_files",command=get_files)
btn2 = Button(root,text="get_cuted_file",command=get_cuted_file)
btn3 = Button(root,text="jump",command=jump)
btn4 = Button(root,text="delete",command=delete)


btn.pack()
btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
root.mainloop()


