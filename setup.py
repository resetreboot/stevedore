import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
import os, sys, shutil

setup(
    name = "stevedore",
    version = "0.1",
    packages = find_packages('src', exclude=['distribute_setup']),
    # install_requires = ['pygtk>=2.0'],
    scripts = ['src/stevedore.py','src/docker.py'],
    entry_points = {
        'gui_scripts': [
            'stevedore = stevedore:MainApp.start',
        ]
    },
    package_data = {
        # If any package contains *.glade files, include them:
        '': ['*.glade'],
    },
    data_files=[('usr/share/stevedore',
    ['res/stevedore128x128.png',
     'res/stevedore64x64.png',
     'res/stevedore32x32.png',
     'res/stevedore16x16.png',
     'res/stevedore.glade'])],

    # metadata for upload to PyPI
    author = "Jose Carlos Cuevas",
    author_email = "reset.reboot@gmail.com",
    description = "Graphic application in GTK to manage and build docker containers.",
    license = "GPLv3",
    keywords = "docker container gtk gnome",
    url = "",   # project home page, if any
)

if sys.platform == 'linux2':
    osdatadir = '/usr/share/'
    ospixmapdir = '/usr/share/pixmaps'

elif sys.platform == 'win32':
    osdatadir = 'C:\\Program Files\\'
    ospixmapdir = osdatadir + 'stevedore'

# Creamos ciertos directorios...
try: 
    os.mkdir(osdatadir + 'stevedore')

    if sys.platform != 'linux2':
        os.mkdir(ospixmapdir)

except OSError:
    pass

# Ahora copiamos ficheritos aqui y alli...
shutil.copy('res/stevedore.glade',osdatadir + 'stevedore')
shutil.copy('res/stevedore16x16.png',ospixmapdir)
shutil.copy('res/stevedore32x32.png',ospixmapdir)
shutil.copy('res/stevedore64x64.png',ospixmapdir)
shutil.copy('res/stevedore128x128.png',ospixmapdir)

if sys.platform == 'linux2':
    shutil.copy('resources/stevedore.desktop','/usr/share/applications')
