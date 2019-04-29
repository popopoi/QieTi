# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 18:17:16 2019

@author: HOLO
"""
import cv2
def crop_Tool(path,location_list):
    img = cv2.imread(path)
    i=0
    for location in location_list:
        cropped = img[location['top']:location['top']+location['height']
        , location['left']:location['left']+location['width']]
        savepath="./"+i+".jpg"
        cv2.imwrite(savepath, cropped)
    