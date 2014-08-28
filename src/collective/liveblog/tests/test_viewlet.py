# -*- coding: utf-8 -*-
"""Test case for viewlets on the package.

For more information on how to test viewlets, see:
http://developer.plone.org/views/viewlets.html#finding-viewlets-programmatically
"""
from plone import api
from Products.Five.browser import BrowserView as View
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletTestCase(unittest.TestCase):

    """Tests for viewlets."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)

        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

    def _get_viewlet_manager(self):
        context = self.liveblog
        request = self.request
        view = View(context, request)
        manager = queryMultiAdapter(
            (context, request, view), IViewletManager, 'plone.abovecontent')

        return manager

    def test_viewlet_is_registered(self):
        manager = self._get_viewlet_manager()
        self.assertTrue(manager)
        manager.update()
        self.assertIn(u'collective.liveblog.header', manager)

    def test_viewlet_order(self):
        manager = self._get_viewlet_manager()
        manager.update()
        self.assertEqual(len(manager.viewlets), 2)
        viewlets = [v.__name__ for v in manager.viewlets]
        self.assertListEqual(
            viewlets, [u'plone.path_bar', u'collective.liveblog.header'])

    def test_viewlet_is_available(self):
        manager = self._get_viewlet_manager()
        manager.update()
        viewlet = manager[u'collective.liveblog.header']
        viewlet.update()
        self.assertFalse(viewlet.available())
        from plone.namedfile.file import NamedBlobImage
        self.liveblog.image = NamedBlobImage()
        self.assertTrue(viewlet.available())
