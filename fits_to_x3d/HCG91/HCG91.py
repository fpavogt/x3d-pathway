# -*- coding: utf-8 -*-
#
# This program is designed to plot an interactive 3D cube of the HI gas in 
# the compact group of galaxies HCG91 using the Mayavi module. It is an example 
# of "real" astrophsyical data plotted interactively in 3-D using Mayavi. 
# In particular, the code does not shy away from the intricasies related to 
# dealing with WCS coordinates, large(-r) datasets, etc ...
#
# See the green and red dice examples for more basic introductions to Mayavi.
#
# To run (in a Python shell):
# run HI_to_x3d.py 
#
# Created, April 2015, F.P.A. Vogt
#
# Questions, comments : frederic.vogt@anu.edu.au
#
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

# Import the required modules

from enthought.mayavi import mlab # for the interactive 3D
from astropy.io import fits as pyfits # to open fits files
import numpy as np 
from astropy import wcs # to work with WCS (not required for plotting as such)

# ------------------------------------------------------------------------------
# Define some useful functions to deal with WCS coordinates

# Declination to degrees
def dectodeg (dec) :
    return np.sign(dec[0])*(abs(dec[0]) + dec[1]/60. + dec[2]/3600.)

# R.A. to degrees
def ratodeg (ra) :
    return (ra[0] + ra[1]/60. + ra[2]/3600.)/24.*360

# ------------------------------------------------------------------------------
# Start the program here

# Where to save the diagrams ?
plot_loc = './'

# Open the FITS file from the VLA
hdulist=pyfits.open('./data/HCG91.FITS')

# Load the array
# It must be scaled to a 'reasonable' range to avoid small number issues.
scidata = hdulist['PRIMARY'].data[0] * 1000. 
header = hdulist['PRIMARY'].header

# Load the correspondance between channels and velocity
c_v = np.loadtxt('./data/HCG91.dat')

# Extract some useful parameters
n_slice=scidata.shape[0]
size_y=scidata.shape[1]
size_x=scidata.shape[2]
hdulist.close()

# Define the min and max velocity slice of interest (no HI outside these)
slice_min = 5
slice_max = 50

# Define the x/y limits (in pixels; no HI signal outside these)
limx = [100,160]
limy = [105,165]

# Extract some more parameters of the datacube, and run some safety checks.
dv = np.mean(c_v[:-1,1] - c_v[1:,1])
stdv = np.std(c_v[:-1,1] - c_v[1:,1])
vmin = c_v[slice_max,1]
vmax = c_v[slice_min,1]

# The galaxies in the field RA,DEC,v,z
# From Hickson (1992)
gals = {'hcg91a':{'ra':[22,9,07.7],
                  'dec':[-27,48,34.0],
                  'v':6832.},
        'hcg91b':{'ra':[22,9,16.3],
                  'dec':[-27,43,49.0],
                  'v':7196.}, 
        'hcg91c':{'ra':[22,9,14.0],
                  'dec':[-27,46,56.0],
                  'v':7319.}, 
        'hcg91d':{'ra':[22,9,08.4],
                  'dec':[-27,48,02.0],
                  'v':7195.},
       }

# All of the code below is only required to plot the galaxies in the good place
# in the cube. Forget this part if you don't care about handling WCS elements.
# This is NOT required to use mayavi per say.
# ---

# Create a new WCS object.
w = wcs.WCS(header)

# Ok, now, create the grids of indexes for the plotting
# One must work directly in WCS coord if one wants the correct coordinates
# This is NOT perfect, but close enough given the field-of-view of the data.
# (i.e. the sky is still flat at that scale) 
# Also assumes that North is perfectly up in VLA data !
 
 # Just to be safe, check how big the distortion would be.
# Look at the WCS coordinates of the 4 corners of the cube, and look at the 
# mismatch
# ll = lower left, ur = upper-right, etc ...
ra_ll = w.wcs_pix2world(np.array([[limx[0],limy[0],0,0]]),0)[0][0]
dec_ll = w.wcs_pix2world( np.array([[limx[0],limy[0],0,0]]),0)[0][1]

ra_lr = w.wcs_pix2world(np.array([[limx[1],limy[0],0,0]]),0)[0][0]
dec_lr = w.wcs_pix2world( np.array([[limx[1],limy[0],0,0]]),0)[0][1]
 
ra_ul = w.wcs_pix2world(np.array([[limx[0],limy[1],0,0]]),0)[0][0]
dec_ul = w.wcs_pix2world( np.array([[limx[0],limy[1],0,0]]),0)[0][1] 

ra_ur = w.wcs_pix2world(np.array([[limx[1],limy[1],0,0]]),0)[0][0]
dec_ur = w.wcs_pix2world( np.array([[limx[1],limy[1],0,0]]),0)[0][1]

# The corner mismatch, in arcsec
err_dec_l = np.abs(dec_ll - dec_lr)*3600
err_dec_u = np.abs(dec_ul - dec_ur)*3600
err_ra_l = np.abs(ra_ll - ra_ul)*3600*np.cos(np.radians(dec_ll))
err_ra_r = np.abs(ra_lr - ra_ur)*3600*np.cos(np.radians(dec_lr))

print ' WARNING: WCS coord errors (in arcsec):'
print ' err_dec South/North:',np.round(err_dec_l,2),np.round(err_dec_u,2)
print ' err_ra East/West:',np.round(err_ra_l,2),np.round(err_ra_r,2)
print ' ' 

# Select the final WCS range
ramin = w.wcs_pix2world(np.array([[limx[1],limy[0],0,0]]),0)[0][0] 
ramax = w.wcs_pix2world(np.array([[limx[0],limy[0],0,0]]),0)[0][0]
ramean = np.mean([ramin,ramax])

decmin = w.wcs_pix2world( np.array([[limx[0],limy[0],0,0]]),0)[0][1] 
decmax = w.wcs_pix2world( np.array([[limx[0],limy[1],0,0]]),0)[0][1]
decmean = np.mean([decmin,decmax])

# For info, print the central WCS coordinate of the cube
print ' Central location [RA;Dec]:',ramean,decmean 
    
# Finally, create grids with the coordinates of all the elements in the VLA data
# Use relative offsets in arcsec for R.A. and Dec., and absolute velocity for v
ras,decs,vs = np.mgrid[ (ramin-ramean)*3600.*np.cos(np.radians(decmin)):
                        (ramax-ramean)*3600.*np.cos(np.radians(decmin)):
                        (limx[1]-limx[0]+1)*1j,
                        (decmin-decmean)*3600.:
                        (decmax-decmean)*3600.:
                        (limy[1]-limy[0]+1)*1j,
                        vmin:vmax+0.1:dv]
# ---

# Re-order the VLA array to have the dimensions in the good direction !
# (z = v, x= R.A.), etc ... 
# Also flip the velocity axis to be in the good direction
HI_cube = scidata[slice_min:slice_max+1,limy[0]:limy[1]+1,limx[0]:limx[1]+1 ]
HI_cube = np.transpose(HI_cube, (2,1,0))[::-1,:,::-1]


# Start the plotting
mlab.close(1)
fig = mlab.figure(1, size=(1100,1100)) 

# What contours levels do I want ? Can be chosen by defaults, or scripted.
isolevels = [1.3,2.5,3.5,6.0]

# --- !!! ---
# MAYAVI BUG & WORK-AROUND (#1)
# Currently, the x3d export function from Mayavi ignores the "vmin" and "vmax"
# parameters in the plotting function, and only uses the min and max of the 
# datasets. Hence, to export the "exact same" color for the different plot 
# elements shown in the interactive Mayavi window, the data itself MUST be
# modified; i.e. all values outside the [vmin->vmax] range must be replaced. 
# This is NOT elegant, and will hopefully be fixed in future releases of Mayavi.

color_scale = [0.8,6.1]
HI_cube[HI_cube<color_scale[0]] = color_scale[0]
HI_cube[HI_cube>color_scale[1]] = color_scale[1]
# --- !!! ---

# Plot the different iso-contours of the HI emission
# Draw them one-at-a-time to a) control their transparency individually and b)
# export them as individual structures (useful for the interactive html model).
for (j,level) in enumerate(isolevels):
    if j == len(isolevels)-1:
        op = 1
    else:
        op = 0.2
     
    # Plot the said contour - and flip the colorscheme for aesthetic purposes.     
    cm_tweak = -1.0      
    mlab.contour3d(ras,decs,vs,
                   HI_cube*cm_tweak,
                   contours = [level*cm_tweak],
                   opacity =op,
                   vmin =color_scale[1]*cm_tweak, vmax = color_scale[0]*cm_tweak,
                   name = 'I: '+np.str(level),
                   colormap = 'Set1')     
                   
                   
# Draw a box around the cube to aid in the visualization
mlab.outline(extent=[  np.min(ras),np.max(ras),
                       np.min(decs), np.max(decs),
                       c_v[slice_min,1],
                       c_v[slice_max,1]],
                       color=(0,0,0),
                       line_width = 2.0) # Draw a box around it


# Now, add some axes
ax = mlab.axes(extent=[np.min(ras),np.max(ras),
                       np.min(decs), np.max(decs),
                       c_v[slice_min,1],
                       c_v[slice_max,1]],
                       nb_labels=3, color = (0,0,0))

# Fine tune the look of the axis               
ax.axes.fly_mode = 'outer_edges'
ax.title_text_property.font_size = 10
ax.title_text_property.font_family = 'courier'
ax.title_text_property.italic = False
ax.label_text_property.font_family = 'courier'
ax.label_text_property.italic = False
ax.scene.parallel_projection = True
ax.scene.background = (1.0,1.0,1.0)
ax.title_text_property.color = (0,0,0)
ax.label_text_property.color = (0,0,0)
ax.axes.x_label = 'R.A. ["]'
ax.axes.y_label = 'Dec. ["]'
ax.axes.z_label = 'V [km/s]'    
ax.axes.label_format = '%-#6.1f'

# --- !!! ---
# MAYAVI BUG & WORK-AROUND (#2)
# Currently, the default axis drawn by Mayavi are NOT exported to the x3d model.
# This is very inconvenient, and will hopefully be addressed in future releases.
# A possible work around is to draw the axis, axis labels and axis tick labels 
# manually, one-at-a-time. This is what is done below.
# So, for clarity, turn off the "default" mayavi axis for now.

ax.visible = False

# One should note that the diagrams visible in Figure 2 in Vogt, Owen, et al.,
# ApJ (2015) were generated with the default Mayavi axis, i.e. by setting
#
#ax.visible = True
#
# --- !!! ---


# Now, add spheres and cubes to mark locations of interest in the data. 
# First, the 4 galaxies members of the compact groups.
# Also add black crosses for clarity.
cross_size = 100
sphere_size = 50
galcolors = [(1,0,0),(0.2,0.6,1),(0.8,0,0.8),(0,1,0)]

for (k,gal) in enumerate(gals.keys()):

    # Go from RA/Dec -> rescaled pixel space !
    coords = [[ratodeg(gals[gal]['ra']), 
               dectodeg(gals[gal]['dec']),0,0]]
    pixcrd = w.wcs_world2pix(coords, 0)
    
    coords_plot = (np.array(coords)-np.array([ramean,decmean,0,0]))*3600.
    coords_plot[0][0] *= np.cos(np.radians(decmin))

    # Remember that we also flipped x before ...
    pixcrd[0][0] = size_x - pixcrd[0][0]
    
    vel_n = gals[gal]['v']
    
    my_x = coords_plot[0][0]
    my_y = coords_plot[0][1]
    my_z = vel_n
    lw = 5
    
    # Plot the black crosses first ...
    mlab.points3d([my_x],[my_y],
                [my_z],[1.0],
                color=(0,0,0),
                mode = 'axes',
                scale_factor= sphere_size)

    # ... and a sphere at the same location.                    
    mlab.quiver3d([my_x],
                  [my_y - sphere_size/4.],
                  [my_z],
                  [0],[1],[0],
                  scalars = [1],
                  scale_factor = sphere_size/2.,
                  scale_mode = 'scalar',
                  mode = 'sphere',
                  line_width = lw*0.75,
                  name = gal,
                  color=galcolors[k])
                  
    # Finally, add the galaxy name as 3D text.             
    #mlab.text3d(my_x,my_y,my_z,'HCG91'+gal[-1],scale=20,color = (0,0,0))        
    mlab.text(my_x,my_y,'HCG91'+gal[-1],color=(0,0,0),z=my_z,width=0.1) 
                 
# Next, add peculiar HII regions of interest inside HCG 91c
# (See Vogt+, MNRAS (2015) for details)

# First, compute their coordinates                
coords_91c = [[ratodeg(gals['hcg91c']['ra']), 
               dectodeg(gals['hcg91c']['dec']),0,0]]
    
coords_91c_plot = (np.array(coords_91c)-np.array([ramean,decmean,0,0]))*3600.
coords_91c_plot[0][0] *= np.cos(np.radians(decmin))

cube_size = 5
hx1 = coords_91c_plot[0][0] - 3.2 
hx2 = coords_91c_plot[0][0] - 7.0
hx3 = coords_91c_plot[0][0] - 10.5
hy1 = coords_91c_plot[0][1] + 13.5
hy2 = coords_91c_plot[0][1] + 13.5
hy3 = coords_91c_plot[0][1] + 15.3
hv1 = 7244
hv2 = 7235
hv3 = 7230

# Once again, draw both a cube ...
mlab.points3d([hx1,hx2,hx3],[hy1,hy2,hy3],
                [hv1,hv2,hv3],[1.0,1.0,1.0],
                color=(1,1,1),
                mode = 'cube',
                scale_factor= cube_size,
                name = 'HII_regions')

# And crosses for clarity.
mlab.points3d([hx1,hx2,hx3],[hy1,hy2,hy3],
                [hv1,hv2,hv3],[1.0,1.0,1.0],
                color=(0,0,0),
                mode = 'axes',
                scale_factor= 3*cube_size,
                name = 'HII_regions')


# Finally, also add a symbols to mark the location of two HI clumps of interest.
# (See Vogt+, MNRAS (2015) for details)

lw = 5
bx1 = -20
by1 = 65
bz1 = 7190
bx2 = 5
by2 = 125
bz2 = 7230

# Once again, some black axes ...
mlab.points3d([bx1,bx2],[by1,by2],
                [bz1,bz2],[1.0,1.0],
                color=(0,0,0),
                mode = 'axes',
                scale_factor= cube_size*6)

# and a yellow cube.                
mlab.quiver3d([bx1,bx1,bx2,bx2],[by1,by1-cube_size*3/2.,by2,by2-cube_size*3/2.],
                [bz1-cube_size*3/2.,bz1,bz2-cube_size*3/2.,bz2], 
                [0,0,0,0],[0,1,0,1],[1,0,1,0],color=(1,0.7,0),
                scalars = [1,1,1,1],
                scale_factor = cube_size*3,
                scale_mode = 'scalar',
                mode = 'cube',
                line_width = lw*0.75,
                name = 'HI_clumps')
                

# Finally, trace the tidal tail in HI inside the cube, using a cyan cylinder.
tails_x = np.array([-80,-50, 0, 30, 50, 80, 80, 90, 70,50])
tails_y = np.array([0,0, -10,-15, -50, -70, -100, -110,-140,-160])
tails_z = np.array([6995,7010, 7020, 7035, 7070, 7120, 7121, 7170,7215,7220])
rad = 4

mlab.plot3d(tails_x,tails_y,tails_z, color=(0,1,1), tube_radius=rad, 
            name= 'HCG91a_tail')
 
# --- !!! ---
# MAYAVI BUG & WORK-AROUND (#2 continued)
# Normally, the diagram would be complete at this point. 
# However, for the x3d export, we still need to manually include the axis,
# axis labels, and some tick labels. This is tedious, but here we go.
#
# If you do not care about x3d export remove those lines, and set
#
#ax.visible = True
#
# --- !!! ---

# Then, add the axes labels. Include multiple occurance to be visible in the
# top - front - side views in the interactive html model.
mlab.text(200, -350, 'R.A. [arcsec] ',z=6671.3, color = (0,0,0),width=0.2)
mlab.text(350,-200,'Dec. [arsec]', z=6671.3, color=(0,0,0),width=0.2)
mlab.text(-300,-350,'V [km/s]',z=7050,  color=(0,0,0),width=0.1)
mlab.text(-300,-200,'Dec. [arcsec]',z=6620,  color=(0,0,0),width=0.2)
mlab.text(-350,300,'V [km/s]',z=7050,  color=(0,0,0),width=0.1)
mlab.text(-200,300,'R.A. [arcsec]',z=6620, color = (0,0,0),width=0.2)

# Add the axis tick labels ... again more than once, for the 
# interactive html views.
mlab.text(340,  -350, '300',z=6671.3, color = (0,0,0),width=0.05)
mlab.text(-260, -350,'-300',z=6671.3, color = (0,0,0),width=0.05)
mlab.text(420,   280,  '300',z=6671.3, color = (0,0,0),width=0.05)
mlab.text(420,  -320, '-300',z=6671.3, color = (0,0,0),width=0.05)
mlab.text(-300, -350,'6671.3',z=6620, color = (0,0,0),width=0.05)
mlab.text(-300, -350,'7643.7',z=7590, color = (0,0,0),width=0.05)
mlab.text(-300,  280, '300',z=6560, color = (0,0,0),width=0.05)
mlab.text(-300, -320,'-300',z=6560, color = (0,0,0),width=0.05)
mlab.text(-350,  300, '6671.3',z=6620, color = (0,0,0),width=0.05)
mlab.text(-350,  300, '7643.7',z=7590, color = (0,0,0),width=0.05)
mlab.text( 280,  300, '300', z=6560, color = (0,0,0),width=0.05)
mlab.text(-320,  300, '-300',z=6560, color = (0,0,0),width=0.05)

# Finally, add some tick lines in the middle of the top-front-side panels
mlab.plot3d([-300,300],[0,0],[np.min(vs),np.min(vs)], color=(0,0,0), 
            tube_radius=1)
mlab.plot3d([0,0],[-300,300],[np.min(vs),np.min(vs)], color=(0,0,0), 
            tube_radius=1)
mlab.plot3d([0,0],[np.max(decs),np.max(decs)],[6671.3,7643.7], color=(0,0,0), 
            tube_radius=1)
mlab.plot3d([-300,300],[np.max(decs),np.max(decs)],[7157.5,7157.5],color=(0,0,0), 
            tube_radius=1)
mlab.plot3d([np.min(ras),np.min(ras)],[0,0],[6671.3,7643.7], color=(0,0,0), 
            tube_radius=1)
mlab.plot3d([np.min(ras),np.min(ras)],[-300,300],[7157.5,7157.5], color=(0,0,0), 
            tube_radius=1)

# All done !
# Save it & export the diagram
mlab.savefig(plot_loc + 'HCG91.x3d')
mlab.savefig(plot_loc + 'HCG91.png')

# Show it !
mlab.show()
