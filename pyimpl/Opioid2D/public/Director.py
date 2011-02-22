"""Director

This module define the Director singleton object that 
"""

__all__ = [
    "Director",
    ]

import time


from Opioid2D.internal.utils import deprecated
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.public.Image import ImageMeta
from Opioid2D.public.ResourceManager import ResourceManager
import sys, traceback

class Director(object):
    """Director

    The Director singleton is the main controller of the software
    runtime. It handles transitions from one scene to another, updates
    the screen and calls event and collision handlers.
    """
    _cDirector = None
    
    @deprecated
    def Run(self, initialScene, *args, **kw):
        return self.run(initialScene, *args, **kw)
    
    def run(self, initialScene, *args, **kw):
        """Run the Director mainloop until program exit
        """
        try:
            # This is a long and ugly function that hasn't been splitted into smaller parts
            # because of performance considerations.
            #
            
            import pygame
            pygame.init()
            from Opioid2D.public.Mouse import Mouse
            
            # Bind functions to local names in order to increase performance
            sleep = time.sleep
            throttle = pygame.time.Clock()
            flip = pygame.display.flip
            get_ticks = pygame.time.get_ticks
            cD = self._cDirector
            OM = ObjectManager
            
            self._scene = None
            self.next_scene = None
            self.next_state = None
            
            now = get_ticks()
            cD.Start(now)

            self.set_scene(initialScene, *args, **kw)
            
            self._running = True            
            start = time.time()
            frames = 0
            self.delta = 0
            ticker = cD.GetTicker()
            old_ticks = now
            self.now = now
            
            # Preload Image subclasses that have been imported and that
            # contain the preload flag.
            for img in ImageMeta.subclasses:
                if img.preload:
                    ResourceManager.get_image(img)
                    
            while self._running:
                # Trigger possible scene change at the beginning of a new frame
                if self.next_scene is not None:
                    self._change_scene()
                
                # Time delta calculation
                ticks = get_ticks()
                self.delta = delta = min(ticks-old_ticks, 25) # limit the virtual clock to a max. advance of 25ms per frame
                old_ticks = ticks
                self.now = now = now + delta
                cD.Iterate(now)
                
                scene = self._scene
                cscene = scene._cObj
                cscene.Tick()
                
                # Event handling
                ev = pygame.event.get()
                if scene._gui is not None:
                    scene._gui.tick(ev)
                scene._handle_events(ev)
                
                # Call Scene tick callbacks
                if scene._tickfunc is not None:
                    scene._tickfunc()
                if ticker.realTick:
                    if scene._realtickfunc is not None:
                        scene._realtickfunc()
                
                # Manage state change within the scene
                while self.next_state is not None:
                    s = self.next_state
                    self.next_state = None
                    self.scene._init_state(s)
                
                # Update the screen
                cD.RenderFrame()
                
                # render software mouse cursor
                ms = Mouse._sprite
                if ms:
                    ms.position = Mouse.position
                    ms._cObj.TraverseFree()
                
                flip()
                
                # Purge managed C++ objects that have been killed on the C++ side.
                OM.purge()
                
                frames += 1
                throttle.tick(100) # limit FPS to 100 for lower CPU usage
            end = time.time()
        finally:
            from Opioid2D import _opi2d
            _opi2d.cleanup()
        return frames/(end-start)

    @deprecated
    def SetScene(self, sceneClass, *args, **kw):
        self.set_scene(sceneClass, *args, **kw)
    @deprecated
    def GetScene(self):
        return self.get_scene()

    def set_scene(self, sceneClass, *args, **kw):
        """Change to a new Scene"""
        self.next_scene = sceneClass, args, kw
    def get_scene(self):
        """Get the currently active Scene"""
        return self._scene
    scene = property(get_scene, set_scene)

    @deprecated
    def GetTime(self):
        return self.get_time()

    def get_time(self):
        return self._cDirector.GetTicker().now
    time = property(get_time)

    @deprecated
    def GetDelta(self):
        return self.get_delta()
    
    def get_delta(self):
        return self.delta

    @deprecated
    def Quit(self):
        self.quit()
        
    def quit(self):
        """Exit the Director mainloop.

        You only need to call this if you have called Director.Run()
        and want to stop executing it.
        """
        self._running = False

    def _change_scene(self):
        sceneClass, args, kw = self.next_scene
        self.next_scene = None
        if self._scene is not None:
            self._scene.exit()
        self._scene = sceneClass()
        self._cDirector.SetScene(self.scene._cObj)
        self._scene.enter(*args, **kw)
        
        
Director = Director()
