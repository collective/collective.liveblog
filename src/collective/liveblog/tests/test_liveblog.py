# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import ILiveblog
from collective.liveblog.testing import INTEGRATION_TESTING
from collective.liveblog.tests.utils import _create_microupdates
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

    def test_adding(self):
        self.assertTrue(ILiveblog.providedBy(self.liveblog))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Liveblog')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Liveblog')
        schema = fti.lookupSchema()
        self.assertEqual(ILiveblog, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Liveblog')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ILiveblog.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
        self.assertTrue(IExcludeFromNavigation.providedBy(self.liveblog))

    def test_content_types_constrains(self):
        allowed_types = [t.getId() for t in self.liveblog.allowedContentTypes()]
        self.assertListEqual(allowed_types, ['Image'])

    def test_get_microupdates(self):
        self.assertEqual(len(self.liveblog.get_microupdates()), 0)
        _create_microupdates(self.liveblog, 10)
        self.assertEqual(len(self.liveblog.get_microupdates()), 10)
