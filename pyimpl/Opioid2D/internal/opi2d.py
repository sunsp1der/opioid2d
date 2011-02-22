"""Initialization functions.

Do not call this explicitly from your code. These are just internal helpers
"""

import cOpioid2D as _c
from Opioid2D.public.Director import Director
from Opioid2D.public.Display import Display
from Opioid2D.public.Keyboard import Keyboard
from Opioid2D.public.Sprite import SpritePool
from Opioid2D.internal.objectmgr import ObjectManager
import Opioid2D.internal.spritemap as spritemap

class Opi2D(object):
    def __init__(self):
        _c.InitOpioid2D()
        Director._cDirector = _c.Director.GetInstance()
        Display._cDisplay = _c.Display.GetInstance()
        spritemap.SpriteMapper = _c.SpriteMapper.GetInstance()

    def cleanup(self):
        SpritePool.clear()
        SpritePool.clearing = True
        Director._cDirector.SetScene(None)
        ObjectManager.purge()
        ObjectManager.purge()
        #print "purged"        
        Display._cDisplay = None
        ObjectManager.objects.clear()
        #print "cleared"
        Director.scene = None
        #print "scene detached"
        _c.Director.Destroy()
        #print "cDirector destroyed"
        #print "quitting"
        _c.QuitOpioid2D()
        #print "quit succesful"
        
