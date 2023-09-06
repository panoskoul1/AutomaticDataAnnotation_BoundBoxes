# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:42:38 2022

@author: panos
"""


#%%
#------------------------------------------------------------------------------
#--------------------------------------------------------APPs Functions section
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2, imutils
import pandas as pd
import numpy as np



class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):   
        global cnt
        cnt=0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2*536, 2*571)


        # Define Layouts
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")        


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")


        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")


        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")


        self.horizontalLayout_3.addLayout(self.horizontalLayout)
       
        
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        
        
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 2, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)


        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 6, 6)


        spacerItem = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)




        # Assign Widgets inside the Layouts
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("image")
        self.horizontalLayout_3.addWidget(self.label)
        
        
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.horizontalLayout_3.addWidget(self.verticalSlider)
        
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        
        
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
    
        
        self.box_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.box_2.setMinimum(-10000000000000001.175494)
        self.box_2.setPrefix('x_tr ')
        self.box_2.setObjectName("box_2")
        self.horizontalLayout_4.addWidget(self.box_2)
        
        
        self.box_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.box_3.setMinimum(-10000000000000001.175494)
        self.box_3.setPrefix('y_tr ')
        self.box_3.setObjectName("box_3")
        self.horizontalLayout_4.addWidget(self.box_3)
        
        
        self.box_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.box_4.setMinimum(-10000000000000001.175494)
        self.box_4.setPrefix('x_magn ')
        self.box_4.setObjectName("box_4")
        self.horizontalLayout_4.addWidget(self.box_4)
        
        
        self.box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.box.setMinimum(-10000000000000001.175494)
        self.box.setPrefix('y_magn ')
        self.box.setObjectName("box")
        self.horizontalLayout_4.addWidget(self.box)
        
        
        
        
        
        
        spacerItem = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        
        self.retranslateUi(MainWindow)
        self.verticalSlider.valueChanged['int'].connect(self.brightness_value)
        # self.verticalSlider_2.valueChanged['int'].connect(self.blur_value)
        self.pushButton.clicked.connect(self.savePhoto)
        self.pushButton_2.clicked.connect(self.loadImage)
        self.pushButton_3.clicked.connect(self.loadFile)
        self.pushButton_4.clicked.connect(self.boundbox_superposition)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Added code here
        self.filename = None # Will hold the image address location
        self.filename1 = None # Will hold the image address location
        self.brightness_value_now = 0 # Updated brightness value
        self.blur_value_now = 0 # Updated blur value
        self.tmp = None # Will hold the temporary image for display
        self.loc2=0
        self.x_magn=1
        self.y_magn=1
        self.x_tr=0
        self.y_tr=0
        self.loc2=[]
        self.loc1x=[]
        self.loc1y=[]     
        
        
    def loadImage(self):
        """ This function will load the user selected image
            and set it to label using the setPhoto function"""
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        m = cv2.imread(self.filename)
        self.image = cv2.imread(self.filename) 
        self.setPhoto(self.image)
        
    
    def setPhoto(self,image):
        """ This function will take image input and resize it 
            only for display purpose and convert it to QImage
            to set at the label."""
        self.tmp = image
        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
    
    
    def loadFile(self):
        """ This function will load the user selected file.
            The file loaded will be the.txt including the 
            bounding boxes coordinates exported through blender."""
        self.filename1 = QFileDialog.getOpenFileName(filter="File (*.*)")[0]
        file = open(self.filename1, mode = 'r')
        lines = file.readlines()
        comp=list()
        loc=list()
        for line in lines:
            if line.find("object name:")!=-1:
                comp_temp=line[int(line.find(' ')+1):int(len(line)-1)]
                if comp_temp.find('Camera')>=0 or comp_temp.find('Light') >=0:
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
        loc1.insert(0,"x",loc1x); loc1.insert(1,"y",loc1y); loc1.insert(2,"z",loc1z);
        loc2=[]
        k=0
        for i in range(0,int(len(loc)/8)):
            loc2.append({'name':comp[i][7:], 'p1':loc[k+0][1:], 'p2':loc[k+1+0][1:], 'p3':loc[k+4+0][1:], 'p4':loc[k+5+0][1:]})
            k=k+8
        print('Data transformation achieved. Data stored in lists\n')
        # print(loc2)
        self.loc2 = loc2
        self.loc1x = loc1x
        self.loc1y = loc1y


    def  get_img_points(self,img):
        import cv2
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
        # Loading PCB top layer image
        scale_width = 640/ img.shape[1]
        scale_height = 480/ img.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(img.shape[1] * scale)
        window_height = int(img.shape[0] * scale)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', window_width, window_height)
        #set mouse callback function for window
        cv2.setMouseCallback('image', mouse_callback)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        new_img=img[right_clicks[0][1]:right_clicks[1][1],right_clicks[0][0]:right_clicks[1][0]]
        return new_img    



    def boundbox_img2coord(self, img2):
        # dim=[image.shape[1],image.shape[0]]
        # image1 = np.zeros([image.shape[1],image.shape[0]])
        
        # For every colour . Every class of components needs to have a different colour
        # xrange=np.arange(0,out.shape[1]-1)
        # yrange=np.arange(0,out.shape[0]-1)
        # for y in xrange:
        #     for x in yrange:
        #         if cpxl=np.where(img[x][y][:3] == (255,0,255)) # USB

        
        loc1x = self.loc1x
        loc1y = self.loc1y
        loc2=self.loc2
        
        # from matplotlib import pyplot as plt
        # plt.figure(cnt);
        # plt.imshow(img)
        
        loc3=np.copy(loc2)
        
        img = cv2.imread(self.filename)
        for i in range(1,int(len(loc2))):
            # 
            x=int(round((float(loc3[i]['p1'][0])*self.image4.shape[1])/(max(loc1x)-min(loc1x))))
            y=int(round((abs(float(loc3[i]['p1'][1]))*self.image4.shape[0])/(max(loc1y)-min(loc1y))))
            w=int(round((float(loc3[i]['p4'][0])*self.image4.shape[1])/(max(loc1x)-min(loc1x))))
            h=int(round((abs(float(loc3[i]['p4'][1]))*self.image4.shape[0])/(max(loc1y)-min(loc1y))))
            # 
            if loc2[i]['name'].find('Header')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,0,255), 4)
                # 
                cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 0) & (img[:,:,2] == 255))     # Header
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]); 
                
            elif loc2[i]['name'].find('USB')==0:
                cv2.rectangle(img, (x, y), (w, h), (0,0,125), 4)
                # 
                cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 0) & (img[:,:,2] == 125))     # USB
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]);  loc2[i]['p1'][1] = np.min(cpxl[0]); 
                loc2[i]['p4'][0] =  np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);  
                
            elif loc2[i]['name'].find('Power_Jack')==0:
                cv2.rectangle(img, (x, y), (w, h), (240,240,240), 4)
                # 
                cpxl = np.where((img[:,:,0] == 240) & (img[:,:,1] == 240) & (img[:,:,2] == 240))     # power jack
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);    
                
            # elif loc2[i]['name'].find('Capacitor')==0:
            #     cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 125) & (img[:,:,2] == 0))     # Capacitor
            #     p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
            #     p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
            #     # assignment
            #     loc2[i]['p1'][0] = p1x;  loc2[i]['p1'][1] = p1y; 
            #     loc2[i]['p4'][0] = p2x;  loc2[i]['p1'][1] = p2y;         
            elif loc2[i]['name'].find('USB')==0:
                cv2.rectangle(img, (x, y), (w, h), (0,255,0), 4)
                # 
                cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 255) & (img[:,:,2] == 0))     # USB
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);      
                
            elif loc2[i]['name'].find('Resistor')==0:
                cv2.rectangle(img, (x, y), (w, h), (125,0,0), 4)
                # 
                cpxl = np.where((img[:,:,0] == 125) & (img[:,:,1] == 0) & (img[:,:,2] == 0))     # Resistor
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);    
                
            elif loc2[i]['name'].find('Inductance')==0:
                cv2.rectangle(img, (x, y), (w, h), (255,0,0), 4)
                # 
                cpxl = np.where((img[:,:,0] == 255) & (img[:,:,1] == 0) & (img[:,:,2] == 0))     # Inductance
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);     
                
            elif loc2[i]['name'].find('ic')==0:
                cv2.rectangle(img, (x, y), (w, h), (255,0,255), 4)
                # 
                cpxl = np.where((img[:,:,0] == 255) & (img[:,:,1] == 0) & (img[:,:,2] == 255))     # IC
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);   
                
            elif loc2[i]['name'].find('Oscillator')==0:
                cv2.rectangle(img, (x, y), (w, h), (0,255,255), 4)
                # 
                cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 255) & (img[:,:,2] == 255))     # IC
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);  
                
            elif loc2[i]['name'].find('SOT')==0:
                cv2.rectangle(img, (x, y), (w, h), (255,255,0), 4)
                # 
                cpxl = np.where((img[:,:,0] == 255) & (img[:,:,1] == 255) & (img[:,:,2] == 0))     # Transistor
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);   
                
            elif loc2[i]['name'].find('PushButoon')==0:
                cv2.rectangle(img, (x, y), (w, h), (0,0,0), 4)
                # 
                cpxl = np.where((img[:,:,0] == 0) & (img[:,:,1] == 0) & (img[:,:,2] == 0))     # Push Button
                p1x = np.min(cpxl[0]);   p1y = np.min(cpxl[1]);
                p2x = np.max(cpxl[0]);   p2y = np.max(cpxl[1]);
                # assignment
                loc2[i]['p1'][0] = np.min(cpxl[1]); loc2[i]['p1'][1] = np.min(cpxl[0]);
                loc2[i]['p4'][0] = np.max(cpxl[1]);  loc2[i]['p4'][1] = np.max(cpxl[0]);           
                
        # print(loc2)
        self.loc3=loc2
        



    def boundbox_superposition(self):
        global cnt
        if cnt == 0:
            # Load the input image and template from disk
            # Cropping
            template=cv2.imread('D:\\Work-FINDEN\\Work_files\\temp_Panos\\Code(copy)\\Code\\Labelled_blender_view.png')
            image2=cv2.imread(self.filename)
            image3=image2
            bound_box_img = np.zeros([image3.shape[1],image3.shape[0],3])
            # Resize
            dim=[image3.shape[1],image3.shape[0]]
            template2=cv2.resize(template, dim, interpolation = cv2.INTER_AREA)
            # Get PCB edges
            global right_clicks
            right_clicks = list()
            template3=self.get_img_points(template2)
            input_diag_pts = right_clicks
            del right_clicks
            right_clicks = list()
            image4=self.get_img_points(image3)
            output_diag_pts = right_clicks
            maxWidth = image3.shape[1]
            maxHeight= image3.shape[0]
            input_pts = np.float32([[input_diag_pts[0][0],input_diag_pts[0][1]],[input_diag_pts[1][0],input_diag_pts[0][1]],[input_diag_pts[1][0],input_diag_pts[1][1]], [input_diag_pts[0][0],input_diag_pts[1][1]]])
            output_pts = np.float32([[output_diag_pts[0][0],output_diag_pts[0][1]],[output_diag_pts[1][0],output_diag_pts[0][1]],[output_diag_pts[1][0],output_diag_pts[1][1]], [input_diag_pts[0][0],input_diag_pts[1][1]]])
            # Compute the perspective transform M
            M = cv2.getPerspectiveTransform(input_pts,output_pts)
            out = cv2.warpPerspective(template2,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
            cv2.imshow("Image", out)
            cv2.waitKey(0)
            # self.image=out
            # Stacked display
            # our first output visualization of the image alignment will be a side-by-side comparison of the output aligned image and the template
            # stacked = np.hstack([out, image3])
            # cv2.imshow("Image Alignment Stacked", stacked)
            # cv2.waitKey(0)
            # Assigning Bounding boxes
            xrange=np.arange(0,out.shape[1]-2)
            yrange=np.arange(0,out.shape[0]-2)
            for y in xrange:
                for x in yrange:
                    if (out[x][y][0]==0 and out[x][y][1]== 0 and out[x][y][2]==255):
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==0 and out[x][y][2]==125:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==240 and out[x][y][1]==240 and out[x][y][2]==240:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==125 and out[x][y][2]==255:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==255 and out[x][y][2]==0:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==125 and out[x][y][1]==0 and out[x][y][2]==0:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==255 and out[x][y][1]==0 and out[x][y][2]==0:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==255 and out[x][y][1]==0 and out[x][y][2]==255:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==255 and out[x][y][2]==255:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==255 and out[x][y][1]==255 and out[x][y][2]==0:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==0 and out[x][y][2]==0:
                        if x>10 & y>10:
                            image3[x][y]=out[x][y]
                            # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==125 and out[x][y][1]==125 and out[x][y][2]==125:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==125 and out[x][y][2]==125:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
                    elif out[x][y][0]==0 and out[x][y][1]==0 and out[x][y][2]==255:
                        image3[x][y]=out[x][y]
                        # bound_box_img[x][y] = out[x][y]
            cnt=cnt+1
    
            self.image6=bound_box_img
            self.image4=np.copy(image3)
            self.update(image3)
      
        else:

            img =  self.image6
            
            # from matplotlib import pyplot as plt
            # plt.figure(cnt);
            # plt.imshow(img)
            
            img2 = cv2.imread(self.filename)
            
            
            img3 = cv2.addWeighted(img, 1, img2, 1, 0)
            
        
                    
            cnt=cnt+1
            print(cnt)
            # self.loc4=loc2
            
            from matplotlib import pyplot as plt
            plt.figure(cnt+1);
            plt.imshow(img3)
            
            self.image4=img3
            self.update(img3)
            #     
    




            
           

        
    def brightness_value(self,value):
        """ This function will take value from the slider
            for the brightness from 0 to 99"""
        self.brightness_value_now = value
        print('Brightness: ',value)
        self.update(self.image)
        
    
    def changeBrightness(self,img,value):
        """ This function will take an image (img) and the brightness
            value. It will perform the brightness change using OpenCv
            and after split, will merge the img and return it."""
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return img
        
    
    def update(self,img):
        """ This function will update the photo according to the 
            current values of blur and brightness and set it to photo label."""
        self.image = img
        self.image = self.changeBrightness(self.image,self.brightness_value_now)
        self.setPhoto(self.image)

    
    def savePhoto(self):
        """ This function will save the image"""
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',self.filename)
    
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Panos App"))
        self.pushButton_2.setText(_translate("MainWindow", "Open Image"))
        self.pushButton_3.setText(_translate("MainWindow", "Open File"))
        self.pushButton_4.setText(_translate("MainWindow", "Bound. Boxes fit"))                
        self.pushButton.setText(_translate("MainWindow", "Save"))


#------------------------------------------------------------------------------
#-------------------------------------------------Operational Functions section
#--------------------------MAIN-----------------------------------------------#


#--------------------------------------------------------------------------MAIN
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


