# -*- coding: utf-8 -*-
from collective.liveblog.config import PROJECTNAME
from collective.liveblog.testing import INTEGRATION_TESTING
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest


class UpgradesTestCase(unittest.TestCase):

    """Ensure product upgrades work."""

    layer = INTEGRATION_TESTING
    profile = PROJECTNAME + ':default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']

    def test_latest_version(self):
        self.assertEqual(
            self.setup.getLastVersionForProfile(self.profile)[0], u'1000')

    def _match(self, item, source, dest):
        return item['source'] == tuple(source) and item['dest'] == tuple(dest)

    def test_to1010_available(self):
        steps = listUpgradeSteps(self.setup, self.profile, '1000')
        steps = [s for s in steps if self._match(s[0], '1000', '1010')]
        self.assertEqual(len(steps), 1)
