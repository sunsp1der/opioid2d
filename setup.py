#!/usr/bin/python
DEBUG = False

import sys, os, re

#from distutils.dir_util import remove_tree
#try:
#    remove_tree('build')
#except:
#    pass

sys.path.append("pyimpl")

from distutils.core import setup, Extension

def find_version():
    f = open(os.path.join("pyimpl", "Opioid2D", "__init__.py"))
    s = f.read()
    f.close()
    m = re.search(r'__version__ = "(.*)"', s)
    return m.group(1)

def find_packages(root):
    packages = []
    for dirpath, dirnames, filenames in os.walk('pyimpl/%s' % root):
        try:
            dirnames.remove("obsolete")
        except:
            pass
        if '__init__.py' in filenames:
            package = dirpath.replace(os.path.sep, '.')
            print package
            packages.append(package[7:])
    return packages

def find_sources(dir):
    sources = []
    l = os.listdir(dir)
    return [os.path.join(dir,fn) for fn in l if fn.endswith(".cpp") or fn.endswith(".cxx")]

def find_files(dir, *ext):
    files = []
    l = os.listdir(dir)
    for fn in l:
        for e in ext:
            if fn.endswith("."+e):
                break
        else:
            continue
        files.append(os.path.join(dir,fn))
    return files

macros = []
dlls = []
libdirs = []
incdirs = ["include", "swig_dist"]

libraries = []
extra_link_args = []
extra_compile_args = []

macros.append(("USE_FLOATS",None))

platform = sys.platform

if platform == 'win32' and '--compiler=mingw32' in sys.argv:
        platform = 'mingw32'

if platform == 'win32':
    macros.append(("O2D_MINGW", None))
    dlls = find_files("winbuild/dlls", "dll")
    libdirs = ["winbuild/lib"]
    incdirs.append("winbuild/include")
    #libraries = ["OpenGL32", "SDL", "SDL_image", "SDLmain", "SDL_ttf"]
    libraries = ["OpenGL32"]
    extra_compile_args = ["/GR", "/w"]
    extra_link_args = ["-enable-auto-import"]
elif platform == 'mingw32':
    macros.append(("O2D_MINGW", None))
    dlls = find_files("winbuild/dlls", "dll")
    libdirs = ["winbuild/lib", "/mingw/lib"]
    incdirs.append("winbuild/include")
    libraries = ["OpenGL32", "supc++"]
    extra_link_args = ["-enable-auto-import"]
elif sys.platform == 'darwin':
    #extra_link_args = ["-framework", "OpenGL", "-framework", "SDL", "-framework", "SDL_image", "-framework", "SDL_ttf"]
    extra_link_args = ["-framework", "OpenGL"]
    macros.append(("DARWIN", None))
    incdirs.append("/System/Library/Frameworks/OpenGL.framework/Headers")
    #incdirs.append("/Library/Frameworks/SDL.framework/Headers")
    #incdirs.append("/Library/Frameworks/SDL_image.framework/Headers")
    #incdirs.append("/Library/Frameworks/SDL_ttf.framework/Headers")
else:
    #libraries = ["GL", "SDL", "SDL_image", "SDL_ttf"]
    libraries = ["GL"]

if DEBUG:
    macros.append(("DEBUGGING", None))

cOpi = Extension(
    '_cOpioid2D',
    find_sources("src")+find_sources("swig_dist"),
    include_dirs = incdirs,
    define_macros = macros,
    library_dirs = libdirs,
    libraries = libraries,
    extra_link_args = extra_link_args,
    extra_compile_args = extra_compile_args,
    )

#################################################################
# smart_install_data class copied from pygame distrbution
# (c) Pete Shinners
from distutils.command.install_data import install_data

class smart_install_data(install_data):
    def run(self):
        #need to change self.install_dir to the actual library dir
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return install_data.run(self)
#################################################################

cmdclass = {}    
cmdclass['install_data'] = smart_install_data

setup(
    cmdclass = cmdclass,
    
    name = "Opioid2D",
    version = find_version(),
    author = "Sami Hangaslammi",
    author_email = "shang@iki.fi",
    maintainer = "Ivan DelSol",
    maintainer_email = "sunsp1der@yahoo.com",
    package_dir = {'': 'pyimpl'},
    packages = find_packages("Opioid2D")+find_packages("OpioidTools"),
    package_data = {
        'Opioid2D': ['data/*.ico', 'data/*.png'],
        },
    py_modules = ["cOpioid2D"],
    scripts = ["scripts/o2d.py"],

    ext_modules = [cOpi],

    extra_path = "Opioid2D",

    data_files = [('', dlls)]
    )
    
