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


def _render_updates_cachekey(method, self):
    return len(self._updates())


class View(grok.View):

    """Default view for Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')

    @property
    def can_add_microupdate(self):
        """Return True if the user has permission to add a micro-update."""
        mt = api.portal.get_tool('portal_membership')
        return mt.checkPermission(
            'collective.liveblog.AddMicroUpdate', self.context)

    def _updates(self):
        """Return the list of micro-updates in the Liveblog in reverse order."""
        container = IMicroUpdateContainer(self.context)
        updates = []
        for id, update in enumerate(container):
            if update is None:
                continue  # update has been removed
            updates.append(dict(
                id=id + 1,
                creator=update.creator,
                timestamp=_timestamp(update.created),
                created=api.portal.get_localized_time(update.created, True),
                time_only=api.portal.get_localized_time(update.created, time_only=True),
                title=update.title,
                text=update.text,
            ))
        updates.reverse()  # show micro-updates in reverse order
        return updates

    @ram.cache(_render_updates_cachekey)
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
