#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:01:36 2019

@author: tt
"""

import temp
import JudgeTool as tool
filepath='/Users/tt/Desktop/timg.jpg'
print("temp.py test")
results=temp.accurate_ocr(filepath)


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
    #single_examination_area:存储单个（多个result集合的题目区域）题目区域的数组
    #存储多个result（属于同一题的result），result:文本信息，包括文本内容和文本位置
    single_examination_area=[]#单个题目数据（文本／位置信息）的area
    #examination_number:题目的数量
    examination_number=0
    #current_numberlevel:当前题号类型层次标示
    current_numberstyle=0;#默认为0，即还没有分层。
    #current_flag=0;#默认为0，当前层是否失效
    for i in range(len(results['words_result'])):
        result=results['words_result'][i]
        #print("[i]:",i,"  ",result['words'])
        #print(result['location'])
        isquestion,numberstyle,code=tool.question_JudgeTool(result['words'])
        '''if(numberstyle>current_numberstyle):
            #进入了大题中的小题
            current_numberstyle=numberstyle
        if(numberstyle<current_numberstyle):
            #可能是到下一大题了
            current_numberstyle=numberstyle'''
        '''if(code=404):
            
            continue'''

        if(isquestion=="YES"):
            '''是题干。考虑属于上级题目的情况（如 一、单项选择题），存在上下级时，忽略。TODO'''
            #考虑第一道题的情况，当之前没有题目area这是第一个时，直接将location信息添加到single_examination_area
            if(examination_number==0):    
                single_examination_area.append(result)
            #如果不是第一题，那么先提交上一题的area到examinations_area，然后清空，然后再开始添加下一题的内容到single_examination_area
            elif(examination_number!=0):   
                if(current_numberstyle==numberstyle):
                    if(numberstyle<=5):
                        examinations_area.append(single_examination_area)#将上一single题的area提交，开始下一题的area的识别收集
                        examination_number=examination_number+1#将题目数加一
                        single_examination_area.clear()#提交后清空single题的存储空间
                    elif(numberstyle>5):
                        single_examination_area.append(result)#将本行添加到single题的area
                elif(numberstyle>current_numberstyle):
                    if(numberstyle>5):
                        single_examination_area.append(result)#将本行添加到single题的area
                    elif(numberstyle<=5):
                        single_examination_area.clear()#先清空single题的存储空间
                        single_examination_area.append(result)#再将本行添加到single题的area
                elif(numberstyle<current_numberstyle):
                    current_numberstyle=numberstyle
                
                single_examination_area.append(result)#将下一题 (也就是本行)添加到single题的area
                    
                    
                        
                        
        elif(isquestion=="NO"):
            '''不是题干,可能是题目的一部分(选择题选项／题干的非第一行/下级题目)，
            也可能完全不属于题目(如 考出风格／非题干的一部分)，
            '''
            '''TODO'''
            single_examination_area.append(result)#添加到当前single题的area
            #考虑最后一行的情况，此时已经没有题干行进行判断一道题的area是否结束，
            #所以当最后一行时,直接进行area提交，结束
            if(i==(len(results['words_result'])-1)):
                examinations_area.append(single_examination_area)
                single_examination_area.clear()
            else:
                continue
                
    return examinations_area
print(JudgeFunction(results))