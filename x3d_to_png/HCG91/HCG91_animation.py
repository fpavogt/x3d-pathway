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
from mathutils import Vector

"""
This script imports an X3D file created with Python (MayaVI) which contains 
several 3D density contours of HI gas from HCG91 as observed by the VLA.  
A simple rotation animation is automatically produced.
"""

###########################################
## Define file locations and directories ##
###########################################

X3D_location = "/Volumes/Flash/automated/HCG91.x3d"
output_raw_dir = "/Volumes/Flash/automated/raw/"
output_composite_dir = "/Volumes/Flash/automated/composite/"


############################
## Initial setup of scene ##
############################

# Select all the default items in the scene and delete them

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
bpy.ops.object.select_all(action="DESELECT")

# We will use the Cycles render engine

bpy.data.scenes["Scene"].render.engine = "CYCLES"

# Set the world settings

bpy.data.worlds["World"].light_settings.use_ambient_occlusion = True	
# Turn on ambient occulusion, provides a global illumination to the scene
bpy.data.worlds["World"].light_settings.ao_factor = 1.0					
# Ambient occulusion value
bpy.data.worlds["World"].horizon_color = [0.0, 0.0, 0.0]				
# Set background colour to black


############################
## Define render settings ##
############################

# Could normally put these at the end, but we'll want to access some of these
# values in the script

bpy.data.scenes["Scene"].render.fps_base = 1
bpy.data.scenes["Scene"].render.resolution_x = 1280
bpy.data.scenes["Scene"].render.resolution_y = 720
bpy.data.scenes["Scene"].render.resolution_percentage = 100
bpy.data.scenes["Scene"].render.image_settings.compression = 100
bpy.data.scenes["Scene"].render.fps = 25
bpy.data.scenes["Scene"].cycles.samples = 130
bpy.data.scenes["Scene"].cycles.preview_samples = 100
bpy.data.scenes["Scene"].cycles.sample_clamp_indirect = 0.03
bpy.data.scenes["Scene"].cycles.max_bounces = 6
bpy.data.scenes["Scene"].cycles.min_bounces = 0
bpy.data.scenes["Scene"].cycles.transparent_max_bounces = 20
bpy.data.scenes["Scene"].cycles.caustics_reflective = False
bpy.data.scenes["Scene"].cycles.caustics_refractive = False
bpy.data.scenes["Scene"].cycles.blur_glossy = 0.2
bpy.data.scenes["Scene"].render.tile_x = 32
bpy.data.scenes["Scene"].render.tile_y = 32

#####################
## Import X3D file ##
#####################

# Import the X3D file.

bpy.ops.import_scene.x3d(filepath=X3D_location)

"""
When imported into Blender, the X3D file contains a number of contour meshes 
with default names like "ShapeIndexedFaceSet.???". We will delete those not 
required for this video, and rename the rest to something more human friendly.
The default MayaVI viewport objects are also imported, including a camera and 
some light sources.  We will remove these too. We will also define the positions 
of the galaxies within the HCG91 galaxy group, along with some RGB colours for 
their materials.
"""

# Following manually importing the X3D file into Blender and examining which 
# objects were which ...

bpy.data.objects["ShapeIndexedFaceSet"].name = "Contour1"
bpy.data.objects["ShapeIndexedFaceSet.001"].name = "Contour2"
bpy.data.objects["ShapeIndexedFaceSet.002"].name = "Contour3"
bpy.data.objects["ShapeIndexedFaceSet.003"].name = "Contour4"

# Delete everything else that isn't a "Contour*".

bpy.ops.object.select_all(action="DESELECT")

for ob in bpy.data.objects[:]:
	if "Contour" not in ob.name:
		ob.select = True
		bpy.ops.object.delete()
		
# Define the names, positions and display colours for the group's galaxies.

galaxies = [ #["Name", ra, V, dec, (R, G, B)],
["HCG 91a", 5.80581, 6832.0, -119.093, (0.0, 1.0, 0.0)],
["HCG 91b", -108.242, 7196.0, 165.907, (0.0, 0.2, 1.0)],
["HCG 91c", -77.7411, 7319.0, -21.0932, (0.4, 0.0, 1.0)],
["HCG 91d", -3.47719, 7195.0, -87.0932, (1.0, 0.0, 0.0)],
]

# Add the galaxy objects

for gal in galaxies:

	# Sphere

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	obj = bpy.context.object
	obj.name = gal[0]
	obj.location = (float(gal[1]), float(gal[2]), float(gal[3]))
	obj.scale = (10.0, 10.0, 10.0)	

	# Light
	
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.lamp_add(type="POINT")
	obj = bpy.context.object
	obj.name = "%s_Lamp" %gal[0]
	obj.location = (float(gal[1]), float(gal[2]), float(gal[3]))

# Change emission strength and softness of lamp objects

for ob in bpy.data.objects[:]:
	if ob.type == "LAMP":
		ob.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 500.0
		ob.data.shadow_soft_size = 1.0


##################################################################
## Decide on origin point for recentering and scaling the scene ##
##################################################################

# Select the largest contour

obj = bpy.data.objects["Contour1"]
obj.select = True

# Place origin at geometry

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

# Read the location

new_origin = obj.location

# Move 3D cursor to this point

bpy.context.scene.cursor_location = new_origin

obj.select = False


#######################################################################
## Cycle through objects and make corrections, recenter, resize, etc ##
#######################################################################

for obj in bpy.data.objects[:]:

	bpy.ops.object.select_all(action='DESELECT')
	obj.select = True
	bpy.context.scene.objects.active = obj 
	
	bpy.ops.object.transform_apply(location=True, scale=True, rotation=True)
	
	if obj.type == "MESH":
	
		# Shift and resize the object
		
		bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
		obj.location = [0.0, 0.0, 0.0]
		obj.rotation_euler = [0.0, 0.0, 0.0]
		obj.scale = [0.05, 0.05, 0.05]
		obj.select = False

		# Make some corrections to the mesh produced by MayaVI - 
		# removes duplicate vertexes and makes sure direction of faces 
		# are consistent.

		bpy.ops.object.mode_set(mode="EDIT")
		bpy.ops.mesh.remove_doubles()
		bpy.ops.mesh.normals_make_consistent()
		bpy.ops.object.mode_set(mode="OBJECT")

		# Adds some cosmetic smoothing to the meshes to remove sharp 
		# triangular edges.  Artistic choice for end user to make.

		obj.modifiers.new("smooth", type="SMOOTH")
		obj.modifiers["smooth"].iterations = 2

		obj.modifiers.new("subd", type="SUBSURF")
		obj.modifiers["subd"].levels = 2
		obj.modifiers["subd"].render_levels = 2

	if obj.type == "LAMP":
	
		# Lamp origin can't have an offset, so need to use a slightly 
		# different approach to shift/resize.
	
		obj.location[0] = (obj.location[0] - bpy.context.scene.cursor_location[0])*0.05
		obj.location[1] = (obj.location[1] - bpy.context.scene.cursor_location[1])*0.05
		obj.location[2] = (obj.location[2] - bpy.context.scene.cursor_location[2])*0.05
		
bpy.context.scene.cursor_location = [0.0, 0.0, 0.0]


#################################
## Create and assign materials ##
#################################

bpy.ops.object.select_all(action="DESELECT")


## First we'll focus on the galaxy spheres
# We'll be creating simple coloured diffuse materials

for gal in galaxies:

	# Remove existing materials, if any
	
	if len(bpy.data.objects["%s" %gal[0]].data.materials[:]) > 0:
		bpy.data.objects["%s" %gal[0]].data.materials.pop()
		
	# Create the material

	mat = bpy.data.materials.new("%sMaterial" %gal[0])
	mat.use_nodes = True

	# Remove existing nodes

	for node in mat.node_tree.nodes[:]:
		mat.node_tree.nodes.remove(node)

	# Add required shader nodes - an emission shader node, and the material 
	# output node

	mat.node_tree.nodes.new(type="ShaderNodeEmission")
	mat.node_tree.nodes["Emission"].location = [-100, 0]
	mat.node_tree.nodes["Emission"].inputs["Color"].default_value = (gal[4][0], gal[4][1], gal[4][2], 1.0)
	mat.node_tree.nodes["Emission"].inputs["Strength"].default_value = 1.0

	mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
	mat.node_tree.nodes["Material Output"].location = [100, 0]

	# Link the nodes together
        # Link the Diffuse shader's "BSDF" output with the material output's 
        # "Surface" input.
	mat.node_tree.links.new(mat.node_tree.nodes["Emission"].outputs["Emission"], 
	                        mat.node_tree.nodes["Material Output"].inputs["Surface"])	
	                        

	# Attach the material to the mesh

	bpy.data.objects[gal[0]].data.materials.append(mat)	
	
	# Change the ray visibility fo the objects - helps simplify the render 
	# and reduce noise.
	
	bpy.data.objects["%s" %gal[0]].cycles_visibility.diffuse = False
	bpy.data.objects["%s" %gal[0]].cycles_visibility.glossy = False
	bpy.data.objects["%s" %gal[0]].cycles_visibility.transmission = False
	bpy.data.objects["%s" %gal[0]].cycles_visibility.scatter = False
	bpy.data.objects["%s" %gal[0]].cycles_visibility.shadow = False
	
	
## Now we'll create a semi-transparent material for the contour meshes

# Define the contour colours we'll use

contours = [ #["Name", (R, G, B)],
["Contour1", (0.5, 0.225, 0.275)],
["Contour2", (0.65, 0.35, 0.22)],
["Contour3", (0.75, 0.21, 0.0)],
["Contour4", (1.0, 0.06, 0.0)]
]

for con in contours:

	# Remove existing materials, if any
	
	if len(bpy.data.objects["%s" %con[0]].data.materials[:]) > 0:
		bpy.data.objects["%s" %con[0]].data.materials.pop()

	# Create the material

	mat = bpy.data.materials.new("%sMaterial" %con[0])
	mat.use_nodes = True

	# Remove existing nodes

	for node in mat.node_tree.nodes[:]:
		mat.node_tree.nodes.remove(node)

	# Add required shader nodes - a diffuse node, a transparency node, a 
	# "layer weight" node, a mixing node, and the material output node	

	mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
	mat.node_tree.nodes["Diffuse BSDF"].location = [-100, -50]
	mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = \
	                                  (con[1][0], con[1][1], con[1][2], 1.0)

	mat.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
	mat.node_tree.nodes["Transparent BSDF"].location = [-100, 0]

	mat.node_tree.nodes.new(type="ShaderNodeLayerWeight")
	mat.node_tree.nodes["Layer Weight"].location = [-100, 50]
	mat.node_tree.nodes["Layer Weight"].inputs["Blend"].default_value = 0.1
	
	mat.node_tree.nodes.new(type="ShaderNodeMixShader")
	mat.node_tree.nodes["Mix Shader"].location = [0, 0]	

	mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
	mat.node_tree.nodes["Material Output"].location = [100, 0]	
	
	# Link the nodes together

	mat.node_tree.links.new(mat.node_tree.nodes["Layer Weight"].outputs["Facing"], 
	                        mat.node_tree.nodes["Mix Shader"].inputs["Fac"])
	mat.node_tree.links.new(mat.node_tree.nodes["Transparent BSDF"].outputs["BSDF"], 
	                        mat.node_tree.nodes["Mix Shader"].inputs[1])
	mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], 
	                        mat.node_tree.nodes["Mix Shader"].inputs[2])
	mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs["Shader"], 
	                        mat.node_tree.nodes["Material Output"].inputs["Surface"])

	# Attach the material to the mesh

	bpy.data.objects["%s" %con[0]].data.materials.append(mat)	

	# Change the ray visibility fo the objects - helps simplify the render 
	# and reduce noise.
	
	bpy.data.objects["%s" %con[0]].cycles_visibility.diffuse = False
	bpy.data.objects["%s" %con[0]].cycles_visibility.glossy = False
	bpy.data.objects["%s" %con[0]].cycles_visibility.transmission = False
	bpy.data.objects["%s" %con[0]].cycles_visibility.scatter = False
	bpy.data.objects["%s" %con[0]].cycles_visibility.shadow = False

##########################
## Setup default camera ##
##########################

bpy.ops.object.select_all(action="DESELECT")

# Add control "empty" object.  This will control camera rotation from the centre 
# of the scene.

bpy.ops.object.empty_add(type="PLAIN_AXES")
bpy.context.active_object.name = "CameraControl"

# Add camera

bpy.ops.object.camera_add()
bpy.data.cameras["Camera.001"].clip_start = 0.0
bpy.data.cameras["Camera.001"].clip_end = 10000.0		
# Increases the camera's view distance

# Parent camera to "empty" camera control object

bpy.ops.object.select_all(action="DESELECT")

bpy.data.objects["CameraControl"].select = True
bpy.context.scene.objects.active = bpy.data.objects["CameraControl"]
bpy.data.objects["Camera"].select = True

bpy.ops.object.parent_set(type="OBJECT", keep_transform=True)

# Move/rotate camera to default position

bpy.data.objects["Camera"].location = [100.0, 0.0, 0.0]
bpy.data.objects["Camera"].rotation_euler = [math.radians(90.0), 0.0, 
                                             math.radians(90.0)]

bpy.data.scenes["Scene"].camera = bpy.data.objects["Camera"]




########################################
## Create new scene with text overlay ##
########################################

bpy.ops.scene.new(type="EMPTY")

# Create a new "world" for the scene and assign some settings

bpy.ops.world.new()
bpy.data.scenes["Scene.001"].world = bpy.data.worlds["World.001"]

bpy.data.worlds["World.001"].light_settings.use_ambient_occlusion = True
bpy.data.worlds["World.001"].light_settings.ao_factor = 0.05
bpy.data.worlds["World.001"].horizon_color = [0.0, 0.0, 0.0]

bpy.data.scenes["Scene.001"].cycles.film_transparent = True

# Add a camera

bpy.ops.object.camera_add()

bpy.data.objects["Camera.001"].location = [0.0, 0.0, 25.0]
bpy.data.objects["Camera.001"].rotation_euler = [0.0, 0.0, 0.0]

bpy.data.scenes["Scene.001"].camera = bpy.data.objects["Camera.001"]

# Now add the text

i = 0

for gal in galaxies:

	bpy.ops.object.text_add()
	
	bpy.context.object.data.body = gal[0]
	
	bpy.data.objects["Text"].data.materials.append(bpy.data.materials["%sMaterial" %gal[0]])
	
	bpy.data.objects["Text"].location = [-11.3, 5.5 - (1.0*i), 0.0]
	
	bpy.context.object.data.name = "%s_Text" %gal[0]
	bpy.data.objects["Text"].name = "%s_Text" %gal[0]
	
	i = i + 1

# Move back to original scene and add nodes to the compositor
# We will use the compositor to overlay this text on the original rendered scene
# This allows us to simultaneously produce versions of the animation with and 
# without text 

bpy.context.screen.scene = bpy.data.scenes["Scene"]

# Switch on nodes and get reference
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# Clear default nodes
for node in tree.nodes:
    tree.nodes.remove(node)

# Create the required nodes

renderlayer1 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeRLayers")
renderlayer1.scene = bpy.data.scenes["Scene"]
renderlayer1.location = [-200, 200]

renderlayer2 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeRLayers")
renderlayer2.scene = bpy.data.scenes["Scene.001"]
renderlayer2.location = [-200, -200]

alphaover = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeAlphaOver")
alphaover.location = [0, 0]

composite = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeComposite")
composite.location = [200, 300]

viewer = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeViewer")
viewer.location = [200, 100]

fileoutput1 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeOutputFile")
# Output directory for render+text version
fileoutput1.base_path = output_composite_dir	
fileoutput1.location = [200, -100]	

fileoutput2 = bpy.context.scene.node_tree.nodes.new(type="CompositorNodeOutputFile")
# Output directory for render only version
fileoutput2.base_path = output_raw_dir			
fileoutput2.location = [200, -300]

# Link the nodes together

bpy.context.scene.node_tree.links.new(renderlayer1.outputs[0], alphaover.inputs[1])
bpy.context.scene.node_tree.links.new(renderlayer2.outputs[0], alphaover.inputs[2])
bpy.context.scene.node_tree.links.new(renderlayer1.outputs[0], fileoutput2.inputs[0])
bpy.context.scene.node_tree.links.new(alphaover.outputs[0], composite.inputs[0])
bpy.context.scene.node_tree.links.new(alphaover.outputs[0], viewer.inputs[0])
bpy.context.scene.node_tree.links.new(alphaover.outputs[0], fileoutput1.inputs[0])


###################
## Add animation ##
###################

# There is an immense variety of options that can be utilised here, pretty much 
# everything you can think of can be keyframed.
# For this example, we will animate some simple 360 degree rotations of the 
# camera around the scene.
# With each rotation we will vary the appearance of some of the objects in the 
# scene in order to highlight different galaxies on each rotation

# Define the animation parameters

animation = [ # time (s), AO value, [xrot1, yrot1, zrot1], [xrot2, yrot2, zrot2], [objects "on"], [objects "off"],
[5.0, 1.0, [0.0, 0.0, 0.0], [0.0, 0.0, 360.0], ["HCG 91a", "HCG 91b", "HCG 91c", "HCG 91d"], []],	# Everything is "on"
[5.0, 0.25, [0.0, 0.0, 0.0], [0.0, 0.0, 360.0], ["HCG 91a"], ["HCG 91b", "HCG 91c", "HCG 91d"]],	# Only galaxy A is "on"
[5.0, 0.25, [0.0, 0.0, 0.0], [0.0, 0.0, 360.0], ["HCG 91c"], ["HCG 91a", "HCG 91b", "HCG 91d"]],	# Only galaxy C is "on"
]

# Set animation length

total_time = 0.0
for ani in animation:
	total_time = total_time + ani[0]

total_frames = total_time * bpy.data.scenes["Scene"].render.fps
			
bpy.data.scenes["Scene"].frame_start = 1
bpy.data.scenes["Scene"].frame_end = total_frames		
		
# Select the camera controls

bpy.ops.object.select_all(action="DESELECT")

cc = bpy.data.objects["CameraControl"]
cc.select = True

bpy.context.scene.objects.active = bpy.data.objects["CameraControl"]

# Construct animation

frames_prior = 0

for ani in animation:

	frames = ani[0] * bpy.data.scenes["Scene"].render.fps
	
	first_frame = frames_prior + 1
	last_frame = frames_prior + frames
		
	keyframes = [(first_frame,2), (last_frame,3)]
	
	for keyframe in keyframes:

		bpy.data.scenes["Scene"].frame_current = keyframe[0]		
	
		# Camera rotation
	
		cc.rotation_euler = [math.radians(ani[keyframe[1]][0]), 
		                     math.radians(ani[keyframe[1]][1]), 
		                     math.radians(ani[keyframe[1]][2])]
		bpy.ops.anim.keyframe_insert(type='Rotation',
		                              confirm_success=False)

		# Scene AO brightness
		# Change the value
		bpy.data.worlds["World"].light_settings.ao_factor = ani[1]
		# Insert a keyframe				
		bpy.data.worlds["World"].light_settings.keyframe_insert("ao_factor")	
		
		# Galaxy illumination
		
		for on in ani[4]:

			# Spheres
		
			bpy.data.objects["%s" %on].data.materials["%sMaterial" %on].node_tree.nodes["Emission"].inputs["Strength"].default_value = 1.0
			bpy.data.objects["%s" %on].data.materials["%sMaterial" %on].node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert("default_value")
		
			# Lamps
			bpy.data.objects["%s_Lamp" %on].data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 500.0
			bpy.data.objects["%s_Lamp" %on].data.node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert("default_value")
		
		for off in ani[5]:
		
			# Spheres
		
			bpy.data.objects["%s" %off].data.materials["%sMaterial" %off].node_tree.nodes["Emission"].inputs["Strength"].default_value = 0.1
			bpy.data.objects["%s" %off].data.materials["%sMaterial" %off].node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert("default_value")
		
			# Lamps
			bpy.data.objects["%s_Lamp" %off].data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 0.0
			bpy.data.objects["%s_Lamp" %off].data.node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert("default_value")
	
		# Note that we don't need to explicitly do anything for the text 
		# overlays on the other scene.
		# These are using the exact same materials as the galaxy spheres, 
		# so they are already animated.
				
	frames_prior = frames_prior + frames		

# Set interpolation and curve handles
# Animations can be linear, or can speed up/slow down using Bezier curves
# For this animation everything will be simple and linear

frames_prior = 0

for ani in animation:

	frames = ani[0] * bpy.data.scenes["Scene"].render.fps
	
	first_frame = frames_prior + 1
	last_frame = frames_prior + frames
		
	keyframes = [(first_frame,2), (last_frame,3)]
	
	for keyframe in keyframes:

		for curves in bpy.data.objects["CameraControl"].animation_data.action.fcurves:
			for kfs in curves.keyframe_points:
				if float(kfs.co[0]) == float(keyframe[0]):
					kfs.interpolation = "LINEAR"
		
	frames_prior = frames_prior + frames
			
##########################################
## Set viewport shading and camera view ##
##########################################

# This just automatically sets Blender to a "rendered" view for instant feedback 
# that the script has worked.

for area in bpy.context.screen.areas: # iterate through areas in current screen
    if area.type == 'VIEW_3D':
        for space in area.spaces: # iterate through spaces in current VIEW_3D area
            if space.type == 'VIEW_3D': # check if space is a 3D view
                # set the viewport shading to rendered
                space.viewport_shade = 'RENDERED' 
                space.region_3d.view_perspective="CAMERA"


# READY TO RENDER! #
#bpy.ops.render.render(animation=True)
