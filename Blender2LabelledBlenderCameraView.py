# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 22:18:33 2022

@author: Panos Koulountzios
"""

#%%  
import numpy as np
import cv2
import pandas as pd

right_clicks = list()
def  crop_img(img):
    import os
    import cv2
    import urllib
    import cv2
    from win32api import GetSystemMetrics
    import argparse
    # 
    #the [x, y] for each right-click event will be stored here
    #this function will be called whenever the mouse is right-clicked
    def mouse_callback(event, x, y, flags, params):
        #right-click event value is 2
        if event == 2:
            global right_clicks
            #store the coordinates of the right-click event
            right_clicks.append([x, y])
            #this just verifies that the mouse data is being collected
            #you probably want to remove this later
            print(right_clicks) 
    # 
    # Loading PCB top layer image
    scale_width = 640 / img.shape[1]
    scale_height = 480 / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)
    #set mouse callback function for window
    points=cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #
    new_img=img[right_clicks[0][1]:right_clicks[1][1],right_clicks[0][0]:right_clicks[1][0]]
    '''cv2.imshow('new image', new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)'''
    #
    return new_img







#%%
# Load .txt file
filename='D:\\Work-FINDEN\\Work_files\\temp_Panos\\Code\\boundboxing_fitting_code\\GUI_App\\Arduino_Leonardo_BBox2.txt'
file = open(filename, mode = 'r')
lines = file.readlines()

comp=list()
loc=list()
for line in lines:
    if line.find("object name:")!=-1:
        comp_temp=line[int(line.find(' ')+1):int(len(line)-1)]
        if comp_temp.find('Camera')>=0 or comp_temp.find('Light')>=0:
            continue
        else:
            comp.append(comp_temp)
    if line.find("Point")!=-1:
        points_temp=line[int(line.find(' ')+1):int(len(line)-1)]
        tmp=points_temp.split(' ')
        if comp_temp.find('Camera')>=0 or comp_temp.find('Light')>=0:
            continue
        else:
            loc.append(tmp)
loc1 = pd.DataFrame()
loc1x=np.zeros(len(loc)); loc1y=np.zeros(len(loc)); loc1z=np.zeros(len(loc))
cnt=0
for a in loc :
    loc1x[cnt]=(a[1])
    loc1y[cnt]=(a[2])
    loc1z[cnt]=(a[3])
    cnt=cnt+1
# Shifting the points to positive quadrant
loc1y=abs(loc1y)
loc1x=loc1x
minx=min(loc1x); loc1x=loc1x+abs(minx) if minx<0 else loc1x
miny=min(loc1y); loc1y=loc1y+abs(miny) if miny<0 else loc1y
minz=min(loc1z); loc1z=loc1z+abs(minz) if minz<0 else loc1z
# 
loc1.insert(0,"x",loc1x); loc1.insert(1,"y",loc1y); loc1.insert(2,"z",loc1z);
#
loc2=[]
k=0
for i in range(0,int(len(loc)/8)):
    loc2.append({'name':comp[i][7:], 'p1':loc[k+0][1:], 'p2':loc[k+1+0][1:], 'p3':loc[k+4+0][1:], 'p4':loc[k+5+0][1:]})
    k=k+8

#%  
# Loading PCB top layer image
filename = 'D:\\Work-FINDEN\\Work_files\\temp_Panos\\Code\\Cropped_Image8.png'
# filename = 'D:\\Work-FINDEN\\Work_files\\temp_Panos\\Code\\blender_camera_view4.png'
img = cv2.imread(filename, -1)
#
# right_clicks = list()
# img2=crop_img(img)
img2=img
#
boundboxes=[]
for i in range(1,int(len(loc2))):
    
    # Scale the points
    x=round(((float(loc2[i]['p1'][0])-min(loc1x))*img2.shape[1])/(max(loc1x)-min(loc1x)))
    w=round(((float(loc2[i]['p4'][0])-min(loc1x))*img2.shape[1])/(max(loc1x)-min(loc1x)))
    y=round(((abs(float(loc2[i]['p1'][1]))-min(loc1y))*img2.shape[0])/(max(loc1y)-min(loc1y)))
    h=round(((abs(float(loc2[i]['p4'][1]))-min(loc1y))*img2.shape[0])/(max(loc1y)-min(loc1y)))
    
    k=[0,0,0]
    # Add bounding box
    if loc2[i]['name'].find('Header')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,0,255), 4)
        list_temp=[x,y,h,w,[0,0,255]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('USB')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,0,125), 4)
        list_temp=[x,y,h,w,[0,0,125]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Power_Jack')==0:
        cv2.rectangle(img2, (x, y), (w, h), (240,240,240), 4) 
        list_temp=[x,y,h,w,[240,240,240]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Capacitor')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,125,0), 4) 
        list_temp=[x,y,h,w,[0,125,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('USB')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,255,0), 4) 
        list_temp=[x,y,h,w,[0,255,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('4xResistor')==0:
        cv2.rectangle(img2, (x, y), (w, h), (125,0,0), 4) 
        list_temp=[x,y,h,w,[125,0,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Resistor')==0:
        cv2.rectangle(img2, (x, y), (w, h), (125,0,0), 4)
        list_temp=[x,y,h,w,[125,0,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Inductance')==0:
        cv2.rectangle(img2, (x, y), (w, h), (255,0,0), 4) 
        list_temp=[x,y,h,w,[255,0,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('IC_Atmel')==0:
        cv2.rectangle(img2, (x, y), (w, h), (255,0,255), 4) 
        list_temp=[x,y,h,w,[255,0,255]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('ic')==0:
        cv2.rectangle(img2, (x, y), (w, h), (255,0,255), 4) 
        list_temp=[x,y,h,w,[255,0,255]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Oscillator')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,255,255), 4) 
        list_temp=[x,y,h,w,[0,255,255]] 
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('SOT23')==0:
        cv2.rectangle(img2, (x, y), (w, h), (255,255,0), 4) 
        list_temp=[x,y,h,w,[255,255,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('PushButton')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,0,0), 4)
        list_temp=[x,y,h,w,[0,0,0]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('DIODE')==0:
        cv2.rectangle(img2, (x, y), (w, h), (125,125,125), 4) 
        list_temp=[x,y,h,w,[125,125,125]]
        cv2.rectangle(img2, (x, y), (w, h), k, 4)
        list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('DEL')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,125,125), 4) 
        list_temp=[x,y,h,w,[0,125,125]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('Part_feature')==0:
        cv2.rectangle(img2, (x, y), (w, h), (0,125,125), 4) 
        list_temp=[x,y,h,w,[0,125,125]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    elif loc2[i]['name'].find('fuse')==0:
        cv2.rectangle(img2, (x, y), (w, h), (125,125,125), 4)
        list_temp=[x,y,h,w,[125,125,125]]
        # cv2.rectangle(img2, (x, y), (w, h), k, 4)
        # list_temp=[x,y,h,w,k]
    boundboxes.append(list_temp)
    
    
list_temp=[img2.shape[1],img2.shape[0]]
boundboxes.append(list_temp)


# Resize image
dim=[img2.shape[1]*1,img2.shape[0]*1]
img3 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
        

# Display image
cv2.imshow('asd',img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('D:\\Work-FINDEN\\Work_files\\temp_Panos\\Code\\boundboxing_fitting_code\\Labelled_blender_view3.png', img3)









