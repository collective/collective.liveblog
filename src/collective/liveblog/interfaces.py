# -*- coding: utf-8 -*-
from plone.directives import form
from zope.interface import Interface


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


class ILiveblog(form.Schema):

    """A liveblog is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.
    """
