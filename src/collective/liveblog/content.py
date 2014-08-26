# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone.dexterity.content import Container


class Liveblog(Container):

    """A liveblog is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.
    """

    grok.implements(ILiveblog)
