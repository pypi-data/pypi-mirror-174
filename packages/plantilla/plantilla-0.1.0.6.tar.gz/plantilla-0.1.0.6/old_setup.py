import atexit
from setuptools                 import setup
from setuptools.command.install import install

def _post_install():
    import goosempl
    package_name.copy_style()

class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

__version__ = '0.0.8'

setup(
    name              = 'plantilla',
    version           = __version__,
    install_requires  = ['matplotlib>=2.0.0'],
    packages          = ['plantilla'],
    cmdclass          = {'install': new_install},
    package_data      = {'plantilla/styles':[
        'plantilla/styles/mecon.mplstyle'
    ]},
)