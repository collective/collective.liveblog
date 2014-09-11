# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import ILiveblog
from plone.app.caching.purge import ContentPurgePaths
from z3c.caching.interfaces import IPurgePaths
from zope.component import adapts
from zope.interface import implements


class LiveBlogPurgePaths(ContentPurgePaths):

    """Paths to purge for LiveBlog."""

    implements(IPurgePaths)
    adapts(ILiveblog)

    def getRelativePaths(self):
        paths = super(LiveBlogPurgePaths, self).getRelativePaths()
        # Also adds recent-updates view to the list of urls to be purged
        url = self.context.absolute_url()
        paths.append('{0}/recent-updates'.format(url))
        return paths
