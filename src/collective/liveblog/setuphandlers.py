# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements


class HiddenProfiles(object):

    implements(INonInstallable)

    def getNonInstallableProfiles(self):  # pragma: no cover
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.liveblog:uninstall',
        ]
