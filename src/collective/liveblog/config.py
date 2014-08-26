# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'collective.liveblog'


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'collective.liveblog:uninstall',
            u'collective.liveblog.upgrades.v1010:default'
        ]
