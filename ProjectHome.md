# Opioid2D #
A python 2D graphics engine and game framework, with C++ swig bindings to opengl.

Documentation can be found in Downloads section. Example and test code can be found in the source distributions.

Current version - 0.6.5 released 3-21-11

## requirements ##
  * python 2.6 (original 2.5 version available in download section)
  * pyopengl
  * pygame
  * numpy
For Mac and linux, use the .gz source package, which has a number of requirements that aren't obvious: build-essential, python-dev, libgl1-mesa-dev, and swig.

### Changes made since 2006 release from original author ###
  * works with python 2.6
  * works with numpy instead of numeric (which is no longer supported)
  * ability to order sprites within a layer and layers within a scene

### Note from maintainer ###
This library was originally created by Sami Hangaslammi. I have never managed to contact him, and his work has not been available on the web for years, but I use his code and I've decided to maintain it and update it as necessary. Starting at 0.6.5 I have changed the release numbering system. The release before 0.6.5 was 6.4.
The project I use this engine for is a 2D game/art editor environment called pig. You can find it at http://code.google.com/p/pug.
