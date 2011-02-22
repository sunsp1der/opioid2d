"""Math utilities
"""

__all__ = [
    "rad2xy",
    "angledir",
    "angledelta",
    ]

import math

def rad2xy(angle, magnitude):
    """Radial to x,y translation"""
    angle = math.pi + math.pi * angle/180.0
    x = -math.sin(angle) * magnitude
    y = math.cos(angle) * magnitude
    return x,y

def angledir(a,b):
    a %= 360.0
    b %= 360.0
    delta = b-a
    result = cmp(delta, 0)
    if abs(delta) > 180:
        return -result
    return result

def angledelta(a,b):
    a %= 360.0
    b %= 360.0
    delta = b-a
    if delta > 180:
        return delta-360
    elif delta < -180:
        return delta+360
    return delta
    
