"""Display - setting up and querying the viewport
"""
__all__ = [
    "Display",
    ]

import cOpioid2D as _c

from Opioid2D.internal.utils import deprecated
from Opioid2D.public.Mouse import Mouse

class Display(object):
    """Display

    Class for intializing and querying information about the screen.
    """
    _cDisplay = None

    @deprecated
    def Init(self, resolution, units=None, title="Opioid2D", fullscreen=False, icon=""):
        self.init(resolution, units=None, title="Opioid2D", fullscreen=False, icon="")
    def init(self, resolution, units=None, title="Opioid2D", fullscreen=False, icon=""):
        """Initialize the display.

        This method opens a window or intializes fullscreen view for the
        application.

        resolution - size of the window or screen resolution in fullscreen
        units - view port size in units (defaults to resolution)
        title - window title
        fullscreen - flag signalling wether to use windowed mode (False) or fullscreen (True)
        """
        import sys, pygame, os
        import Opioid2D
        if units is None:
            units = resolution
        xres, yres = resolution
        pygame.init()
        flags = pygame.OPENGL|pygame.DOUBLEBUF|pygame.HWSURFACE
        if (fullscreen):
             flags |= pygame.FULLSCREEN

        pygame.display.set_caption(title)

        if icon is not None:
            if icon == "":
                icon = os.path.join(Opioid2D.__path__[0], "data", "o2dicon.png")
            img = pygame.image.load(icon)
            pygame.display.set_icon(img)

        pygame.display.set_mode((xres,yres), flags)

        self._cDisplay.InitView(xres, yres, *units)

        self.resolution = resolution
        self.units = units
        Mouse._mscalex = float(units[0])/resolution[0]
        Mouse._mscaley = float(units[1])/resolution[1]
        

    @deprecated
    def GetResolution(self):
        return self.resolution
    def get_resolution(self):
        """Return current screen resolution as a (width,height) tuple"""
        return self.resolution

    @deprecated
    def GetViewSize(self):
        return self.units
    def get_view_size(self):
        """Return current viewport size in units as a (width,height) tuple"""
        return self.units

    @deprecated
    def SetClearColor(self, rgba):
        self.set_clear_color(rgba)
    def set_clear_color(self, rgba):
        if rgba is None:
            self._cDisplay.EnableClearing(False)
        else:
            self._cDisplay.SetClearColor(_c.Color(*rgba))
    
Display = Display()
