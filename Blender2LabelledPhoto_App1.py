# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:42:38 2022

@author: Panos Koulountzios
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
      
        # ---Define Grids 
       self.centralwidget = QtWidgets.QWidget(MainWindow)
       self.centralwidget.setObjectName("centralwidget")
       
       
       self.gridLayout = QtWidgets.QGridLayout()
       self.gridLayout.setObjectName("gridLayout")

       self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
       self.gridLayout_2.setObjectName("gridLayout_2")
       
       
       # Define Layouts 
       self.horizontalLayout = QtWidgets.QHBoxLayout()
       self.horizontalLayout.setObjectName("horizontalLayout")        

       self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
       self.horizontalLayout_2.setObjectName("horizontalLayout_2")

       self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
       self.horizontalLayout_3.setObjectName("horizontalLayout_3")

       self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
       self.horizontalLayout_4.setObjectName("horizontalLayout_4")

       self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
       self.horizontalLayout_5.setObjectName("TextAppDescription")  
       
       self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
       
       self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 2, 2)

       self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

       self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 6, 6)
       
       self.gridLayout.addLayout(self.horizontalLayout_5, 10, 0, 7, 7)
       
       spacerItem = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
       self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)


       # ---Assign Widgets inside the Layouts
       self.label = QtWidgets.QLabel(self.centralwidget)
       self.label.setText("")
       self.label.setObjectName("image")
       self.horizontalLayout_3.addWidget(self.label)
            
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
       self.box_2.setPrefix('translate x: ')
       self.box_2.setObjectName("box_2")
       self.horizontalLayout_4.addWidget(self.box_2)
             
       self.box_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
       self.box_3.setMinimum(-10000000000000001.175494)
       self.box_3.setPrefix('translate y: ')
       self.box_3.setObjectName("box_3")
       self.horizontalLayout_4.addWidget(self.box_3)       
       
       self.box_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
       self.box_4.setMinimum(-10000000000000001.175494)
       self.box_4.setPrefix('multiple x: ')
       self.box_4.setObjectName("box_4")
       self.horizontalLayout_4.addWidget(self.box_4)

       self.box = QtWidgets.QDoubleSpinBox(self.centralwidget)
       self.box.setMinimum(-10000000000000001.175494)
       self.box.setPrefix('multiple y: ')
       self.box.setObjectName("box")
       self.horizontalLayout_4.addWidget(self.box)


       self.line = QtWidgets.QLabel("Hello! At first you can load an PCB's image file. Use 'Open Image' box.")
       # self.line.setPrefix('x_magn ')
       self.line.setObjectName("line")
       self.horizontalLayout_5.addWidget(self.line)
       
     
     
       MainWindow.setCentralWidget(self.centralwidget)
       self.statusbar = QtWidgets.QStatusBar(MainWindow)
       self.statusbar.setObjectName("statusbar")
       MainWindow.setStatusBar(self.statusbar)
       
       
       self.retranslateUi(MainWindow)
       self.pushButton.clicked.connect(self.savePhoto)
       self.pushButton_2.clicked.connect(self.loadImage)
       self.pushButton_3.clicked.connect(self.loadFile)
       self.pushButton_4.clicked.connect(self.boundbox_superposition)

       QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
        
       # ---Added code here
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
        global tmp1
        m = cv2.imread(self.filename)
        tmp1 = m
        self.update_message("PCB's image loaded. Time to load the .txt component file. Use 'open file' button.")
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
        self.update_message('File loaded. Time to set the scaling variables (translate x/y, multiple x/y).\n'\
                            'First set "multiple x = 1"  and  "multiple y = 1". Then press the "Bound. Boxes fit"'\
                            'button to paste the bound. boxes on the image.\n Continue playing with'\
                            'the variables values to perfectly fit the boxes.\n When you finish save the image.')
        self.loc2 = loc2
        self.loc1x = loc1x
        self.loc1y = loc1y
    
    def boundbox_superposition(self):
        im=cv2.imread(self.filename)
        loc2 = self.loc2
        loc1x = self.loc1x
        loc1y = self.loc1y
        y_magn=self.box.value()
        x_magn=self.box_4.value()
        x_tr=self.box_2.value()
        y_tr=self.box_3.value()
        # 
        print(x_magn)
        print(y_magn)
        print(x_tr)
        print(y_tr)        
        img2=im
        for i in range(1,int(len(loc2))):
            x=int(round((float(loc2[i]['p1'][0])*img2.shape[1])/(max(loc1x)-min(loc1x))*y_magn)+x_tr)
            y=int(round((abs(float(loc2[i]['p1'][1]))*img2.shape[0])/(max(loc1y)-min(loc1y))*x_magn)+y_tr)
            w=int(round((float(loc2[i]['p4'][0])*img2.shape[1])/(max(loc1x)-min(loc1x))*y_magn)+x_tr)
            h=int(round((abs(float(loc2[i]['p4'][1]))*img2.shape[0])/(max(loc1y)-min(loc1y))*x_magn)+y_tr)
            # 
            if loc2[i]['name'].find('Header')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,0,255), 2)
            elif loc2[i]['name'].find('USB')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,0,125), 2)      
            elif loc2[i]['name'].find('Power_Jack')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,0,0), 2) 
            elif loc2[i]['name'].find('Capacitor')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,125,0), 2) 
            elif loc2[i]['name'].find('USB')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,255,0), 2) 
            elif loc2[i]['name'].find('4xResistor')==0:
                cv2.rectangle(img2, (x, y), (w, h), (125,0,0), 2) 
            elif loc2[i]['name'].find('Resistor')==0:
                cv2.rectangle(img2, (x, y), (w, h), (125,0,0), 2)
            elif loc2[i]['name'].find('Inductance')==0:
                cv2.rectangle(img2, (x, y), (w, h), (255,0,0), 2) 
            elif loc2[i]['name'].find('IC_Atmel')==0:
                cv2.rectangle(img2, (x, y), (w, h), (255,0,255), 2) 
            elif loc2[i]['name'].find('ic')==0:
                cv2.rectangle(img2, (x, y), (w, h), (255,0,255), 2) 
            elif loc2[i]['name'].find('Oscillator')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,255,255), 2) 
            elif loc2[i]['name'].find('SOT23')==0:
                cv2.rectangle(img2, (x, y), (w, h), (255,255,0), 2) 
            elif loc2[i]['name'].find('PushButton')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,0,0), 2)
            elif loc2[i]['name'].find('DIODE')==0:
                cv2.rectangle(img2, (x, y), (w, h), (125,125,125), 2) 
            elif loc2[i]['name'].find('DEL')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,125,125), 2) 
            elif loc2[i]['name'].find('Part_feature')==0:
                cv2.rectangle(img2, (x, y), (w, h), (0,125,125), 2) 
            elif loc2[i]['name'].find('fuse')==0:
                cv2.rectangle(img2, (x, y), (w, h), (125,125,125), 2)
        self.update(img2)
               
    
    # def changeBrightness(self,img,value):
    #     """ This function will take an image (img) and the brightness
    #         value. It will perform the brightness change using OpenCv
    #         and after split, will merge the img and return it."""
    #     hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #     h,s,v = cv2.split(hsv)
    #     lim = 255 - value
    #     v[v>lim] = 255
    #     v[v<=lim] += value
    #     final_hsv = cv2.merge((h,s,v))
    #     img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
    #     return img
        
    
    def update(self,img):
        """ This function will update the photo """
        img1 = img
        # img1 = self.changeBrightness(img,self.brightness_value_now)
        self.setPhoto(img1)

    
    def savePhoto(self):
        """ This function will save the image"""
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',self.filename)
    
    
    def update_message(self,msg):
        """ This function will update AppDescription message """
        # self.line = QtWidgets.QLabel(msg)
        self.line.setText(msg)
        
    
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
    
    
    
    
    
    
