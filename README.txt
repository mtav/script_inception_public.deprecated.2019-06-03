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

Blender scripts installation HOWTO:
-----------------------------------

I still need to make it a bit more user-friendly, but to install it, here's what you have to do:

1) Install blender 2.49b (so, not the latest version, but I'll try to fix that later. The problem is that the latest blender version uses python 3 instead of python 2.6)

http://download.blender.org/release/Blender2.49b/blender-2.49b-windows.exe

2) Install python 2.6 (normally, there is a bundled package with blender+python, but apparently they only keep it for the latest stable release)

http://www.python.org/download/releases/2.6.6/

3) Download and extract the latest version of the repository wherever you want, let's say "H:\script_inception_public" for example.

4) copy all the .py files from "H:\script_inception_public\blender_scripts" into "C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender\scripts"

5) Define the following environment variables (cf http://support.microsoft.com/kb/310519 for how to do this) :

* DATADIR = H:\ (or whatever else you want to use as the default import directory. It doesn't matter much, since the import script will store the last directory you imported from. I'm going to change it so this variable isn't mandatory anymore)

* PYTHONPATH = H:\script_inception_public

