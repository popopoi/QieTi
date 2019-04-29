#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:00:32 2019

@author: tt
"""
import re

            
'''
    判断一句话是否为疑问句／命令句／是非判断句的函数
    return ：True／False
    author ：poi
'''           
#判断一句话是否为疑问句／命令句／是非判断句的函数
def questionemotion_JudgeTool(textcontent):

    interrogtive_dict=['吗\?','(有|是)哪[些里]','(有|要)(几|多少)(些|种|分钟|时间|千克|米|吨|本|万)','如何.*(定义|进行|处理)','(什么|何).*(问题|区别|不同|作用|原因)',
                       '(为|是|有)(什么|何|多少)','请问.(怎么|区别是|看法是|多长时间)','怎样.*(理解|处理)','(问|检验.*(差异|差别|影响))']#疑问句
    imperative_dict=['\。','请.*(辨析|解释)','求.*(概率|解|面积|值)','求解.*问题','则.*为','一项是','阅读.*[“回答”,“完成”]','简要说明.*区别',
                     '归纳.主要内容','概[述|论].*(历史意义|作用)','证明','[综结]合.*(体会|理解)','请你.应该是','恰当的是','其中.*是','下列.*是','根据.*给',
                     '[句文词].*[默填]写','的(主要内涵|基本标准)','(简析|简述|分析|解释|试论).*(原因|好处|历史条件|程序|流程|意义|产生|应用|内容|影响|策略)',
                     '试加以说明','简要描述','指出.*方面']#命令句
    copulative_dict=['判断','是否','正确.*的是','错误.*的是']#是非判断句
    
    key=textcontent
    for p in interrogtive_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            print(res)
            return True
    for p in copulative_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            print(res)
            return True
    for p in imperative_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            print(res)
            return True
    return False


'''
    判断是否有题号，以及题号的类型的函数
    return ：True／False,numberstyle(1,2,3,4,5,6,7,0),code
    author ：Yuta Mizuki
'''
def index_of_str(s1, s2):
    lt=s1.split(s2,1)
    if len(lt)==1:
        return -1
    return len(lt[0])
#判断是否有题号，以及题号的类型的函数
def questionnumber_JudgeTool(textcontent):

    questionnumber_dict=["[一二三四五六七八九十]+、","[一二三四五六七八九十]+\.","[0-9]+\.","[0-9]+、"
                         ,"[Ee][Gg].[0-9]+","\([0-9]+\)","\([一二三四五六七八九十]+\)"]
    key=textcontent
    i=0
    for p in questionnumber_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        print(res)
        i=i+1
        if(len(res)==0):
            continue
        elif(len(res)==1):
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"666"
            else:
                return False,i,"404"
        else:
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"404"
            else:
                return False,i,"404" 
    return False,0,"505"





'''
    判断一句话是否为选择题选项的函数
    判断是否为A.,B.,C.,D.开头，并与后三句话进行匹配
        达成A，B，C，D／A,B,C/a,b,c,d/a,b,c认为是选择题的选项
    return ：True／False,ABCDstyle(0 or 1 or 2 or 3 or 4),code(标示码)
    author ：Yuta Mizuki

'''  
#判断是否为选择题的选项的函数
def option_JudgeTool(textcontent):
    option_dict=["[Aa]\.","[Bb]\.","[Cc]\.","[Dd]\."]
    key=textcontent
    i=0
    for p in option_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        print(res)
        i=i+1
        if(len(res)==0):
            continue
        elif(len(res)==1):
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"666"
            else:
                return False,i,"404"
        else:
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"404"
            else:
                return False,i,"404" 
    return False,0,"505"

'''
    判断一句话是否为考试注意事项的函数

    return ：True／False,code(标示码)
    author ：Yuta Mizuki

'''   
def note_JudgeTool(textcontent):
    note_dict=["本试题.部分","签字笔.答题卡","答题区域","(切记不要｜切忌).答题"]
    key=textcontent
    i=0
    for p in note_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        print(res)
        i=i+1
        if(len(res)==0):
            continue
        elif(len(res)==1):
                return True,"666"
        else:
            return True,"404"
    return False,"505"

'''
    判断一句话是否为题干的函数
    主要考虑到文本语气／题号及其位置／(选项判断及其位置)
    in ：textcontent (result['words'])
    return ："YES"(确认是题干)/"NO"(不确认是题干)，numberstyle（题号的类型）,code(标示码)
    code：404:存在题号，没有问题情感，可能是注意事项之类的／也可能是判断题的陈述
          505:不存在题号，也没有问题情感，也不属于选择项
          
    author ：Yuta Mizuki
'''
def question_JudgeTool(textcontent):
    x=textcontent
    #判断是否为疑问／命令／是非判断
    isorder=questionemotion_JudgeTool(x)
    #判断是否有题号，以及题号的类型
    hasquestionnumber,numberstyle,code=questionnumber_JudgeTool(x)
            
    if(isorder==True):
        '''初步认为是可能为疑问的题干。但也有可能是阅读题中的反问或者是选择题选项中的问句'''
        if(hasquestionnumber==True):
            return "YES",numberstyle,"11"
        else:
            if(option_JudgeTool(x)==True):
                return "NO",0,"101"
            else:
                return "YES",numberstyle,"100"
    elif(isorder==False):
        '''初步认为不为疑问／命令／是非判断。但也有可能是判断题中的陈述句。'''
        if(hasquestionnumber==True):
            '''有题号，所以大致认为是一道题里面的内容'''
            if(note_JudgeTool(x)==True):
                return "NO",0,"011"
            else:
                return "NO",0,"010"
        else:
            '''既没有题干语气，又没有题号，最难判断的一类。不出意外就是需要忽略的内容'''
            if(option_JudgeTool(x)==True):
                return "NO",0,"001"
            else:
                return "NO",0,"000"
            