# -*- coding: utf-8 -*-
from App.Common import rfc1123_date
from collective.liveblog.browser.base import BaseView
from collective.liveblog.config import PROJECTNAME
from datetime import datetime
from time import time
from zope.publisher.browser import BrowserView

import logging

logger = logging.getLogger(PROJECTNAME)


class RecentUpdates(BrowserView, BaseView):

    """Helper view for Liveblog."""

    def _needs_hard_refresh(self):
        """Return True if a hard refresh of the page is needed.

        Typically, we will request a hard refresh if a micro-update has
        been edited of deleted in the last minute.
        We set an HTTP status code 205 (Reset Content) to handle it on
        the view and update pages using JavaScript.
        """
        if self.context._last_microupdate_edition > str(time() - 60):
            logger.debug(
                u'A micro-update was deleted withing the last minute. '
                u'Setting status code 205.'
            )
            self.request.RESPONSE.setStatus(205)
            return True

        if self.context._last_microupdate_deletion > str(time() - 60):
            logger.debug(
                u'A micro-update was edited withing the last minute. '
                u'Setting status code 205.'
            )
            self.request.RESPONSE.setStatus(205)
            return True

    def _not_modified(self):
        """Return True and set a status code of 304 (Not Modified) if the
        requested variant has not been modified since the time specified.
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
                logger.debug(u'If-Modified-Since header was not valid.')
            if mod_since is not None:
                logger.debug(u'Requesting page if modified since ' + mod_since)
                # convert to UTC and normalize for comparison
                modified = self.context.modified().utcdatetime()
                modified = modified.strftime('%Y-%m-%d %H:%M:%S')
                logger.debug(u'Last modification occurred on ' + modified)
                if modified <= mod_since:
                    logger.debug(u'Setting status code 304.')
                    self.request.RESPONSE.setStatus(304)  # not modified
                    return True
        logger.debug(u'No If-Modified-Since header on the request.')

    def __call__(self):
        logger.debug(
            u'Processing request from ' + self.request.environ['REMOTE_ADDR'])

        if self._needs_hard_refresh():
            return ''

        if self._not_modified():
            return ''

        # the Expires header will help us control how often clients
        # will ask for a page; this supercedes the value defined on our
        # JavaScript code so, if we put here a value above 1 minute,
        # clients will wait that time before requesting the page again
        expires = rfc1123_date(time() + 59)  # page expires in 59 seconds
        last_modified = rfc1123_date(self.context.modified())
        self.request.RESPONSE.setHeader('Cache-Control', 'public')
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Last-Modified', last_modified)
        return self.index()

    # FIXME: caching this function will speed up the rendering of this
    #        view by at least an order of magnitude, but it will also
    #        create an issue: on the update view, the latest updates
    #        will lose the Delete action as a consequence of the
    #        removal of duplicated micro-updates and the mixing of
    #        anonymous and logged in users
    # @ram.cache(lambda *args: time() // 60)  # cache for one minute
    def get_latest_microupdates(self):
        """Return micro-updates posted in the last minute."""
        updates = self.context.get_microupdates()
        updates = [u for u in updates if u['timestamp'] > str(time() - 60)]
        return updates
