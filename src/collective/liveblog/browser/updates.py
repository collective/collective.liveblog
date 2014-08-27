# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone.memoize import ram
from time import time

grok.templatedir('templates')


class Updates(grok.View):

    """Helper view for Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')

    def _updates_since_timestamp(self):
        """Return the list of micro-updates since the specified timestamp."""
        timestamp = self.request.get('timestamp', None)

        # timestamp should a string representing a float
        try:
            float(timestamp)
        except (TypeError, ValueError):
            return []

        updates = self.context.restrictedTraverse('view').updates()
        updates = [u for u in updates if u['timestamp'] > timestamp]
        return updates

    @ram.cache(lambda *args: time() // 20)
    def updates_since_timestamp(self):
        """Return the list of micro-updates since the specified timestamp;
        the list is cached for 20 seconds.
        """
        return self._updates_since_timestamp()
