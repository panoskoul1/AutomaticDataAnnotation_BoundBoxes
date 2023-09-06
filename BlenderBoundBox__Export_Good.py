# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:42:38 2022

@author: Panos Koulountzios
"""

#Comments:
# Run the "blender.exe --background Arduino_Leonardo.blend --python 3.2\scripts\addons\Test_script_panos.py" 
# in the command prompt in the directory "C:\Program Files\Blender Foundation\Blender 3.2>" 

import bpy
import os
from mathutils import Vector

obj = bpy.context.scene.objects   

'''for attr in dir(obj):
    print(str(attr), getattr(obj, attr))'''

# Components=open('C:\\Users\\simon\\Desktop\\temp_Panos\\Arduino_Leonardo_Components2.txt','w')
BBox=open('C:\\Users\\simon\\Desktop\\temp_Panos\\Arduino_Leonardo_BBox2.txt','w')

for ob in bpy.context.scene.objects:
    #print(dir(ob.data))
    print("object name:  ", ob.data.name)


    # Components.write('\n'+"Name: "+ob.data.name+'\n')
    # Components.write("Loc: " + str((ob.location.x))  +" "+  str((ob.location.y))  +" "+  str((ob.location.z))+'\n')
    # Components.write("Dim: " + str((ob.dimensions.x))  +" "+  str((ob.dimensions.y))  +" "+  str((ob.dimensions.z)))
    
    bbox_corners = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    cnt=0
    BBox.write("object name:  "+ ob.data.name +'\n')
    for v in bbox_corners:
        print(v)
        BBox.write("Point "+str(cnt)+":"+" "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")
        cnt=cnt+1


    print("-----")
    
    
BBox.close()
# Components.close()