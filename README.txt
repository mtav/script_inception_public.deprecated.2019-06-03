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

. Install python 2.6 (normally, there is a bundled package with blender+python, but apparently they only keep it for the latest stable release): +
http://www.python.org/download/releases/2.6.6/

. Install numpy from: +
http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.6.exe/download

. Install blender 2.49b (so, not the latest version, but I'll try to fix that later. The problem is that the latest blender version uses python 3 instead of python 2.6) +
http://download.blender.org/release/Blender2.49b/blender-2.49b-windows.exe

. Download and extract the latest version of the repository wherever you want, let's say *H:\script_inception_public* for example: https://github.com/mtav/script_inception_public/archives/master

. Copy all the .py files from *H:\script_inception_public\blender_scripts* into *C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender\scripts* +
_Note 1: The "Application Data" folder may be hidden. To unhide it: http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/win_fcab_show_file_extensions.mspx?mfr=true_ +
_Note 2: The .py extensions may be hidden, but just copy all the contents of the folder. The other files shouldn't cause problems._

. Copy the file *H:\script_inception_public\blender_scripts\.B.blend* into *C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender* +
_Note: This is just to set up a nicer default workspace, so it is optional. You can save your workspace as the default at any time in Blender with *File->Save default settings*._

. Define the following environment variables (cf http://support.microsoft.com/kb/310519 for how to do this) :

* *DATADIR = H:\* (or whatever else you want to use as the default import directory. It does not matter much, since the import script will store the last directory you imported from. I am going to change it so this variable is not mandatory anymore)
* *PYTHONPATH = H:\script_inception_public* (Use the folder you chose in step 4)

Ok, you are now ready to import BFDTD files with blender.

Example filestructure after installation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
H:\script_inception_public\addpath_recurse +
H:\script_inception_public\README.html +
... +
H:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender\.B.blend +
H:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender\scripts\FDTDGeometryObjects.py +
...

Usage instructions:
~~~~~~~~~~~~~~~~~~~

. Start blender

. *File->Import->Bristol FDTD*

. Search for .geo,.inp or .in files and import them (Tip: middle-click on a file opens it)

Other blender scripts:
~~~~~~~~~~~~~~~~~~~~~~

1) Layer manager:
^^^^^^^^^^^^^^^^^

It makes it easier to show/hide the diverse components of the BFDTD files. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->System->Layer manager*.

2) Blender caliper:
^^^^^^^^^^^^^^^^^^^

To show dimensions, etc, you can use the blender caliper script. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->Wizards->Blender caliper*.

Matlab/Octave scripts:
----------------------
To effectively use the Matlab/Octave scripts from this repository, you should add the paths to your Matlab/Octave path. +

. First of all, edit *startup.m* by setting *PUBLIC_REPO_DIR* to the directory where you placed the repository (ex: _H:\script_inception_public_):
+
----
    % Adapt those settings according to your setup and where you placed the repository
    PUBLIC_REPO_DIR = H:\script_inception_public;
----
+
. Then:

If you use Matlab:
~~~~~~~~~~~~~~~~~~
For Matlab, there are several ways to do this. Choose one of the following options:

* Copy *startup.m* from the repository into your Matlab startup folder (you can find out what it is by running *userpath()* in Matlab). Restart Matlab and it should run the startup.m script and recursively add the necessary folders.
* Add the repository recursively in Matlab: *File->Set path...->Add with subfolders...*, select the repository, then *Save*.
* If you don't use any startup script already, you can also simply add just the repository folder *File->Set path...->Add folder...*, select the repository, then *Save*. Matlab will then use the startup script from the repository.
* Edit your own *startup.m* appropriately.

To test if it works, you can run *get_c0()* for example or *postprocessor()*.

_Note: You can also set up the environment variable *MATLABPATH* to define the Matlab search path._

If you use Octave:
~~~~~~~~~~~~~~~~~~
Under GNU/Linux:
----
ln -s $PATH_TO_REPO/.octaverc ~/.octaverc 
----
