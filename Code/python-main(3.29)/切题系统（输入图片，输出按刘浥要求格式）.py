#import sys

import numpy as np
import cv2

def test_detect (img_path):
    # 参考：https://blog.csdn.net/it2153534/article/details/79185397
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)#cv2.IMREAD_GRAYSCALE
    
    cv2.imshow("huiduhuahou",img)
    
    # 二值化图片
    ret,th=cv2.threshold(img,127,255,cv2.THRESH_BINARY)#ret是阈值，就是后面的100，th是产生的目标图像
    
    cv2.imshow("erzhihuahou",th)

#    the=cv2.medianblur(th,5)#中值滤波，输出是the图像
    
    kernel = np.ones((10,20),np.uint8)
    #返回uint8数据类型的一个[10，20]的元素全部为1的数组,kernel是一个卷积核，数组越大，一次腐蚀的范围就越大
    
    # 开运算,形态学针对的是二值图片
    closing = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    
    cv2.imshow("kaiyunsuanhou",closing)
    
    # 腐蚀,形态学针对的是二值图片
    kernel = np.ones((5,10),np.uint8)#返回uint8数据类型的一个[5，10]的元素全部为1的数组,kernel是一个卷积核
    dilation = cv2.erode(closing,kernel,iterations = 1)# 对图像进行1次腐蚀,就是将二值图像的是白色图像的边缘进行腐蚀掉
    
#    cv2.imshow("fushihou",dilation)
    
    #膨胀
#    kernel = np.ones((5,10),np.uint8)#返回uint8数据类型的一个[5，10]的元素全部为1的数组,kernel是一个卷积核
#    a = cv2.erode(dilation,kernel,iterations = 1)
    
#    cv2.imshow("pengzhanghou",a)
    
    
    
    
    
    
    
    
    
    
    
    
    a=[]#a列表，每个元素都是一个字典
    
    
    #  查找和筛选文字区域
    region = []
    #  查找轮廓
    img2,contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    #cv2.findContours()函数来查找检测物体的轮廓
    #第一个参数是，dilation是待处理图像，
    #第二个参数表示轮廓的检索模式，cv2.RETR_EXTERNAL表示只检测外轮廓，
    #cv2.RETR_LIST检测的轮廓不建立等级关系，cv2.RETR_CCOMP建立两个等级的轮廓，
    #cv2.RETR_TREE建立一个等级树结构的轮廓
    #第三个参数method为轮廓的近似办法，
    #cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1
    #cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    #cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
    
    
    #contour返回值：cv2.findContours()函数首先返回一个list，list中每个元素都是图像中的一个轮廓，矩形4个点
    #hierarchy:该函数还可返回一个可选的hiararchy结果，这是一个ndarray，其中的元素个数和轮廓个数相同，
    #每个轮廓contours[i]对应4个hierarchy元素hierarchy[i][0] ~hierarchy[i][3]，
    #分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号.
    
    
    cv2.imshow("shaixuanquyuhou",img2)
    
    
    # 利用以上函数可以得到多个轮廓区域，存在一个列表中。
    #  筛选那些面积小的
    for i in range(len(contours)):
        # 遍历所有轮廓
       
        cnt = contours[i]# cnt是一个点集,里面是矩形4个点，list中每个元素都是图像中的一个轮廓
        #print(cnt)
       
        area = cv2.contourArea(cnt)  # 计算该轮廓的面积
        

       
        if(area < 300):  # 面积小的都筛选掉(跳过)、这个300可以按照效果自行设置
             continue

        
        rect = cv2.minAreaRect(cnt)# 找到上述点集下最小面积的矩形，该矩形可能有方向
        
        # 打印出各个矩形四个点的位置
        #print ("rect is: ")
        #print (rect)
        #输出一个括号中包括三个值，第一个值返回矩形的中心点（x，y），
        #第二个值返回（长，宽），第三个值返回矩阵的旋转角度，
        #angel是由x轴逆时针转至W(宽)的角度
        

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #print(box)
        #输出矩阵四个点，分别是左下，左上，右上，右下
        
        
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        
        # 筛选那些太细的矩形，留下扁的
        if(height > width ):
            continue

        region.append(box)
        
        top=box[1][1]#计算出字典中top
        left=box[1][0]#计算出字典中left
    
        dictionary={'width':width,'top':top,'left':left,'height':height}
        #创建每个元素为一个字典
        
        a.append(dictionary)#把字典加入a列表中
        
        
        
    for i in range(len(a)):
            print(a[i])    
    #输出a
    
    
    color = cv2.cvtColor(dilation, cv2.COLOR_GRAY2RGB)#dilation是使用的图像，这里灰度转彩色，产生了color图像

    for box in region:
        cv2.drawContours(color, [box], 0, (0, 0, 255), 2)
        #cv2.drawContours在图像上绘制轮廓
        #第一个参数是指明在哪幅图像上绘制轮廓
        #第二个参数是轮廓本身，在Python中是一个list
        #第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
        
        
    #cv2.drawContours(color, [box1], 0, (0, 0, 255), 2)
    cv2.imshow('gray', color)
    cv2.imwrite(r'E:\testphoto\cun1.jpg',img2)#将文件处理好的图片存入该地址
    cv2.waitKey(0)#无限期等待输入
#    cv2.destroyAllWindows()
#    sys.exit()
    
    
    
    
    
if __name__ == '__main__':
    # test_detect('imgs/182019010306541866.png')
    test_detect(r'E:\testphoto\a.jpg')
    
    
    
    
    
    
    
    
    
    
