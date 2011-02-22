"""Object manager for tracking SWIG objects"""

__all__ = [
    "ObjectManager",
    ]

import cOpioid2D as _c
import sys, traceback

class ObjectManager(object):
    def __init__(self):
        self.objects = {}
        self.delayed = set()
        self.purgatory = set()

    def register(self, obj):
        #sys.stdout.flush()
        c = obj._cObj
        id = c.GetID()
        c.SetManaged(True)
        #print "registering", id, obj
        self.objects[id] = obj

    def get(self, id):
        return self.objects[id]

    def c2py(self, obj):
        if obj is None:
            return None
        id = obj.GetID()
        return self.objects[id]

    def discard(self, id):
        #print "discarding", id
        try:
            obj = self.objects[id]
            del self.objects[id]
            obj._on_mgr_delete()
            #print "manager discard",repr(obj),"Cptr",int(obj._cObj.this)
            obj = None
        except KeyError:
            #print "%i not found" % id
            #sys.stdout.flush()
            pass
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def delayed_discard(self, id):
        #obj = self.objects[id]
        #print "delayed discard", repr(obj), "Cptr", int(obj._cObj.this)
        self.delayed.add(id)

    def purge(self):
        purgatory = self.purgatory
        self.purgatory = self.delayed
        self.delayed = set()
        for id in purgatory:
            self.discard(id)
            
        
class ObjectManagerCallback(_c.DeleteCallback):
    def OnDelete(self, id):
        #print "OnDelete:", id
        #sys.stdout.flush()
        ObjectManager.delayed_discard(id)

ObjectManager = ObjectManager()
_callback = ObjectManagerCallback()
_c.Identified.SetDeleteCallback(_callback)
