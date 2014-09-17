# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from time import sleep
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def _create_microupdates(context, count):
    """Create 10 micro-updates. Note the use of the sleep method to avoid
    doing this so fast that we ended with the same timestamp on different
    updates."""
    adapter = IMicroUpdateContainer(context)
    for i in range(1, count + 1):
        sleep(0.05)
        adapter.add(MicroUpdate(str(i), str(i)))

    # wait and update Liveblog modification time to invalidate the cache
    sleep(1)
    notify(ObjectModifiedEvent(context))
