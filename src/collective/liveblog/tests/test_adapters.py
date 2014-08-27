# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.testing import INTEGRATION_TESTING
from datetime import datetime
from plone import api

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

    def test_adding(self):
        adapter = IMicroUpdateContainer(self.liveblog)
        adapter.add(MicroUpdate(u'One', u'First micro-update.'))
        adapter.add(MicroUpdate(u'Two', u'Second micro-update.'))
        adapter.add(MicroUpdate(u'Three', u'Third micro-update.'))
        self.assertEqual(len(adapter), 3)

        # check the first micro-update
        self.assertEqual(adapter[0].creator, 'test_user_1_')
        self.assertTrue(isinstance(adapter[0].created, datetime))
        self.assertTrue(isinstance(adapter[0].modified, datetime))
        self.assertEqual(adapter[0].created, adapter[0].modified)
        self.assertEqual(adapter[0].title, u'One')
        self.assertEqual(adapter[0].text, u'First micro-update.')

        # dates are sequential
        self.assertTrue(adapter[0].created < adapter[1].created)
        self.assertTrue(adapter[1].created < adapter[2].created)

        # check the other micro-updates
        self.assertEqual(adapter[1].title, u'Two')
        self.assertEqual(adapter[2].title, u'Three')
        self.assertEqual(adapter[1].text, u'Second micro-update.')
        self.assertEqual(adapter[2].text, u'Third micro-update.')
