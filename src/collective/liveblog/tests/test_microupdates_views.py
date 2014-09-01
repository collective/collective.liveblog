# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import FUNCTIONAL_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides

import unittest


class AddMicroUpdateViewTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

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


class DeleteMicroUpdateViewTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')
        adapter = IMicroUpdateContainer(self.liveblog)
        adapter.add(MicroUpdate(u'', u'Delete me!'))

    def test_delete_microupdate(self):
        # invoke the view and check the status message
        self.request.form['id'] = '0'
        self.liveblog.unrestrictedTraverse('delete-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item deleted.'
        self.assertEqual(msg[0].message, expected)

    def test_delete_microupdate_no_id(self):
        # invoke the view and check the status message
        self.liveblog.unrestrictedTraverse('delete-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'There were some errors. Required input is missing.'
        self.assertEqual(msg[0].message, expected)

    def test_delete_microupdate_invalid_id(self):
        # invoke the view and check the status message
        self.request.form['id'] = 'invalid'
        self.liveblog.unrestrictedTraverse('delete-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Invalid id specified.'
        self.assertEqual(msg[0].message, expected)

    def test_delete_microupdate_id_greater_than_lenght(self):
        # invoke the view and check the status message
        self.request.form['id'] = '2'
        self.liveblog.unrestrictedTraverse('delete-microupdate')()
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Invalid id specified.'
        self.assertEqual(msg[0].message, expected)
