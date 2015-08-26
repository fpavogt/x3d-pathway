# -*- coding: utf-8 -*-
# If you find this code useful for your research, please cite the following 
# article accordingly:
#
# Vogt, Owen et al., Advanced Data Visualization in Astrophysics: 
# the X3D Pathway, ApJ (2015).
#
#    Copyright (C) 2015  Frédéric P.A. Vogt, Chris I. Owen
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import bpy, math

"""
This is a simple Blender script to import an X3D mesh of a green dice.
It sets up a typical Blender scene, imports an X3D mesh, applies some simple 
materials, and sets up a simple animation.
"""

###########################################
## Define file locations and directories ##
###########################################

X3D_location = "/Volumes/Flash/green_dice.x3d"
# Rendered frames output location.
bpy.data.scenes["Scene"].render.filepath = "/Volumes/Flash/green_dice/"	

############################
## Initial setup of scene ##
############################

# Remove default objects

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
bpy.ops.object.select_all(action="DESELECT")

# We'll use the Cycles rendering engine

bpy.data.scenes["Scene"].render.engine = "CYCLES"

# Set background world color

bpy.data.worlds["World"].horizon_color = [0.5, 0.5, 0.5]

# Use a global ambient occlusion lighting to brighten the scene a bit

bpy.data.worlds["World"].light_settings.use_ambient_occlusion = True
bpy.data.worlds["World"].light_settings.ao_factor = 0.1

#######################
## Add scene objects ##
#######################

# Import X3D file

bpy.ops.import_scene.x3d(filepath=X3D_location)

# Note that this X3D file contains the required objects, and also some other 
# unwanted objects from MayaVI.  This includes the MayaVI viewport camera and 
# some lamps.  We will delete these and keep only the dice.

# "ShapeIndexedFaceSet" is the default name for imported X3D meshes.
dice = bpy.data.objects["ShapeIndexedFaceSet"]  
dice.name = "Dice" # We should rename to something more human friendly

spheres = bpy.data.objects["ShapeIndexedFaceSet.001"]
spheres.name = "Spheres"

# The "Spheres" exported from MayaVI have a low number of polygons.  
# To make them look a bit prettier we'll apply a quick subsurface modifier.
# They're not really spheres though, so they'll still be a bit lumpy.  
# Adds character to the scene. :)
spheres.modifiers.new("subd", type="SUBSURF")
spheres.modifiers["subd"].levels = 3
spheres.modifiers["subd"].render_levels = 3

# Remove all the other unwanted objects imported in the X3D file
bpy.ops.object.select_all(action="DESELECT")

for obj in bpy.data.objects[:]:
	if obj.name not in ["Dice", "Spheres"]:
		bpy.data.objects[obj.name].select = True	
		bpy.ops.object.delete()		

# Import flat plane for dice to sit above
bpy.ops.mesh.primitive_plane_add(radius=100)
plane = bpy.data.objects["Plane"]

plane.location = [0.0, 0.0, -0.7]

# Add a point lamp
bpy.ops.object.lamp_add(type="POINT")
lamp = bpy.data.objects["Point"]

lamp.location = [2.0, 1.0, 3.0]
# Set lamp brightness value
lamp.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 300.0  

# Add a camera
bpy.ops.object.camera_add()
camera = bpy.data.objects["Camera"]

camera.location = [2.0, -2.0, 2.75]
camera.rotation_euler = [math.radians(45.0), 0.0, math.radians(45.0)]


############################################################
## Create some simple materials and assign to our objects ##
############################################################

## Spheres and plane materia - the default Cycles material ##

"""
For simplicity, we won't bother to add a material to the "Spheres" or "Plane" 
objects. The default Cycles material is an off-white diffuse shader, perfect for 
both of these objects. So we don't have to do anything for these two!
"""

## Dice material - a simple green diffuse material ##
# For the dice material we will use the default Cycles material but simply 
# colour it green.

# Create the new material

mat = bpy.data.materials.new("DiceMaterial")
mat.use_nodes = True

# Change the default off-white RGB colour to a pure green

mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = \
                                                (0.0,1.0,0.0,1.0) # Green colour

# Remove any default material already associated with the object
for i in range(len(bpy.data.objects["Dice"].data.materials[:])):
	bpy.data.objects["Dice"].data.materials.pop()
	
# And make sure our new material is attached to the dice
bpy.data.objects["Dice"].data.materials.append(mat) 


###############
## Animation ##
###############

# For our animation we'll make the camera do a 360 degree spin around the centre 
# of the dice.

# First, we'll create an "empty" object at the centre of the scene - this will 
# control the camera's rotation.

bpy.ops.object.empty_add(type="PLAIN_AXES")
bpy.data.objects["Empty"].name = "CameraControl"

# Now we'll parent the Camera to the CameraControl object.  
# Any location/rotation/scale operation applied to the CameraControl will also 
# be applied to the Camera.

bpy.data.objects["Camera"].parent = bpy.data.objects["CameraControl"]

# Now we'll animate the CameraControl to rotate 360 degrees around the Z axis.
# The default frames-per-second is 24, so we'll make a 5 second animation 
# (5 * 24 = 120 frames)

# Set the animation range
bpy.data.scenes["Scene"].frame_start = 1
bpy.data.scenes["Scene"].frame_end = 120

# Make sure only the CameraControl is selected
bpy.ops.object.select_all(action="DESELECT")
bpy.data.objects["CameraControl"].select = True

# Add the first animation keyframe
bpy.data.scenes["Scene"].frame_current = 1
bpy.ops.anim.keyframe_insert(type='Rotation',confirm_success=False)

# Add the second animation keyframe
# We want the 121th frame to be the 360th degree to make sure frame 1 and 120 
# are not identical.
bpy.data.scenes["Scene"].frame_current = 121		
bpy.data.objects["CameraControl"].rotation_euler = [0.0,0.0,math.radians(360.0)]
bpy.ops.anim.keyframe_insert(type='Rotation',confirm_success=False)

# The animation is interpolated between these two keyframes.  You get a choice 
# of what kind of interpolation to use.The default uses Bezier curves in order 
# to accelerate and decelerate the motion. We want a smooth linear motion here, 
# so we'll change the interpolation for each keyframe to "linear".

for curves in bpy.data.objects["CameraControl"].animation_data.action.fcurves:
	for kfs in curves.keyframe_points:
		kfs.interpolation = "LINEAR"


##############################
## Set some render settings ##
##############################

bpy.data.scenes["Scene"].render.resolution_x = 1280
bpy.data.scenes["Scene"].render.resolution_y = 720
bpy.data.scenes["Scene"].render.resolution_percentage = 100
bpy.data.scenes["Scene"].render.image_settings.compression = 100
# The "quality" of the render. More samples means less noise, but longer 
# render time.
bpy.data.scenes["Scene"].cycles.samples = 125
# Clamps the indirect light rays.  Reduces noise at the cost of the accuracy of 
# bounced light.
bpy.data.scenes["Scene"].cycles.sample_clamp_indirect = 0.5
# The render tile sizes.  Smaller tiles render faster, but at the cost of 
# additional overhead for swapping more tiles.  For typical CPU rendering on my 
# Macbook Pro, 32 is a good size.
bpy.data.scenes["Scene"].render.tile_x = 32
bpy.data.scenes["Scene"].render.tile_y = 32					

# If you're looking for something a tiny bit more fancy to add to the fluidity 
# of the animation, try switching on motion blur
#bpy.data.scenes["Scene"].render.use_motion_blur = True

# READY TO RENDER! #

