# This script creates a transparent red dice to explore further the capabilities
# of mayavi.
#
# To run (in a Python shell):
# run red_dice.py 
#
# Created January 2015 by F.P.A.Vogt for the ANITA astroinformatics summer 
# school 2015. 
# Published as supplementary material in Vogt, Owen et al., ApJ (2015).
#
# Questions, comments : frederic.vogt@anu.edu.au
#
# If you find this code useful for your research, please cite
#
# Vogt, Owen et al., Advanced Data Visualization in Astrophysics: 
# the X3D Pathway, ApJ (2015).
#
# ------------------------------------------------------------------------------

# Import the required packages
from enthought.mayavi import mlab

# Define the dice elements
xs = [0]
ys = [0]
zs = [0]
px = [0,
    -0.25,-0.25,-0.25,0.25, 0.25,0.25,
    -0.5, -0.5,-0.5, -0.5,-0.5,
     0.5, 0.5,
     0,-0.25,0.25,
    -0.25, -0.25, 0.25, 0.25]
py = [0, 
    -0.25, 0, 0.25,-0.25, 0, 0.25,
    0,-0.25,0.25, -0.25, 0.25,
    -0.25,0.25,
    -0.5, -0.5, -0.5, 
    0.5, 0.5, 0.5, 0.5]
pz = [-0.5,
    0.5,0.5, 0.5, 0.5, 0.5,0.5,
    0, -0.25, -0.25, 0.25, 0.25,
    0.25, -0.25,
    0,-0.25, 0.25,
    -0.25,0.25, -0.25, 0.25]
pc = [0,
    6,6,6,6,6,6,
    5,5,5,5,5,
    2,2,
    3,3,3,
    4,4,4,4,]        


# Create a mayavi window
mlab.close(2)
mlab.figure(2,size=(500,500))

# Add some inner spheres with transparency and the cube
mlab.points3d(xs,ys,zs, scale_factor=0.25,color=(1,0.5,0), mode= 'sphere',
                opacity=1)
mlab.points3d(xs,ys,zs, scale_factor=0.5,color=(1,1,1), mode= 'sphere', 
                opacity=0.5)
mlab.points3d(xs,ys,zs, scale_factor=1,scale_mode='none', color=(0.7,0,0),
                mode='cube', opacity=0.5)

# A dark outline for the look
mlab.outline(color=(0,0,0),line_width = 2.0)

# The different cube faces this time with some colors
mlab.points3d(px,py,pz, pc, scale_factor=0.2, scale_mode='none', 
                colormap="bone",mode='sphere')

# And the associated colorbar
mlab.colorbar(orientation="vertical",nb_labels=7)

# Finally add some text. 
# This can be done via either mlab.text() or mlab.text3d(). We prefer the former
# function, as it will result in a "text" instance in the associated X3D file, 
# which allows, e.g. to modifiy the text itself at the X3D level. By comparison,
# mlab.text3D() creates a full 3-D structure which cannot be modified later on.
mlab.text(0,0,"This is a dice",z=1)

# Export the model to X3D and WRL
mlab.savefig('./red_dice.x3d')
mlab.savefig('./red_dice.png')

mlab.show()
