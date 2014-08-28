# -*- coding: utf-8 -*-
from collective.liveblog.config import PROJECTNAME
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest

CSS = (
    '++resource++collective.liveblog/styles.css',
)

ADD_PERMISSIONS = (
    dict(
        title='collective.liveblog: Add Liveblog',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
    dict(
        title='collective.liveblog: Add MicroUpdate',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
)


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'collective.liveblog:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']


class InstallTestCase(BaseTestCase):

    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_add_permissions(self):
        for permission in ADD_PERMISSIONS:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'1000',)
        )


class TestUpgrade(BaseTestCase):

    """Ensure product upgrades work."""

    def test_to1010_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('1010',))
                and (step[0]['source'] == ('1000',))]
        self.assertEqual(len(step), 1)


class UninstallTestCase(BaseTestCase):

    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertNotIn(id, resource_ids, '{0} not removed'.format(id))
