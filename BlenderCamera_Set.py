import bpy
import mathutils
import math


# Camera set position, rotation
mat_loc = mathutils.Matrix.Translation((bpy.data.objects['PCB'].location[0], bpy.data.objects['PCB'].location[1], bpy.data.objects['PCB'].location[2]+800))
mat_sca = mathutils.Matrix.Scale(0.5, 4, (0.0, 0.0, 1.0))
mat_rot = mathutils.Matrix.Rotation(math.radians(0.0), 4, 'X')
mat_comb = mat_loc @ mat_rot @ mat_sca

cam = bpy.data.objects['Camera']
cam.matrix_world = mat_comb


#(bpy.data.objects['PCB'].location[0], bpy.data.objects['PCB'].location[1], bpy.data.objects['PCB'].location[2]))


# Set save path
sce = bpy.context.scene.name
bpy.data.scenes[sce].render.filepath = "C:\\Users\\simon\\Desktop\\temp_Panos\\Code\\blender_camera_view6.png"

# Go into camera-view (optional)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        break

# Render image through viewport
bpy.ops.render.opengl(write_still=True)

'''for ob in bpy.context.selected_objects:
    ob.select = False'''
    
