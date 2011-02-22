
import cOpioid2D as _c

from cOpioid2D import \
    LinearForce, \
    BounceBox as _cBounceBox, \
    LifeZone, \
    KillZone

def BounceBox(x,y,width=None,height=None,xx=None,yy=None,userect=False,xmul=1.0,ymul=1.0):
    if xx is None:
        xx = x+width
    if yy is None:
        yy = y+height
    bb = _cBounceBox(x,y,xx,yy,userect)
    bb.SetMultipliers(xmul, ymul);
    return bb;

class _AreaMutator(object):
    def __init__(self, cClass):
        self._class = cClass
        
    def __call__(self, x, y, width=None, height=None, xx=None, yy=None, radius=None, direction=None, arc=None):
        if arc is not None:
            area = _c.ArcArea(x,y,radius,direction,arc)
        elif radius is not None:
            area = _c.CircleArea(x,y,radius)
        else:
            if xx is None:
                xx = x+width
            if yy is None:
                yy = y+height
            area = _c.RectArea(x,y,xx,yy);
        area.thisown = 0
        return self._class(area)
    
KillZone = _AreaMutator(KillZone)
LifeZone = _AreaMutator(LifeZone)