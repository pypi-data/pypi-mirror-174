# -*- coding: utf-8 -*-
"""
Tests for greenlet.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from gc import collect
from gc import get_objects
from threading import active_count as active_thread_count
from time import sleep
from time import time

from greenlet import greenlet as RawGreenlet
from greenlet import getcurrent

from greenlet._greenlet import get_pending_cleanup_count
from greenlet._greenlet import get_total_main_greenlets

from . import leakcheck


class TestCaseMetaClass(type):
    # wrap each test method with
    # a) leak checks
    def __new__(cls, classname, bases, classDict):
        # pylint and pep8 fight over what this should be called (mcs or cls).
        # pylint gets it right, but we can't scope disable pep8, so we go with
        # its convention.
        # pylint: disable=bad-mcs-classmethod-argument
        check_totalrefcount = True

        # Python 3: must copy, we mutate the classDict. Interestingly enough,
        # it doesn't actually error out, but under 3.6 we wind up wrapping
        # and re-wrapping the same items over and over and over.
        for key, value in list(classDict.items()):
            if key.startswith('test') and callable(value):
                classDict.pop(key)
                if check_totalrefcount:
                    value = leakcheck.wrap_refcount(value)
                classDict[key] = value
        return type.__new__(cls, classname, bases, classDict)

class TestCase(TestCaseMetaClass(
        "NewBase",
        (unittest.TestCase,),
        {})):

    cleanup_attempt_sleep_duration = 0.001
    cleanup_max_sleep_seconds = 1

    def wait_for_pending_cleanups(self,
                                  initial_active_threads=None,
                                  initial_main_greenlets=None):
        initial_active_threads = initial_active_threads or self.threads_before_test
        initial_main_greenlets = initial_main_greenlets or self.main_greenlets_before_test
        sleep_time = self.cleanup_attempt_sleep_duration
        # NOTE: This is racy! A Python-level thread object may be dead
        # and gone, but the C thread may not yet have fired its
        # destructors and added to the queue. There's no particular
        # way to know that's about to happen. We try to watch the
        # Python threads to make sure they, at least, have gone away.
        # Counting the main greenlets, which we can easily do deterministically,
        # also helps.

        # Always sleep at least once to let other threads run
        sleep(sleep_time)
        quit_after = time() + self.cleanup_max_sleep_seconds
        # TODO: We could add an API that calls us back when a particular main greenlet is deleted?
        # It would have to drop the GIL
        while (
                get_pending_cleanup_count()
                or active_thread_count() > initial_active_threads
                or (not self.expect_greenlet_leak
                    and get_total_main_greenlets() > initial_main_greenlets)):
            sleep(sleep_time)
            if time() > quit_after:
                print("Time limit exceeded.")
                print("Threads: Waiting for only", initial_active_threads,
                      "-->", active_thread_count())
                print("MGlets : Waiting for only", initial_main_greenlets,
                      "-->", get_total_main_greenlets())
                break
        collect()

    def count_objects(self, kind=list, exact_kind=True):
        # pylint:disable=unidiomatic-typecheck
        # Collect the garbage.
        for _ in range(3):
            collect()
        if exact_kind:
            return sum(
                1
                for x in get_objects()
                if type(x) is kind
            )
        # instances
        return sum(
            1
            for x in get_objects()
            if isinstance(x, kind)
        )

    greenlets_before_test = 0
    threads_before_test = 0
    main_greenlets_before_test = 0
    expect_greenlet_leak = False

    def count_greenlets(self):
        """
        Find all the greenlets and subclasses tracked by the GC.
        """
        return self.count_objects(RawGreenlet, False)

    def setUp(self):
        # Ensure the main greenlet exists, otherwise the first test
        # gets a false positive leak
        super(TestCase, self).setUp()
        getcurrent()
        self.threads_before_test = active_thread_count()
        self.main_greenlets_before_test = get_total_main_greenlets()
        self.wait_for_pending_cleanups(self.threads_before_test, self.main_greenlets_before_test)
        self.greenlets_before_test = self.count_greenlets()

    def tearDown(self):
        if getattr(self, 'skipTearDown', False):
            return

        self.wait_for_pending_cleanups(self.threads_before_test, self.main_greenlets_before_test)
        super(TestCase, self).tearDown()
