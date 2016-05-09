# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase


class Header(ViewletBase):

    """A viewlet to include a header in the Liveblog."""

    def available(self):
        """Check if the viewlet must be displayed; that is, if an image
        is been used and the context is not a micro-update.
        """
        is_microupdate = self.request['PARENTS'][0].__name__ == 'microupdate'
        return self.context.image is not None and not is_microupdate
