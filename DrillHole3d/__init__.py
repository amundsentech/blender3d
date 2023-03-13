import bpy
import bmesh
import addon_utils as addons
import pkgutil
import importlib
from importlib.metadata import version
from pathlib import Path
import subprocess
import sys
import site
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "DrilHole3d",
    "author" : "SebC",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "3D View",
    "addons": ["BlenderGIS"]
}

pkgs = {'pandas': 'pandas',
 'tqdm': 'tqdm',
 'numpy':'numpy',
 'openpyxl':'openpyxl',
 'debugpy':'debugpy',
 'pyproj':'pyproj',
#  'GDAL':'GDAL',
 'matplotlib':'matplotlib'
 }

import subprocess
import sys
import os
 


from . import auto_load

pybin=sys.executable
target_lib = Path(pybin).parent.parent / "lib"
def add_user_site():
    # Locate users site-packages (writable)
    user_site = subprocess.check_output([pybin, "-m", "site", "--user-site"])
    user_site = user_site.decode("utf8").rstrip("\n")   # Convert to string and remove line-break
    # Add user packages to sys.path (if it exits)
    user_site_exists = user_site is not None
    if user_site not in sys.path and user_site_exists:
        sys.path.append(user_site)
    return user_site_exists

def enable_pip():
    print('######### ENSURE PIP #######')
    if importlib.util.find_spec("pip") is None:
        subprocess.check_call([pybin, "-m", "ensurepip",])
        subprocess.check_call([pybin, "-m", "pip", "install", "--upgrade", "pip",])

def check_packages():
    print('######### ENSURE PACKAGES #######')


    for p in pkgs:
        
        print('######### EXECUTABLE_PATH:',pybin)
        print('######### Tasrget install:',target_lib )
        s = pkgs[p]
        try:
            print(f'check for {p}')
            s = importlib.import_module(p)
            
        except ImportError:
            print(f'{p} is not installed and has to be installed')
            subprocess.call([pybin, '-m', 'pip', 'install', p,'-t',target_lib  ])
        finally:
            try:
                s = importlib.import_module(p)
                print(f'{p} is properly installed')
            except Exception as e:

                print('##### Package not installed #####')
                print(f'{p} was not properly installed')
                print(e)
    return

def check_xl_version():
    try:
        xl=version('openpyxl')
        xl.split('.')
        vers=xl.split('.')
        vers=[int(v) for v in vers]
        if  vers[0]!=3 and vers[1]!=1 and vers[-1]!=0 :
            print(xl,'wrong version')
            subprocess.call([site.sys.executable, '-m', 'pip', 'install', '--force-reinstall','-v', "openpyxl==3.1.0",'-t',target_lib ])
    except Exception as e:
        print('#### expection on PYXL#####')
        print(e)

## ADD THE BLENDER PYTHON LOCATION
# user_site_added = add_user_site()
## IF NO PIP ENBALE PIP
enable_pip()
## CHECK PACKAGES
check_packages()

check_xl_version()




auto_load.init()


def register():
    auto_load.register()

def unregister():
    auto_load.unregister()


if __name__ == "__main__":
    enable_pip()
    ## CHECK PACKAGES
    check_packages()

    check_xl_version()
    register()