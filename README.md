# Blender3D tools

This repository holds an evolving set of scripts useful for importing / manipulating data within Blender3D for geologists / the mining industry.

## import_drill.py

Imports drill data as *cylinders* from a file, makes the cylinder the length of the interval, rotates the cylinder according to azimuth and dip, and displays a color from a single attribute.
File must have the following data: [x, y, z, azimuth, dip, length, attribute].
User of the script must specify the column # for the specific variable of each item above.  *Remember!* indexing of the columns starts at 0 not 1!  Therefore human counted column #1 is actually index 0, so when specifying the column number in the script, remember to start at 0 (not 1).

**UNTESTED**


## import_points.py

Imports any data as *points* aka *spheres* from a file... not necessarily needing to be drill data.  Examples: soil assays.  Same as ```import_drill.py``` but does not require azimuth, dip or length.

**UNTESTED**
