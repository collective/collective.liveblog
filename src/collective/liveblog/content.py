# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone.dexterity.content import Container


class Liveblog(Container):

    """A liveblog is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.

    The _last_microupdate_deletion attribute is used to detect if a hard
    refresh of the views is needed.
    """

    grok.implements(ILiveblog)

    _last_microupdate_deletion = '0.0'
