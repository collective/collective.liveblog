# -*- coding: utf-8 -*-
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import FUNCTIONAL_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import directlyProvides

import unittest


class AddMicroUpdateViewTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'test')
        self.liveblog = api.content.create(self.folder, 'Liveblog', 'liveblog')

    def test_add_microupdate_no_parameters(self):
        # invoke the view and check the status message
        self.liveblog.unrestrictedTraverse('add-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'There were some errors. Required input is missing.'
        self.assertEqual(msg[0].message, expected)

    def test_add_microupdate(self):
        self.request.form['title'] = ''
        self.request.form['text'] = 'Extra! Extra! Read All About It!'
        # invoke the view and check the status message
        self.liveblog.unrestrictedTraverse('add-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item published.'
        self.assertEqual(msg[0].message, expected)
