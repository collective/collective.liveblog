# -*- coding: utf-8 -*-
from collective.liveblog.testing import INTEGRATION_TESTING
from collective.liveblog.testing import IS_PLONE_5
from plone import api

import unittest


class UpgradeBaseTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    profile_id = u'collective.liveblog:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)


class To1001TestCase(UpgradeBaseTestCase):

    from_ = '1000'
    to_ = '1001'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)


class To1002TestCase(UpgradeBaseTestCase):

    from_ = '1001'
    to_ = '1002'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    def test_remove_workflow(self):
        title = u'Migrate liveblog workflow'
        step = self._get_upgrade_step_by_title(title)
        assert step is not None

        # simulate (partially) state on previous version
        wtool = api.portal.get_tool('portal_workflow')
        wtool.setChainForPortalTypes(('Liveblog',), ('liveblog_workflow',))
        assert wtool.getChainForPortalType('Liveblog') == ('liveblog_workflow',)

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)

        self.assertEqual(
            wtool.getChainForPortalType('Liveblog'),
            ('simple_publication_workflow',)
        )

    @unittest.skipIf(IS_PLONE_5, 'Not needed in Plone 5')
    def test_make_liveblog_linkable(self):
        title = u'Make Liveblog linkable on TinyMCE'
        step = self._get_upgrade_step_by_title(title)
        assert step is not None

        # simulate state on previous version
        tinymce = api.portal.get_tool('portal_tinymce')
        linkable = tinymce.linkable.split('\n')
        linkable.remove('Liveblog')
        tinymce.linkable = '\n'.join(linkable)
        assert 'Liveblog' not in tinymce.linkable.split('\n')

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)

        self.assertIn('Liveblog', tinymce.linkable.split('\n'))
