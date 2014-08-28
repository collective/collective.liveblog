# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContent
from collective.liveblog.interfaces import ILiveblog
from collective.liveblog.interfaces import IBrowserLayer

grok.templatedir('templates')


class Header(grok.Viewlet):

    """A viewlet to include a header in the Liveblog."""

    grok.name('collective.liveblog.header')
    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContent)

    def available(self):
        """Return True if an image has been defined."""
        return self.context.image is not None
