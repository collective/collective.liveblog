# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from collective.liveblog.utils import _timestamp
from datetime import datetime
from five import grok
from plone import api
from plone.memoize import ram

grok.templatedir('templates')


def _updates_cachekey(method, self):
    return (self.context.absolute_url_path(), int(self.context.modified()))


class View(grok.View):

    """Default view for Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')

    def _updates(self):
        """Return the list of micro-updates in the Liveblog in reverse order."""
        container = IMicroUpdateContainer(self.context)
        updates = []
        for id, update in enumerate(container):
            if update is None:
                continue  # update has been removed
            updates.append(dict(
                id=id,
                creator=update.creator,
                timestamp=_timestamp(update.created),  # 1409223490.21,
                datetime=api.portal.get_localized_time(update.created, True),  # 28/08/2014 10h58
                date=api.portal.get_localized_time(update.created),  # 28/08/2014
                time=api.portal.get_localized_time(update.created, time_only=True),  # 10h58
                isoformat=update.created.isoformat()[:-3],  # 2014-08-28T10:58:10.209468
                title=update.title,
                text=update.text,
            ))
        updates.reverse()  # show micro-updates in reverse order
        return updates

    @ram.cache(_updates_cachekey)
    def updates(self):
        """Return the list of micro-updates in the Liveblog in reverse order;
        the list is cached until a new update is published.
        """
        return self._updates()

    @property
    def has_updates(self):
        """Return True if Liveblog has updates."""
        return len(self.updates()) > 0

    @property
    def now(self):
        """Return a timestamp for the current date and time."""
        return _timestamp(datetime.now())
