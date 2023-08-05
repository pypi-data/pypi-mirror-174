# Copyright (c) 2018 gevent community
# Copyright (c) 2021 greenlet community
#
# This was originally part of gevent's test suite. The main author
# (Jason Madden) vendored a copy of it into greenlet.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import print_function

import os
import sys
import gc

from functools import wraps
import unittest


import objgraph

# graphviz 0.18 (Nov 7 2021), available only on Python 3.6 and newer,
# has added type hints (sigh). It wants to use ``typing.Literal`` for
# some stuff, but that's only available on Python 3.9+. If that's not
# found, it creates a ``unittest.mock.MagicMock`` object and annotates
# with that. These are GC'able objects, and doing almost *anything*
# with them results in an explosion of objects. For example, trying to
# compare them for equality creates new objects. This causes our
# leakchecks to fail, with reports like:
#
# greenlet.tests.leakcheck.LeakCheckError: refcount increased by [337, 1333, 343, 430, 530, 643, 769]
# _Call          1820      +546
# dict           4094       +76
# MagicProxy      585       +73
# tuple          2693       +66
# _CallList        24        +3
# weakref        1441        +1
# function       5996        +1
# type            736        +1
# cell            592        +1
# MagicMock         8        +1
#
# To avoid this, we *could* filter this type of object out early. In
# principle it could leak, but we don't use mocks in greenlet, so it
# doesn't leak from us. However, a further issue is that ``MagicMock``
# objects have subobjects that are also GC'able, like ``_Call``, and
# those create new mocks of their own too. So we'd have to filter them
# as well, and they're not public. That's OK, we can workaround the
# problem by being very careful to never compare by equality or other
# user-defined operators, only using object identity or other builtin
# functions.

RUNNING_ON_GITHUB_ACTIONS = os.environ.get('GITHUB_ACTIONS')
RUNNING_ON_TRAVIS = os.environ.get('TRAVIS') or RUNNING_ON_GITHUB_ACTIONS
RUNNING_ON_APPVEYOR = os.environ.get('APPVEYOR')
RUNNING_ON_CI = RUNNING_ON_TRAVIS or RUNNING_ON_APPVEYOR
RUNNING_ON_MANYLINUX = os.environ.get('GREENLET_MANYLINUX')
SKIP_LEAKCHECKS = RUNNING_ON_MANYLINUX or os.environ.get('GREENLET_SKIP_LEAKCHECKS')
SKIP_FAILING_LEAKCHECKS = os.environ.get('GREENLET_SKIP_FAILING_LEAKCHECKS')
ONLY_FAILING_LEAKCHECKS = os.environ.get('GREENLET_ONLY_FAILING_LEAKCHECKS')

def ignores_leakcheck(func):
    """
    Ignore the given object during leakchecks.

    Can be applied to a method, in which case the method will run, but
    will not be subject to leak checks.

    If applied to a class, the entire class will be skipped during leakchecks. This
    is intended to be used for classes that are very slow and cause problems such as
    test timeouts; typically it will be used for classes that are subclasses of a base
    class and specify variants of behaviour (such as pool sizes).
    """
    func.ignore_leakcheck = True
    return func

def fails_leakcheck(func):
    """
    Mark that the function is known to leak.
    """
    func.fails_leakcheck = True
    if SKIP_FAILING_LEAKCHECKS:
        func = unittest.skip("Skipping known failures")(func)
    return func

class LeakCheckError(AssertionError):
    pass

if hasattr(sys, 'getobjects'):
    # In a Python build with ``--with-trace-refs``, make objgraph
    # trace *all* the objects, not just those that are tracked by the
    # GC
    class _MockGC(object):
        def get_objects(self):
            return sys.getobjects(0) # pylint:disable=no-member
        def __getattr__(self, name):
            return getattr(gc, name)
    objgraph.gc = _MockGC()
    fails_strict_leakcheck = fails_leakcheck
else:
    def fails_strict_leakcheck(func):
        """
        Decorator for a function that is known to fail when running
        strict (``sys.getobjects()``) leakchecks.

        This type of leakcheck finds all objects, even those, such as
        strings, which are not tracked by the garbage collector.
        """
        return func

class ignores_types_in_strict_leakcheck(object):
    def __init__(self, types):
        self.types = types
    def __call__(self, func):
        func.leakcheck_ignore_types = self.types
        return func

class _RefCountChecker(object):

    # Some builtin things that we ignore
    # XXX: Those things were ignored by gevent, but they're important here,
    # presumably.
    IGNORED_TYPES = () #(tuple, dict, types.FrameType, types.TracebackType)

    def __init__(self, testcase, function):
        self.testcase = testcase
        self.function = function
        self.deltas = []
        self.peak_stats = {}
        self.ignored_types = ()

        # The very first time we are called, we have already been
        # self.setUp() by the test runner, so we don't need to do it again.
        self.needs_setUp = False

    def _include_object_p(self, obj):
        # pylint:disable=too-many-return-statements
        #
        # See the comment block at the top. We must be careful to
        # avoid invoking user-defined operations.
        if obj is self:
            return False
        kind = type(obj)
        # ``self._include_object_p == obj`` returns NotImplemented
        # for non-function objects, which causes the interpreter
        # to try to reverse the order of arguments...which leads
        # to the explosion of mock objects. We don't want that, so we implement
        # the check manually.
        if kind == type(self._include_object_p):
            try:
                # pylint:disable=not-callable
                exact_method_equals = self._include_object_p.__eq__(obj)
            except AttributeError:
                # Python 2.7 methods may only have __cmp__, and that raises a
                # TypeError for non-method arguments
                # pylint:disable=no-member
                exact_method_equals = self._include_object_p.__cmp__(obj) == 0

            if exact_method_equals is not NotImplemented and exact_method_equals:
                return False

        # Similarly, we need to check identity in our __dict__ to avoid mock explosions.
        for x in self.__dict__.values():
            if obj is x:
                return False


        if kind in self.ignored_types or kind in self.IGNORED_TYPES:
            return False

        return True

    def _growth(self):
        return objgraph.growth(limit=None, peak_stats=self.peak_stats,
                               filter=self._include_object_p)

    def _report_diff(self, growth):
        if not growth:
            return "<Unable to calculate growth>"

        lines = []
        width = max(len(name) for name, _, _ in growth)
        for name, count, delta in growth:
            lines.append('%-*s%9d %+9d' % (width, name, count, delta))

        diff = '\n'.join(lines)
        return diff


    def _run_test(self, args, kwargs):
        gc_enabled = gc.isenabled()
        gc.disable()

        if self.needs_setUp:
            self.testcase.setUp()
            self.testcase.skipTearDown = False
        try:
            self.function(self.testcase, *args, **kwargs)
        finally:
            self.testcase.tearDown()
            self.testcase.doCleanups()
            self.testcase.skipTearDown = True
            self.needs_setUp = True
            if gc_enabled:
                gc.enable()

    def _growth_after(self):
        # Grab post snapshot
        if 'urlparse' in sys.modules:
            sys.modules['urlparse'].clear_cache()
        if 'urllib.parse' in sys.modules:
            sys.modules['urllib.parse'].clear_cache()

        return self._growth()

    def _check_deltas(self, growth):
        # Return false when we have decided there is no leak,
        # true if we should keep looping, raises an assertion
        # if we have decided there is a leak.

        deltas = self.deltas
        if not deltas:
            # We haven't run yet, no data, keep looping
            return True

        if gc.garbage:
            raise LeakCheckError("Generated uncollectable garbage %r" % (gc.garbage,))


        # the following configurations are classified as "no leak"
        # [0, 0]
        # [x, 0, 0]
        # [... a, b, c, d]  where a+b+c+d = 0
        #
        # the following configurations are classified as "leak"
        # [... z, z, z]  where z > 0

        if deltas[-2:] == [0, 0] and len(deltas) in (2, 3):
            return False

        if deltas[-3:] == [0, 0, 0]:
            return False

        if len(deltas) >= 4 and sum(deltas[-4:]) == 0:
            return False

        if len(deltas) >= 3 and deltas[-1] > 0 and deltas[-1] == deltas[-2] and deltas[-2] == deltas[-3]:
            diff = self._report_diff(growth)
            raise LeakCheckError('refcount increased by %r\n%s' % (deltas, diff))

        # OK, we don't know for sure yet. Let's search for more
        if sum(deltas[-3:]) <= 0 or sum(deltas[-4:]) <= 0 or deltas[-4:].count(0) >= 2:
            # this is suspicious, so give a few more runs
            limit = 11
        else:
            limit = 7
        if len(deltas) >= limit:
            raise LeakCheckError('refcount increased by %r\n%s'
                                 % (deltas,
                                    self._report_diff(growth)))

        # We couldn't decide yet, keep going
        return True

    def __call__(self, args, kwargs):
        for _ in range(3):
            gc.collect()

        expect_failure = getattr(self.function, 'fails_leakcheck', False)
        if expect_failure:
            self.testcase.expect_greenlet_leak = True
        self.ignored_types = getattr(self.function, "leakcheck_ignore_types", ())

        # Capture state before; the incremental will be
        # updated by each call to _growth_after
        growth = self._growth()

        try:
            while self._check_deltas(growth):
                self._run_test(args, kwargs)

                growth = self._growth_after()

                self.deltas.append(sum((stat[2] for stat in growth)))
        except LeakCheckError:
            if not expect_failure:
                raise
        else:
            if expect_failure:
                raise LeakCheckError("Expected %s to leak but it did not." % (self.function,))

def wrap_refcount(method):
    if getattr(method, 'ignore_leakcheck', False) or SKIP_LEAKCHECKS:
        return method

    @wraps(method)
    def wrapper(self, *args, **kwargs): # pylint:disable=too-many-branches
        if getattr(self, 'ignore_leakcheck', False):
            raise unittest.SkipTest("This class ignored during leakchecks")
        if ONLY_FAILING_LEAKCHECKS and not getattr(method, 'fails_leakcheck', False):
            raise unittest.SkipTest("Only running tests that fail leakchecks.")
        return _RefCountChecker(self, method)(args, kwargs)

    return wrapper
