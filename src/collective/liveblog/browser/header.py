# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase


class Header(ViewletBase):

    """A viewlet to include a header in the Liveblog."""

    def available(self):
        """Return True if an image has been defined."""
        return self.context.image is not None
