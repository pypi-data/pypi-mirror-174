import atexit
import glob
import os
import shutil
import matplotlib
from setuptools import setup
from setuptools.command.install import install

def install_styles():

    # Find all style files
    stylefiles = glob.glob('styles/**/*.mplstyle', recursive=True)

    # Find stylelib directory (where the *.mplstyle files go)
    mpl_stylelib_dir = os.path.join(matplotlib.get_configdir() ,"stylelib")
    if not os.path.exists(mpl_stylelib_dir):
        os.makedirs(mpl_stylelib_dir)

    # Copy files over
    print("Installing styles into", mpl_stylelib_dir)
    for stylefile in stylefiles:
        print(os.path.basename(stylefile))
        shutil.copy(
            stylefile, 
            os.path.join(mpl_stylelib_dir, os.path.basename(stylefile)))

class PostInstallMoveFile(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(install_styles)


__version__ = '0.1.0.6'

setup(
    name='plantilla',
    package_data={
        'styles': [
            "mecon.mplstyle"
        ]
    },
    version=__version__,
    packages=['plantilla'],
    include_package_data=True,
    install_requires=['matplotlib>=2.0.0',],
    cmdclass={'install': PostInstallMoveFile,},
)