# -*- coding: utf-8 -*-
"""Adapt a Liveblog with a container of micro-updates.

This is based on code from Products.Poi; for more information see:
https://github.com/collective/Products.Poi/blob/master/Products/Poi/adapters.py
"""
from collective.liveblog.interfaces import ILiveblog
from datetime import datetime
from persistent import Persistent
from persistent.list import PersistentList
from plone import api
from time import time
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.container.contained import ObjectAddedEvent
from zope.container.contained import ObjectRemovedEvent
from zope.event import notify
from zope.interface import Attribute
from zope.interface import implements
from zope.interface import Interface


class IMicroUpdateContainer(Interface):
    pass


class IMicroUpdate(Interface):

    """A micro-update on a Liveblog."""

    creator = Attribute('Id of user creating the micro-update.')
    created = Attribute('Date and time when this micro-update was created.')
    modified = Attribute('Date and time when this micro-update was modified.')
    timestamp = Attribute('Timestamp of the micro-update.')
    title = Attribute('Title of the micro-update.')
    text = Attribute('Text of the micro-update.')


class MicroUpdateContainer(Persistent):

    implements(IMicroUpdateContainer)
    adapts(ILiveblog)
    ANNO_KEY = 'liveblog.microupdates'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self.__mapping = annotations.get(self.ANNO_KEY, None)
        if self.__mapping is None:
            self.__mapping = PersistentList()
            annotations[self.ANNO_KEY] = self.__mapping

    def __contains__(self, key):
        return key in self.__mapping

    def __getitem__(self, i):
        i = int(i)
        return self.__mapping.__getitem__(i)

    def __delitem__(self, item):
        self.__mapping.__delitem__(item)

    def __len__(self):
        return self.__mapping.__len__()

    def __setitem__(self, i, y):
        self.__mapping.__setitem__(i, y)

    def append(self, item):
        self.__mapping.append(item)

    def remove(self, id):
        id = int(id)
        self[id] = None

    def add(self, item):
        self.append(item)
        id = str(len(self))
        event = ObjectAddedEvent(item, newParent=self.context, newName=id)
        notify(event)

    def delete(self, id):
        event = ObjectRemovedEvent(self[id], oldParent=self.context, oldName=id)
        self.remove(id)
        notify(event)


class MicroUpdate(Persistent):

    """A micro-update on a Liveblog."""

    implements(IMicroUpdate)

    def __init__(self, title, text):
        self.__parent__ = self.__name__ = None
        self.creator = api.user.get_current().id
        self.modified = self.created = datetime.now()
        self.timestamp = str(time())
        self.title = title
        self.text = text
