# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from datetime import datetime
from plone import api
from time import sleep
from zope.interface import alsoProvides

import unittest


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _create_updates(self):
        """Create 20 micro-updates. Note the use of the sleep method to avoid
        doing this so fast that we ended with the same timestamp on different
        updates."""
        adapter = IMicroUpdateContainer(self.liveblog)
        for i in range(1, 11):
            sleep(0.01)
            adapter.add(MicroUpdate(str(i), str(i)))

        self.timestamp = datetime.now()

        for i in range(11, 21):
            sleep(0.01)
            adapter.add(MicroUpdate(str(i), str(i)))

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')


class DefaultViewTestCase(ViewTestCase):

    def setUp(self):
        super(DefaultViewTestCase, self).setUp()
        self.view = api.content.get_view('view', self.liveblog, self.request)

    def test_can_add_microupdate(self):
        with api.env.adopt_roles(['Manager']):
            self.assertTrue(self.view.can_add_microupdate)
        with api.env.adopt_roles(['Reader']):
            self.assertFalse(self.view.can_add_microupdate)
        with api.env.adopt_roles(['Reviewer']):
            self.assertFalse(self.view.can_add_microupdate)

    def test_updates(self):
        self.assertEqual(len(self.view._updates()), 0)
        self._create_updates()
        self.assertEqual(len(self.view._updates()), 20)

    def test_has_updates(self):
        self.assertFalse(self.view.has_updates)
        self._create_updates()
        self.assertTrue(self.view.has_updates)


class UpdatesViewTestCase(ViewTestCase):

    def setUp(self):
        super(UpdatesViewTestCase, self).setUp()
        self.view = api.content.get_view('updates', self.liveblog, self.request)

    def test_updates_since_timestamp(self):
        from collective.liveblog.utils import _timestamp

        timestamp = datetime.now()
        self._create_updates()

        # before all elements were created
        self.request['timestamp'] = _timestamp(timestamp)
        self.assertEqual(len(self.view._updates_since_timestamp()), 20)
        # middle of the creation
        self.request['timestamp'] = _timestamp(self.timestamp)
        self.assertEqual(len(self.view._updates_since_timestamp()), 10)
        # after all elements were created
        self.request['timestamp'] = _timestamp(datetime.now())
        self.assertEqual(len(self.view._updates_since_timestamp()), 0)

        self.request['timestamp'] = _timestamp(self.timestamp)
        updates = self.view._updates_since_timestamp()
        updates = [u['title'] for u in updates]
        self.assertIn('20', updates)
        self.assertIn('11', updates)
        self.assertNotIn('10', updates)
        self.assertNotIn('1', updates)
