import os
import sys
from glob import glob
from esky import bdist_esky
from distutils.core import setup
from setuptools import setup

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def get_all_files_from_dir(dir_name, excluded=None):
    all_files = []
    for dir_info in os.walk(dir_name):
        path = dir_info[0]
        files = dir_info[2]
        files_in_dir = []
        for file_name in files:
            path_with_filename = "%s%s%s" % (path, os.sep, file_name)
            if not excluded or not path_with_filename in excluded:
                files_in_dir.append(path_with_filename)
        all_files.append((path, files_in_dir))
    return all_files

def get_data_files():
    # These are the files I add manually, on the left are directory name where these files are copied to, and on the right are the files that will be copied
    # You need to specify subfolder separately (like I do for .cache/images)
    # I use dummy files dont-delete to include empty folders
    data_files = [
        ('templates', glob('/Users/ArtificialStudent/anaconda/pkgs/python-docx-0.8.6-py27_1/lib/python2.7/site-packages/docx/templates/*'))
    ]
    
    return get_all_files_from_dir('./')



APP = ['Main_Storyboard.py']
DATA_FILES = get_data_files()

OPTIONS = {
    'argv_emulation': True,
    'iconfile' : 'AEICON.icns',
    'packages': ['PIL']
}

setup(
    name="Artificial Education",
    version="0.1",
    scripts=["Main_Storyboard.py"],
    data_files=DATA_FILES,
    options={"bdist_esky": {
        "freezer_module": "py2app",
        "freezer_options": OPTIONS
    }}
)