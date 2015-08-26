import bpy, math
from mathutils import Vector

"""
This is a more complex Blender script to import an X3D mesh of a red dice.
It sets up a typical Blender scene, imports an X3D mesh, applies a variety of materials, and sets up a simple animation.
"""

###########################################
## Define file locations and directories ##
###########################################

X3D_location = "/Volumes/Flash/red_dice.x3d"
bpy.data.scenes["Scene"].render.filepath = "/Volumes/Flash/red_dice/"				# Rendered frames output location.

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

# Note that this X3D file contains the required objects, and also some other unwanted 
# objects from MayaVI.  This includes the MayaVI viewport camera and some lamps.  We will
# delete these and keep only the dice objects.

bpy.data.objects["ShapeIndexedFaceSet"].name = "YellowSphere"
bpy.data.objects["ShapeIndexedFaceSet.001"].name = "TransparentSphere"
bpy.data.objects["ShapeIndexedFaceSet.002"].name = "TransparentCube"
bpy.data.objects["ShapeIndexedFaceSet.003"].name = "NumberSpheres"
bpy.data.objects["ShapeIndexedLineSet"].name = "DiceOutline"

# Remove all the other unwanted objects imported in the X3D file

bpy.ops.object.select_all(action="DESELECT")

for obj in bpy.data.objects[:]:
	if obj.name not in ["YellowSphere", "TransparentSphere", "TransparentCube", "NumberSpheres", "DiceOutline"]:
		bpy.data.objects[obj.name].select = True	
		bpy.ops.object.delete()		

# The small spheres representing the dice's numbers were exported from MayaVI as a single object.
# We want to split them into separate spheres and work out which are which.

bpy.ops.object.select_all(action="DESELECT")
bpy.data.objects["NumberSpheres"].select = True
bpy.ops.mesh.separate(type="LOOSE")

# Now lets sort through these spheres

n = 0

for obj in bpy.data.objects[:]:

	if "NumberSpheres" in obj.name:
		
		bpy.ops.object.select_all(action="DESELECT")
		obj.select = True
		bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
		
		# There is a single vertex placed at the centre of the scene, we should delete this
		
		if obj.location == Vector((0.0, 0.0, 0.0)):
			bpy.ops.object.delete()
			
		# Now we'll rename the spheres by their dice number, and an arbitrary number to keep them unique
			
		if obj.location[1] < -0.45:	# Number 1
			obj.name = "Dice1_%s" %n			

		if obj.location[0] < -0.45:	# Number 2
			obj.name = "Dice2_%s" %n	

		if obj.location[2] < -0.45:	# Number 3
			obj.name = "Dice3_%s" %n	

		if obj.location[2] > 0.45:	# Number 4
			obj.name = "Dice4_%s" %n	

		if obj.location[0] > 0.45:	# Number 5
			obj.name = "Dice5_%s" %n	
			
		if obj.location[1] > 0.45:	# Number 6
			obj.name = "Dice6_%s" %n	

		# We'll add a subsurface modifier to make these low-poly spheres look more spherical.  
		# They're not really spheres though, so they'll still be a bit lumpy.  Adds character to the scene. :)

		obj.modifiers.new("subd", type="SUBSURF")
		obj.modifiers["subd"].levels = 3
		obj.modifiers["subd"].render_levels = 3
			
	n = n + 1

# Lets also add a subsurface modifier to the other spheres in the scene	

bpy.data.objects["YellowSphere"].modifiers.new("subd", type="SUBSURF")
bpy.data.objects["YellowSphere"].modifiers["subd"].levels = 3
bpy.data.objects["YellowSphere"].modifiers["subd"].render_levels = 3

bpy.data.objects["TransparentSphere"].modifiers.new("subd", type="SUBSURF")
bpy.data.objects["TransparentSphere"].modifiers["subd"].levels = 3
bpy.data.objects["TransparentSphere"].modifiers["subd"].render_levels = 3

# Let's give some volume to the DiceOutline line object

bpy.data.objects["DiceOutline"].data.bevel_depth = 0.005


# Import flat plane for dice to sit above

bpy.ops.mesh.primitive_plane_add(radius=100)
plane = bpy.data.objects["Plane"]

plane.location = [0.0, 0.0, -0.7]

# Add a point lamp

bpy.ops.object.lamp_add(type="POINT")
lamp = bpy.data.objects["Point"]

lamp.location = [2.0, 1.0, 3.0]
lamp.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 300.0  # Set lamp brightness value

# Add a camera

bpy.ops.object.camera_add()
camera = bpy.data.objects["Camera"]

camera.location = [2.0, -2.0, 2.75]
camera.rotation_euler = [math.radians(45.0), 0.0, math.radians(45.0)]


################################################
## Create materials and assign to our objects ##
################################################

"""
Note that setting up materials is a fairly simple process, but one which generally takes a relatively large number of lines.
This is because we are mimicking setting up a node/node-link structure that was designed for manual manipulation in the GUI.
In a "real" script, most of this could be done more efficiently using functions for the repeated lines. For "simplicity" I present each material in full where appropriate.
For more complex materials in a "real" script, it is better to create the material manually in a separate .blend file, then simply "append" it to the script.
Creating materials manually is also helpful as you get to see how they look in real-time.  
"""

## Simple black diffuse material ##
# For the dice outline

mat = bpy.data.materials.new("DiffuseBlack")
mat.use_nodes = True

# Remove existing nodes

for node in mat.node_tree.nodes[:]:
	mat.node_tree.nodes.remove(node)

# Add required shader nodes

mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
mat.node_tree.nodes["Diffuse BSDF"].location = [-200, 0]
mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)		# Black colour

mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
mat.node_tree.nodes["Material Output"].location = [200, 0]

# Link the shader nodes together

mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], mat.node_tree.nodes["Material Output"].inputs["Surface"])

# Remove any default material already associated with the object

for i in range(len(bpy.data.objects["DiceOutline"].data.materials[:])):
	bpy.data.objects["DiceOutline"].data.materials.pop()

# Now append the new material to the object

bpy.data.objects["DiceOutline"].data.materials.append(mat)


## Simple yellow diffuse material ##
# For the yellow internal sphere

mat = bpy.data.materials.new("DiffuseYellow")
mat.use_nodes = True

# Remove existing nodes

for node in mat.node_tree.nodes[:]:
	mat.node_tree.nodes.remove(node)

# Add required shader nodes

mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
mat.node_tree.nodes["Diffuse BSDF"].location = [-200, 0]
mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = (1.0, 0.5, 0.0, 1.0)		# Yellow colour

mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
mat.node_tree.nodes["Material Output"].location = [200, 0]

# Link the shader nodes together

mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], mat.node_tree.nodes["Material Output"].inputs["Surface"])

# Remove any default material already associated with the object

for i in range(len(bpy.data.objects["YellowSphere"].data.materials[:])):
	bpy.data.objects["YellowSphere"].data.materials.pop()

# Now append the new material to the object

bpy.data.objects["YellowSphere"].data.materials.append(mat) 


## Red transparent dice material ##
# This is a combination of the "diffuse" and "transparent" shaders.

mat = bpy.data.materials.new("TransparentRed")
mat.use_nodes = True

# Remove existing nodes

for node in mat.node_tree.nodes[:]:
	mat.node_tree.nodes.remove(node)

# Add required shader nodes

mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
mat.node_tree.nodes["Diffuse BSDF"].location = [-200, -100]
mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = (1.0, 0.0, 0.0, 1.0)		# Red colour

mat.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
mat.node_tree.nodes["Transparent BSDF"].location = [-200, 100]
mat.node_tree.nodes["Transparent BSDF"].inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)		# White colour

mat.node_tree.nodes.new(type="ShaderNodeMixShader")
mat.node_tree.nodes["Mix Shader"].location = [0, 0]
mat.node_tree.nodes["Mix Shader"].inputs["Fac"].default_value = 0.4								# The material will be 60% transparent and 40% diffuse

mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
mat.node_tree.nodes["Material Output"].location = [200, 0]

# Link the shader nodes together

mat.node_tree.links.new(mat.node_tree.nodes["Transparent BSDF"].outputs["BSDF"], mat.node_tree.nodes["Mix Shader"].inputs[1])
mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], mat.node_tree.nodes["Mix Shader"].inputs[2])
mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs["Shader"], mat.node_tree.nodes["Material Output"].inputs["Surface"])

# Remove any default material already associated with the object

for i in range(len(bpy.data.objects["TransparentCube"].data.materials[:])):
	bpy.data.objects["TransparentCube"].data.materials.pop()

# Now append the new material to the object

bpy.data.objects["TransparentCube"].data.materials.append(mat)


## Clear transparent sphere material ##
# This is a combination of the "diffuse" and "transparent" shaders.

mat = bpy.data.materials.new("TransparentClear")
mat.use_nodes = True

# Remove existing nodes

for node in mat.node_tree.nodes[:]:
	mat.node_tree.nodes.remove(node)

# Add required shader nodes

mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
mat.node_tree.nodes["Diffuse BSDF"].location = [-200, -100]
mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)		# White colour

mat.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
mat.node_tree.nodes["Transparent BSDF"].location = [-200, 100]
mat.node_tree.nodes["Transparent BSDF"].inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)		# White colour

mat.node_tree.nodes.new(type="ShaderNodeMixShader")
mat.node_tree.nodes["Mix Shader"].location = [0, 0]
mat.node_tree.nodes["Mix Shader"].inputs["Fac"].default_value = 0.4								# The material will be 60% transparent and 40% diffuse

mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
mat.node_tree.nodes["Material Output"].location = [200, 0]

# Link the shader nodes together

mat.node_tree.links.new(mat.node_tree.nodes["Transparent BSDF"].outputs["BSDF"], mat.node_tree.nodes["Mix Shader"].inputs[1])
mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], mat.node_tree.nodes["Mix Shader"].inputs[2])
mat.node_tree.links.new(mat.node_tree.nodes["Mix Shader"].outputs["Shader"], mat.node_tree.nodes["Material Output"].inputs["Surface"])

# Remove any default material already associated with the object

for i in range(len(bpy.data.objects["TransparentSphere"].data.materials[:])):
	bpy.data.objects["TransparentSphere"].data.materials.pop()

# Now append the new material to the object

bpy.data.objects["TransparentSphere"].data.materials.append(mat)


## Diffuse coloured dice number materials ##

# Now we want to create a material for each of the set of spheres for each side of the dice.
# This requires creating 6 materials which are identical, except for their colour, so we will use a function here.
# Note that these materials are identical to the "DiffuseBlack" and "DiffuseYellow" created above.

# First, define which colours we'll be using:

dice_numbers = [ # [DiceNumber, (R,G,B)],
[1, (0.137, 0.137, 0.196)],
[2, (0.294, 0.294, 0.392)],
[3, (0.392, 0.471, 0.549)],
[4, (0.569, 0.667, 0.706)],
[5, (0.765, 0.863, 0.843)],
[6, (1.0, 1.0, 1.0)]
]

# Next, create the function which will create and assign the material

def create_dicenumbmat(number, R, G, B):

	mat = bpy.data.materials.new("Dice%s" %number)
	mat.use_nodes = True

	# Remove existing nodes

	for node in mat.node_tree.nodes[:]:
		mat.node_tree.nodes.remove(node)

	# Add required shader nodes

	mat.node_tree.nodes.new(type="ShaderNodeBsdfDiffuse")
	mat.node_tree.nodes["Diffuse BSDF"].location = [-200, 0]
	mat.node_tree.nodes["Diffuse BSDF"].inputs["Color"].default_value = (R, G, B, 1.0)		# Dice colour

	mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
	mat.node_tree.nodes["Material Output"].location = [200, 0]

	# Link the shader nodes together

	mat.node_tree.links.new(mat.node_tree.nodes["Diffuse BSDF"].outputs["BSDF"], mat.node_tree.nodes["Material Output"].inputs["Surface"])

	# Find the objects associated with this dice number
	
	for obj in bpy.data.objects[:]:
	
		if "Dice%s" %number in obj.name:

			# Remove any default material already associated with the object

			for i in range(len(obj.data.materials[:])):
				obj.data.materials.pop()

			# Now append the new material to the object

			obj.data.materials.append(mat) 	

# Now run the function for each dice number

for dice_number in dice_numbers:

	create_dicenumbmat(dice_number[0], dice_number[1][0], dice_number[1][1], dice_number[1][2])


## Floor plane material ##

# For simplicity, we'll just leave this as the default Cycles material - a simple diffuse off-white.  Nothing needs to be done here.

###############
## Animation ##
###############

# For our animation we'll make the camera do a 360 degree spin around the centre of the dice.

# First, we'll create an "empty" object at the centre of the scene - this will control the camera's rotation.

bpy.ops.object.empty_add(type="PLAIN_AXES")
bpy.data.objects["Empty"].name = "CameraControl"

# Now we'll parent the Camera to the CameraControl object.  Any location/rotation/scale operation applied to the CameraControl will also be applied to the Camera.

bpy.data.objects["Camera"].parent = bpy.data.objects["CameraControl"]

# Now we'll animate the CameraControl to rotate 360 degrees around the Z axis.
# The default frames-per-second is 24, so we'll make a 5 second animation (5 * 24 = 120 frames)

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

bpy.data.scenes["Scene"].frame_current = 121		# We want the 121th frame to be the 360th degree to make sure frame 1 and 120 are not identical.
bpy.data.objects["CameraControl"].rotation_euler = [0.0, 0.0, math.radians(360.0)]
bpy.ops.anim.keyframe_insert(type='Rotation',confirm_success=False)

# The animation is interpolated between these two keyframes.  You get a choice of what kind of interpolation to use.
# The default uses Bezier curves in order to accelerate and decelerate the motion.  
# We want a smooth linear motion here, so we'll change the interpolation for each keyframe to "linear".

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
bpy.data.scenes["Scene"].cycles.samples = 125							# The "quality" of the render.  More samples means less noise, but longer render time.
bpy.data.scenes["Scene"].cycles.sample_clamp_indirect = 0.5				# Clamps the indirect light rays.  Reduces noise at the cost of the accuracy of bounced light.
bpy.data.scenes["Scene"].render.tile_x = 32								# The render tile sizes.  Smaller tiles render faster, but at the cost of additional overhead for swapping more tiles.  For typical CPU rendering on my Macbook Pro, 32 is a good size.
bpy.data.scenes["Scene"].render.tile_y = 32					

# If you're looking for something a tiny bit more fancy to add to the fluidity of the animation, try switching on motion blur
#bpy.data.scenes["Scene"].render.use_motion_blur = True

# READY TO RENDER! #
