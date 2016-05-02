# -*- coding: utf-8 -*-
from collective.liveblog.browser.base import BaseView
from plone import api
from plone.memoize import ram
from time import time
from zope.publisher.browser import BrowserView


def _updates_cachekey(method, self):
    return (self.context.absolute_url_path(), int(self.context.modified()))


class View(BrowserView, BaseView):

    """Default view for Liveblog."""

    @ram.cache(_updates_cachekey)
    def updates(self):
        """Return the list of micro-updates in the Liveblog in reverse order;
        the list is cached until a new update is published.
        """
        return self.context.get_microupdates()

    @property
    def has_updates(self):
        """Return True if Liveblog has updates."""
        return len(self.updates()) > 0

    @property
    def automatic_updates_enabled(self):
        """Check if the Livelog must be updated automatically.
        Automatic updates should be enabled in active state only.
        """
        return api.content.get_state(self.context) == 'active'

    @property
    def now(self):
        """Return a timestamp for the current date and time."""
        return str(time())
