# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from collective.liveblog.tests.utils import _create_microupdates
from datetime import datetime
from datetime import timedelta
from plone import api
from time import time
from zExceptions import NotFound
from zope.interface import alsoProvides

import unittest


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

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

    def test_has_updates(self):
        self.assertFalse(self.view.has_updates)
        _create_microupdates(self.liveblog, 1)
        self.assertTrue(self.view.has_updates)

    def test_automatic_updates_enabled(self):
        self.assertFalse(self.view.automatic_updates_enabled)
        api.content.transition(self.liveblog, 'activate')
        self.assertTrue(self.view.automatic_updates_enabled)
        api.content.transition(self.liveblog, 'inactivate')
        self.assertFalse(self.view.automatic_updates_enabled)

    def test_date_is_shown_in_microupdates_older_than_today(self):
        # comment inside the JS block that adds the dates
        comment = '/* show dates for micro-updates older than today */'
        self.assertIn(comment, self.view())
        api.content.transition(self.liveblog, 'activate')
        self.assertIn(comment, self.view())
        api.content.transition(self.liveblog, 'inactivate')
        self.assertIn(comment, self.view())


class MicroUpdateViewTestCase(ViewTestCase):

    def test_no_timestamp_raises_bad_request(self):
        self.request.path = []
        view = api.content.get_view('microupdate', self.liveblog, self.request)
        self.assertEqual(view(), '')
        self.assertEqual(self.request.RESPONSE.getStatus(), 400)

    def test_invalid_timestamp_raises_not_found(self):
        self.request.path = ['asdf']
        view = api.content.get_view('microupdate', self.liveblog, self.request)
        with self.assertRaises(NotFound):
            view.publishTraverse(self.request, 'asdf')

    def test_rendered(self):
        _create_microupdates(self.liveblog, 1)
        timestamp = self.liveblog.get_microupdates()[0]['timestamp']
        self.request.path = [timestamp]
        view = api.content.get_view('microupdate', self.liveblog, self.request)
        view.publishTraverse(self.request, timestamp)
        rendered = view()
        self.assertIn('itemtype="http://schema.org/BlogPosting"', rendered)
        self.assertIn('<span property="rnews:author">test_user_1_</span>', rendered)
        self.assertIn('<span property="rnews:datePublished">', rendered)
        self.assertNotIn('<span property="rnews:dateModified">', rendered)
        self.assertIn('data-timestamp="{0}"'.format(timestamp), rendered)


class UpdateViewTestCase(ViewTestCase):

    def setUp(self):
        super(UpdateViewTestCase, self).setUp()
        self.view = api.content.get_view('update', self.liveblog, self.request)

    def test_view_listed_in_actions(self):
        portal_types = api.portal.get_tool('portal_types')
        actions = portal_types['Liveblog'].listActions()
        actions = [a.id for a in actions]
        self.assertIn('update', actions)

    def test_date_is_shown_in_microupdates_older_than_today(self):
        # comment inside the JS block that adds the dates
        comment = '/* show dates for micro-updates older than today */'
        self.assertIn(comment, self.view())
        api.content.transition(self.liveblog, 'activate')
        self.assertIn(comment, self.view())
        api.content.transition(self.liveblog, 'inactivate')
        self.assertIn(comment, self.view())


class RecentUpdatesViewTestCase(ViewTestCase):

    def setUp(self):
        super(RecentUpdatesViewTestCase, self).setUp()
        self.view = api.content.get_view(
            'recent-updates', self.liveblog, self.request)

    def test_needs_hard_refresh_on_edition(self):
        # an edition happened before last update; we already handled it
        self.liveblog._last_microupdate_edition = str(time() - 120)
        self.assertFalse(self.view._needs_hard_refresh())
        # an edition happened after last update; we need to handle it
        self.liveblog._last_microupdate_edition = str(time() - 30)
        self.assertTrue(self.view._needs_hard_refresh())
        self.assertEqual(self.request.RESPONSE.getStatus(), 205)

    def test_needs_hard_refresh_on_deletion(self):
        # a deletion happened before last update; we already handled it
        self.liveblog._last_microupdate_deletion = str(time() - 120)
        self.assertFalse(self.view._needs_hard_refresh())
        # a deletion happened after last update; we need to handle it
        self.liveblog._last_microupdate_deletion = str(time() - 30)
        self.assertTrue(self.view._needs_hard_refresh())
        self.assertEqual(self.request.RESPONSE.getStatus(), 205)

    def test_not_modified(self):
        RFC1123 = '%a, %d %b %Y %H:%M:%S GMT'
        # calling the method without header will return False
        assert not self.request.get_header('If-Modified-Since')
        self.assertFalse(self.view._not_modified())
        # invalid date return False
        self.request.environ['IF_MODIFIED_SINCE'] = 'invalid'
        assert self.request.get_header('If-Modified-Since') == 'invalid'
        self.assertFalse(self.view._not_modified())
        # modified, return False as we must update
        if_modified_since = datetime.utcnow() - timedelta(seconds=60)
        if_modified_since = if_modified_since.strftime(RFC1123)
        self.request.environ['IF_MODIFIED_SINCE'] = if_modified_since
        self.assertFalse(self.view._not_modified())
        # not modified, return True and set header
        if_modified_since = datetime.utcnow() + timedelta(seconds=60)
        if_modified_since = if_modified_since.strftime(RFC1123)
        self.request.environ['IF_MODIFIED_SINCE'] = if_modified_since
        self.assertTrue(self.view._not_modified())
        self.assertEqual(self.request.RESPONSE.getStatus(), 304)

    def test_get_latest_microupdates(self):
        from time import sleep
        _create_microupdates(self.liveblog, 10)
        self.assertEqual(len(self.view.get_latest_microupdates()), 10)
        # after one minutes no micro-updates should be listed
        sleep(60)
        self.assertEqual(len(self.view.get_latest_microupdates()), 0)
        # if we add more micro-updates, they should be listed
        _create_microupdates(self.liveblog, 5)
        self.assertEqual(len(self.view.get_latest_microupdates()), 5)
