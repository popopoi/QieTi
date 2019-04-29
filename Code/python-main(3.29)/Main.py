#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:01:36 2019

@author: tt
"""

import temp
import JudgeTool as tool


def lookarea(examinations_area):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    for examination in examinations_area:
        print("**************************")
        for line in examination:
            print(line['words'])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^") 
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")   

def examinations_location_sort(examinations_area) :

    locations_list=[]
    locations={}
    for examination in examinations_area:
        maxwidth=0
        maxtop=0
        mintop=10086
        minleft=10086
        locations={}
        for line in examination:
            if(line['location']['width']>maxwidth):
                maxwidth=line['location']['width']
            if(line['location']['top']<mintop):
                mintop=line['location']['top']
            if(line['location']['top']>maxtop):
                maxtop=line['location']['top']
            if(line['location']['top']<minleft):
                minleft=line['location']['left']
        locations['width']=maxwidth
        locations['top']=mintop
        locations['left']=minleft
        locations['height']=maxtop-mintop
        locations_list.append(locations)
    return locations_list
        
"""
    遍历全部文本为题干还是其他，划分出每段文本所属的题目的函数
    in： results
    return ： examinations_result
    author ： Yuta Mizuki
"""
def JudgeFunction(results):
    #print(len(results['words_result']))#36条数据
   
    #examinations_area:总的存储所有处理后数据的list,
    #存储多个（多个result集合的题目区域）single_examination_area数组
    examinations_area=[]
    examinations_options_area=[]
    #single_examination_area:存储单个（多个result集合的题目区域）题目区域的数组
    #存储多个result（属于同一题的result），result:文本信息，包括文本内容和文本位置
    single_examination_area=[]#单个题目数据（文本／位置信息）的area
    single_examination_options_area=[]#单个题目选项（文本／位置信息）的area
    #examination_number:题目的数量
    examination_number=0
    #current_numberlevel:当前题号类型层次标示
    #current_numberstyle=0;#默认为0，即还没有分层。
    current_flag=0;#默认为0，当前层是否失效
    for i in range(len(results['words_result'])):
        result=results['words_result'][i]
        #print("[i]:",i,"  ",result['words'])
        #print(result['location'])
        isquestion,numberstyle,code=tool.question_JudgeTool(result['words'])
        if(code=="11" or code=="010"):
            current_flag=1
        if(code=="011" or code=="001"):
            current_flag=0  
        if(isquestion==True):
            print(result['words'],"###Yes###",code)
            '''是题干。考虑属于上级题目的情况（如 一、单项选择题），存在上下级时，忽略。TODO'''

            
            #考虑第一道题的情况，当之前没有题目area这是第一个时，直接将location信息添加到single_examination_area
            if(examination_number==0):  
                examination_number=examination_number+1
                single_examination_area.append(result)
            #如果不是第一题，那么先提交上一题的area到examinations_area，然后清空，然后再开始添加下一题的内容到single_examination_area
            elif(examination_number>=0):   
                if(numberstyle>5): 
                    single_examination_area.append(result)
                else:
                    examination_number=examination_number+1#将题目数加一
                    examinations_area.append(single_examination_area)#将上一single题的area提交
                    examinations_options_area.append(single_examination_options_area)#将上一single题的area提交
                    #lookarea(examinations_area)
                    single_examination_area=[]#提交后清空single题的存储
                    single_examination_options_area=[]#提交后清空single题的存储
                    single_examination_area.append(result)#将下一题 (也就是本行)添加到single题的area
                
        elif(isquestion==False):
            print(result['words'],"&&&NO&&&",code)
            '''不是题干,可能是题目的一部分(选择题选项／题干的非第一行/下级题目)，
            也可能完全不属于题目(如 考出风格／非题干的一部分)，
            '''
            if(current_flag==0):
                continue;
            
            single_examination_area.append(result)#添加到当前single题的area      
            
            #为选择题选项的情况
            if(code=="0001"):
                single_examination_options_area.append(result)#添加到当前single题选项的area  
                
            #考虑最后一行的情况，此时已经没有题干行进行判断一道题的area是否结束，
            #所以当最后一行时,直接进行area提交，结束
            if(i==(len(results['words_result'])-1)):
                
                examinations_area.append(single_examination_area)
                single_examination_area=[]
            else:
                continue
                
    print(examination_number)
    return examinations_area,examinations_options_area


filepath='/Users/tt/Desktop/pic/0011.jpg'
#results=temp.accurate_ocr(filepath)
results=temp.general_ocr(filepath)

r,op=JudgeFunction(results)

print()
print("*results are:")
lookarea(r)
print()
lookarea(op)

locations_list=examinations_location_sort(r)
print(locations_list)