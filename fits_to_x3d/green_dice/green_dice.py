# This script creates a basic green dice to explore the capabilities of 
# mayavi.
#
# To run (in a Python shell):
# run green_dice.py 
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
mlab.close(1)
mlab.figure(1,size=(500,500))

# Add a green cube
mlab.points3d(xs,ys,zs, scale_factor=1,scale_mode='none', color=(0,1.0,0),
                mode='cube')
                
# A dark outline for the look
mlab.outline(color=(0,0,0),line_width = 2.0)

# The different dice faces
mlab.points3d(px,py,pz,pc, scale_factor=0.2, scale_mode="none", 
                color=(1,1,1),mode='sphere')

# Export the model to X3D and/or PNG, etc ...
mlab.savefig('./green_dice.x3d')
mlab.savefig('./green_dice.png')

mlab.show()
