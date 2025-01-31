README: fits_to_x3d
-------------------

The Python scripts

'green_dice.py', 'red_dice.py', 'HCG91.py'

located in their respective folders illustrate how the Mayavi Python package can be used to create interactive 3-D diagrams, and export them to X3D files. 

Each script is commented throughout for clarity. To run them, launch a Python shell and type (e.g. for the green dice example):

run green_dice.py

You will need an up-to-date Python installation. The minimal set of packages required are:

- Mayavi from Enthought (at least v4.4.0)
- astropy (at least v1.0.1, also tested with 1.0.5)
- numpy (at least v1.8.1, also tested with 1.10.1)

If you are new to Python (or simply want a fresh Python environment to work with), you may use Anaconda following these steps:

1.- Install anaconda from: https://www.continuum.io/downloads

2.- Run the following commands in a terminal
cmd$ conda update conda
cmd$ conda create --name x3ds python=2.7.10 numpy astropy mayavi
cmd$ source x3ds
cmd$ source activate x3ds
cmd$ pip install numpy --upgrade
cmd$ pip install astropy --upgrade
cmd$ pip install mayavi --upgrade

3.- check your versions:
cmd$ pip freeze | grep numpy
cmd$ pip freeze | grep astropy
cmd$ pip freeze | grep mayavi

*** Basic file descriptions ***

green_dice.py: Python script
green_dice.png: Image generated by the Python script green_dice.py
green_dice.x3d: X3D file generated by the Python script green_dice.py

red_dice.py: Python script
red_dice.png: Image generated by the Python script red_dice.py
red_dice.x3d: X3D file generated by the Python script red_dice.py

HCG91.py: Python script
HCG91.png: Image generated by the Python script green_dice.py
HCG91.x3d: X3D file generated by the Python script green_dice.py
HCG91.fits: reduced VLA datacube
HCG91.dat: correspondence between slice number and absolute velocity for the VLA datacube




