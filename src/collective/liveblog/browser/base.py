# -*- coding: utf-8 -*-
from plone import api
from plone.memoize import view


class BaseView:

    """Base view with helper methods for Liveblog."""

    @property
    @view.memoize
    def is_anonymous(self):
        return api.user.is_anonymous()

    @property
    @view.memoize
    def show_byline(self):
        """Return True if user is allowed to view 'about' information."""
        site_props = api.portal.get_tool('portal_properties').site_properties
        allow_view = site_props.getProperty('allowAnonymousViewAbout', True)
        return not self.is_anonymous or allow_view
