# -*- coding: utf-8 -*-
from collective.liveblog.config import PROJECTNAME
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from collective.liveblog.testing import IS_PLONE_5
from plone.browserlayer.utils import registered_layers

import unittest

CSS = '++resource++collective.liveblog/styles.css'

ADD_PERMISSIONS = (
    dict(
        title='collective.liveblog: Add Liveblog',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
    dict(
        title='collective.liveblog: Add MicroUpdate',
        expected=['Editor', 'Manager', 'Owner', 'Site Administrator'],
    ),
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    def test_add_permissions(self):
        for permission in ADD_PERMISSIONS:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)
