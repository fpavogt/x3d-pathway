README: x3d_to_stl
------------------

The "ready-to-3-D-print" model of the HI gas content of the compact group of galaxies HCG 91 is contained in

'HCG91.stl'

The model was generated using Blender by manually adding support structures to the base 3-D model exported to X3D using Python. Although the manual Blender steps could be scripted, such a script would be of little interest as it would be very specific to this specific model. 

We do provide the Blender file for the 3-D printable model, which can be used to experiment with the inclusion of additional support structures. In particular, the Blender files contains an 'alternative' simple square base to experiment with.

To add a base to the model inside Blender, the required (minimal) steps are:

1) use the Boolean modifier for the main "HI" structure to 'Union' it with one of the two bases provided: this will result in a complete 3-D model ready to print. The screenshot "adding_a_base.png" illustrates how to perform this step.

2) select the combined structure, and export it as an STL file using "File -> Export as …".

Adding additional structures, columns, plates, etc … can be achieved using the "Add -> Mesh -> …" functions. The internet is full of step-by-step Blender tutorials which will be of much better quality than anything we could include in this README.

Finally, for completeness, a cover image for the sliding rack is also provided. These images are extracted from Vogt+, MNRAS (2015), and included here with authorisation from MNRAS.

*** Basic file descriptions ***

HCG91.stl: 3-D printable file

adding_a_base.png: screenshot of the Blender GUI illustrating how to merge a base plate with a 3-D model.
HCG91.blend: Blender file containing the 3-D model of HCG91 prior to the union of the base plate.
HCG91_dss+VLA.png: image for inclusion inside the sliding rack







 




