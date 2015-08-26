README: x3d_to_png
------------------

Provided in this supplementary material are three Python scripts which automatically produce animated scenes in Blender based on several X3D files:

'green_dice_animation.py', 'red_dice_animation.py' and 'HCG91_animation.py'

These scripts require only a default copy of Blender, which can be downloaded for free on Windows/Mac/Linux at http://www.blender.org/  The other files required (the X3D files, and the scripts themselves) are available as part of this supplementary material. Please ensure that you are using an up-to-date copy of Bender: these scripts have been developed with Blender v2.75.

The scripts are designed to increase in complexity:

green_dice_animation.py
This example is designed to be fairly simple.  It sets up a basic scene, imports the X3D meshes, applies some basic materials, and adds a simple animation to the camera.

red_dice_animation.py
This example is a bit more complex, though not necessarily more difficult.  Here we use some more complicated material designs, and do some additional operations to split apart the X3D mesh.

HCG91_animation.py
This is a more "real world" astrophysical example.  We import HCG91's HI density contours from an X3D file, rescale/relocate the mesh, apply some semi-transparent materials, add new objects to the scene to represent the galaxy positions, animate the camera, etc.  We also create a second scene with text overlays which change dynamically with which galaxy is being illuminated during the animation.


- How to execute the scripts in Blender

These scripts are executed by coping/pasting them into one of Blender's "Text Editor" windows.  You can open such a window by one of the following:

1) Converting the default screen layout into the "Scripting" mode (from the drop down menu at the top of the screen next to the "help" option).

2) Converting one of the current windows into a Text Editor by clicking the icon in a window's lower left and selecting the "Text Editor" option. 

Once you have a Text Editor window open, simply click "New" at the bottom of the window, copy/paste the script into the editor, and hit "Run Script".
Make sure to update the location of the model's file accordingly at the top of the script.


- How to render/animate the scene

Once the script has been executed, the 3D viewport should show the newly created scene populated with objects from the X3D file.  The user can now play around with various elements (change materials, add new objects, change the render options, etc), or they can instantly render out the image/animation.

Each script has a few lines specifying the X3D file location and output image directory(s) at the very top.  The user should alter these to reflect where they have saved the X3D models to, and where they'd like the animation frames to be saved to.

Once the file locations are correctly set, the user simply has to press the "Render" or "Animation" button on the panel to the right of the screen (the Render tab should be open by default in the right panel, otherwise make sure the tab with the image of the camera has been selected).

- If the user hits "Render", a single frame will be rendered out.  By default these individual frames are not written to the hard drive, so the user can save the file in the rendered frame's window by selecting the "Image >> Save As Image" option.

- If the user hits "Animation", the full animation will be rendered out and the frames will automatically be written to the supplied directory.  Note that depending on the complexity of the scene, length of the animation, and the specifications of the user's computer, this process can take a long time.  The time taken for each frame to render is reported at the top of the render screen, so the user can approximate the time it will take for the full set of frames to render.  

By default, these animations will render out as a sequence of images rather than a movie file.  This is done for practical purposes; if Blender crashes while rendering, the user can simply restart from where they left off without having to re-render portions of their movie.  However, it means they'll need to stitch all of the images back into a movie once the process has finished.  This can be done easily using free software like FFmpeg (Mac), VirtualDub (Windows), or in Blender itself using it's internal sequencer.  


- For more information

Note that the goal of these scripts isn't to provide a tutorial on the general use of Blender.  For a much more thorough introduction on the program for astronomers, the user is referred to "Visualizing Astronomical Data with Blender" by Kent (2013): http://arxiv.org/abs/1306.3481  Additionally, Blender is an extremely popular program, so most beginner problems/questions can be easily answered with simple searches in Google/YouTube.


*** Basic file descriptions ***

green_dice_animation.py: Python & Blender animation script
red_dice_animation.py:  Python & Blender animation script
HCG91_animation.py:  Python & Blender animation script

green_dice.mov: animation
red_dice.mov: animation
HCG91.mov: animation (generate from HCG91_animation.py)
HCG91_extended.mov: animation (more complex than HCG91.mov, designed to illustrate additional capabilities of Blender, and designed with a dedicated script available on demand).

green_dice.x3d: X3D file generated via green_dice.py
red_dice.x3d: X3D file generated via red_dice.py
HCG91.x3d: X3D file generated via HCG91.py

