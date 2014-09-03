# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from collective.liveblog.utils import _timestamp
from datetime import datetime
from plone import api
from time import sleep
from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _create_updates(self):
        """Create 20 micro-updates. Note the use of the sleep method to avoid
        doing this so fast that we ended with the same timestamp on different
        updates."""
        adapter = IMicroUpdateContainer(self.liveblog)
        for i in range(1, 11):
            sleep(0.05)
            adapter.add(MicroUpdate(str(i), str(i)))

        self.timestamp = datetime.now()

        for i in range(11, 21):
            sleep(0.05)
            adapter.add(MicroUpdate(str(i), str(i)))

        # update Liveblog modification time to invalidate the cache
        notify(ObjectModifiedEvent(self.liveblog))

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

    def test_updates(self):
        self.assertEqual(len(self.view._updates()), 0)
        self._create_updates()
        self.assertEqual(len(self.view._updates()), 20)

    def test_has_updates(self):
        self.assertFalse(self.view.has_updates)
        self._create_updates()
        self.assertTrue(self.view.has_updates)


class UpdateViewTestCase(ViewTestCase):

    def setUp(self):
        super(UpdateViewTestCase, self).setUp()
        self.view = api.content.get_view('update', self.liveblog, self.request)

    def test_view_listed_in_actions(self):
        portal_types = api.portal.get_tool('portal_types')
        actions = portal_types['Liveblog'].listActions()
        actions = [a.id for a in actions]
        self.assertIn('update', actions)


class RecentUpdatesViewTestCase(ViewTestCase):

    def setUp(self):
        super(RecentUpdatesViewTestCase, self).setUp()
        self.view = api.content.get_view(
            'recent-updates', self.liveblog, self.request)

    def test_needs_hard_refresh(self):
        # calling the method without a timestamp will return False
        self.assertFalse(self.view._needs_hard_refresh())
        # a deletion happened before last update; we already handled it
        self.liveblog._last_microupdate_deletion = _timestamp(datetime.now())
        sleep(0.05)
        self.request['timestamp'] = _timestamp(datetime.now())
        self.assertFalse(self.view._needs_hard_refresh())
        sleep(0.05)
        # a deletion happened after last update; we need to handle it
        self.liveblog._last_microupdate_deletion = _timestamp(datetime.now())
        self.assertTrue(self.view._needs_hard_refresh())
        self.assertEqual(self.request.RESPONSE.getStatus(), 205)

    def test_updates_since_timestamp(self):
        timestamp = datetime.now()
        self._create_updates()

        # before all elements were created
        timestamp = _timestamp(timestamp)
        self.assertEqual(len(self.view._updates_since_timestamp(timestamp)), 20)
        # middle of the creation
        timestamp = _timestamp(self.timestamp)
        self.assertEqual(len(self.view._updates_since_timestamp(timestamp)), 10)
        # after all elements were created
        timestamp = _timestamp(datetime.now())
        self.assertEqual(len(self.view._updates_since_timestamp(timestamp)), 0)

        timestamp = _timestamp(self.timestamp)
        updates = self.view._updates_since_timestamp(timestamp)
        updates = [u['title'] for u in updates]
        self.assertIn('20', updates)
        self.assertIn('11', updates)
        self.assertNotIn('10', updates)
        self.assertNotIn('1', updates)
