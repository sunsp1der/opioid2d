
__all__ = [
    "Keyboard",
    ]

import pygame

class Keyboard(object):
    """Keyboard singleton
    """
    def is_pressed(self, key):
        """Test wether the given key is currently pressed down"""
        return pygame.key.get_pressed()[key]

Keyboard = Keyboard()
