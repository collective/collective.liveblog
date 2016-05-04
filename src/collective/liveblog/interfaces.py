# -*- coding: utf-8 -*-
from collective.liveblog import _
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from zope.interface import Interface


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


class ILiveblog(Interface):

    """A liveblog is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.
    """

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(u'This image will be used as a header on the Liveblog.'),
        required=False,
    )

    text = RichText(
        title=_(u'Body text'),
        required=False,
    )
