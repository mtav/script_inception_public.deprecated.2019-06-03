What this is:
-------------
Useful scripts for MEEP and Bristol FDTD and maybe other stuff :)

The idea is to centralize scripts used by almost everyone to reduce code duplication and therefore errors and time wasting, as well as improve the overall quality of code over time.

License:
--------
Unless otherwise specified inside a file or folder, everything is under GPLv3 (cf COPYING.txt).

The following (written by Ian Buss) are under the LGPL:

* Bris2Meep

* Postprocessor

* Geo2Str

Links:
------
For more info: https://wikis.bris.ac.uk/display/Photonics/Public+scripts+repository

Blender scripts
---------------

Installation HOWTO:
~~~~~~~~~~~~~~~~~~~

I still need to make it a bit more user-friendly, but to install it, here's what you have to do (tested on Windows XP):

1) Install python 2.6 (normally, there is a bundled package with blender+python, but apparently they only keep it for the latest stable release)

http://www.python.org/download/releases/2.6.6/

2) Install numpy from:

http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.6.exe/download

3) Install blender 2.49b (so, not the latest version, but I'll try to fix that later. The problem is that the latest blender version uses python 3 instead of python 2.6)

http://download.blender.org/release/Blender2.49b/blender-2.49b-windows.exe

4) Download and extract the latest version of the repository wherever you want, let's say "H:\script_inception_public" for example.

5) Copy all the .py files from "H:\script_inception_public\blender_scripts" into "C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender\scripts"

_ Note 1: The "Application Data" folder may be hidden. To unhide it: http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/win_fcab_show_file_extensions.mspx?mfr=true _

_ Note 2: The .py extensions may be hidden, but just copy all the contents of the folder. The other files shouldn't cause problems. _

6) Copy the .B.blend file from "H:\script_inception_public\blender_scripts" into "C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender"

7) Define the following environment variables (cf http://support.microsoft.com/kb/310519 for how to do this) :

* DATADIR = H:\ (or whatever else you want to use as the default import directory. It does not matter much, since the import script will store the last directory you imported from. Im going to change it so this variable isnt mandatory anymore)

* PYTHONPATH = H:\script_inception_public (Use the folder you chose in step 4)

Ok, you are now ready to import BFDTD files with blender.

Usage instructions:
~~~~~~~~~~~~~~~~~~~
1) Start blender

2) File->Import->Bristol FDTD

3) Search for .geo,.inp or .in files and import them (Tip: middle-click on a file opens it)

Other blender scripts:
~~~~~~~~~~~~~~~~~~~~~~

1) Layer manager:
^^^^^^^^^^^^^^^^^

It makes it easier to show/hide the diverse components of the BFDTD files.

To use it, in the "scripts window", click on "Scripts->System->Layer manager".

2) Blender caliper:
^^^^^^^^^^^^^^^^^^^

To show dimensions, etc, you can use the blender caliper script.

To use it, in the "scripts window", click on "Scripts->Wizards->Blender caliper".
