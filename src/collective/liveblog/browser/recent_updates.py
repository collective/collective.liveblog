# -*- coding: utf-8 -*-
from App.Common import rfc1123_date
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from datetime import datetime
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

    def _if_modified_since_request_handler(self):
        """Return a status code of 304 (not modified) if the requested
        variant has not been modified since the time specified.
        """
        header = self.request.get_header('If-Modified-Since', None)
        if header is not None:
            # do what RFC 2616 tells to do in case of invalid date
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
            header = header.split(';')[0]
            try:
                # parse RFC 1123 format and normalize for comparison
                mod_since = datetime.strptime(header, '%a, %d %b %Y %H:%M:%S %Z')
                mod_since = mod_since.strftime('%Y-%m-%d %H:%M:%S')
            except (TypeError, ValueError):
                mod_since = None
            if mod_since is not None:
                # convert to UTC and normalize for comparison
                modified = self.context.modified().utcdatetime()
                modified = modified.strftime('%Y-%m-%d %H:%M:%S')
                if modified <= mod_since:
                    self.request.RESPONSE.setStatus(304)  # not modified
                    return True

    def update(self):
        last_modified = rfc1123_date(self.context.modified())
        self.request.RESPONSE.setHeader('Cache-Control', 'public')
        self.request.RESPONSE.setHeader('Last-Modified', last_modified)

        if self._if_modified_since_request_handler():
            return ''

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
