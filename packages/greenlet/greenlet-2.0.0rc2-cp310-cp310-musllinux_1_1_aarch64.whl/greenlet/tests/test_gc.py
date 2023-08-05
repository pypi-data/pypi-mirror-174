import gc

import weakref

import greenlet


from . import TestCase
from .leakcheck import fails_leakcheck
# These only work with greenlet gc support
# which is no longer optional.
assert greenlet.GREENLET_USE_GC

class GCTests(TestCase):
    def test_dead_circular_ref(self):
        o = weakref.ref(greenlet.greenlet(greenlet.getcurrent).switch())
        gc.collect()
        if o() is not None:
            import sys
            print("O IS NOT NONE.", sys.getrefcount(o()))
        self.assertIsNone(o())
        self.assertFalse(gc.garbage, gc.garbage)

    def test_circular_greenlet(self):
        class circular_greenlet(greenlet.greenlet):
            pass
        o = circular_greenlet()
        o.self = o
        o = weakref.ref(o)
        gc.collect()
        self.assertIsNone(o())
        self.assertFalse(gc.garbage, gc.garbage)

    def test_inactive_ref(self):
        class inactive_greenlet(greenlet.greenlet):
            def __init__(self):
                greenlet.greenlet.__init__(self, run=self.run)

            def run(self):
                pass
        o = inactive_greenlet()
        o = weakref.ref(o)
        gc.collect()
        self.assertIsNone(o())
        self.assertFalse(gc.garbage, gc.garbage)

    @fails_leakcheck
    def test_finalizer_crash(self):
        # This test is designed to crash when active greenlets
        # are made garbage collectable, until the underlying
        # problem is resolved. How does it work:
        # - order of object creation is important
        # - array is created first, so it is moved to unreachable first
        # - we create a cycle between a greenlet and this array
        # - we create an object that participates in gc, is only
        #   referenced by a greenlet, and would corrupt gc lists
        #   on destruction, the easiest is to use an object with
        #   a finalizer
        # - because array is the first object in unreachable it is
        #   cleared first, which causes all references to greenlet
        #   to disappear and causes greenlet to be destroyed, but since
        #   it is still live it causes a switch during gc, which causes
        #   an object with finalizer to be destroyed, which causes stack
        #   corruption and then a crash

        class object_with_finalizer(object):
            def __del__(self):
                pass
        array = []
        parent = greenlet.getcurrent()
        def greenlet_body():
            greenlet.getcurrent().object = object_with_finalizer()
            try:
                parent.switch()
            except greenlet.GreenletExit:
                print("Got greenlet exit!")
            finally:
                del greenlet.getcurrent().object
        g = greenlet.greenlet(greenlet_body)
        g.array = array
        array.append(g)
        g.switch()
        del array
        del g
        greenlet.getcurrent()
        gc.collect()
