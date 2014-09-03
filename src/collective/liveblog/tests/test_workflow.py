# -*- coding: utf-8 -*-
from collective.liveblog.testing import INTEGRATION_TESTING
from plone import api

import unittest


class LiveblogWorkflowTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = self.portal['portal_workflow']
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

    def test_workflow_installed(self):
        workflow_ids = self.workflow.getWorkflowIds()
        self.assertIn('liveblog_workflow', workflow_ids)

    def test_is_default_workflow_for_liveblog(self):
        chain = self.workflow.getChainForPortalType('Liveblog')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'liveblog_workflow')

    def test_workflow_lifecycle(self):
        with api.env.adopt_roles(['Manager']):
            review_state = api.content.get_state(self.liveblog)
            self.assertEqual(review_state, 'private')

            api.content.transition(self.liveblog, 'activate')
            review_state = api.content.get_state(self.liveblog)
            self.assertEqual(review_state, 'active')

            api.content.transition(self.liveblog, 'inactivate')
            review_state = api.content.get_state(self.liveblog)
            self.assertEqual(review_state, 'inactive')

            api.content.transition(self.liveblog, 'activate')
            review_state = api.content.get_state(self.liveblog)
            self.assertEqual(review_state, 'active')

            api.content.transition(self.liveblog, 'retract')
            review_state = api.content.get_state(self.liveblog)
            self.assertEqual(review_state, 'private')
