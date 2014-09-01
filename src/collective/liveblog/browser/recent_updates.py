# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone.memoize import ram

grok.templatedir('templates')


def _updates_since_timestamp_cachekey(method, self, timestamp):
    return (
        self.context.absolute_url_path(), int(self.context.modified()), timestamp)


class RecentUpdates(grok.View):

    """Helper view for Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.name('recent-updates')
    grok.require('zope2.View')
    grok.template('recent_updates')

    def _updates_since_timestamp(self, timestamp):
        """Return the list of micro-updates since the specified timestamp."""
        # timestamp should a string representing a float
        try:
            float(timestamp)
        except (TypeError, ValueError):
            return []

        updates = self.context.restrictedTraverse('view').updates()
        updates = [u for u in updates if u['timestamp'] > timestamp]
        return updates

    @ram.cache(_updates_since_timestamp_cachekey)
    def updates_since_timestamp(self, timestamp):
        """Return the list of micro-updates since the specified timestamp;
        the list is cached until a new update is published.
        """
        return self._updates_since_timestamp(timestamp)
