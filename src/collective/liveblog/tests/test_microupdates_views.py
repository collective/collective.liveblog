# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.testing import INTEGRATION_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides

import unittest


class BaseMicroUpdateViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')
        self.view = api.content.get_view(
            'base-microupdate', self.liveblog, self.request)
        adapter = IMicroUpdateContainer(self.liveblog)
        adapter.add(MicroUpdate(u'', u'Check me!'))

    def test_validate_microupdate_id(self):
        self.request.form['id'] = '0'
        valid = self.view._validate_microupdate_id()
        self.assertTrue(valid)

    def test_validate_microupdate_no_id(self):
        valid = self.view._validate_microupdate_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'No micro-update selected.'
        self.assertEqual(msg[0].message, expected)

    def test_validate_microupdate_invalid_id(self):
        self.request.form['id'] = 'invalid'
        valid = self.view._validate_microupdate_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Micro-update id is not an integer.'
        self.assertEqual(msg[0].message, expected)

    def test_validate_microupdate_id_greater_than_lenght(self):
        self.request.form['id'] = '2'
        valid = self.view._validate_microupdate_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Micro-update id does not exist.'
        self.assertEqual(msg[0].message, expected)


class AddMicroUpdateViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')

    def test_add_microupdate_no_parameters(self):
        self.liveblog.unrestrictedTraverse('add-microupdate')()
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Required text input is missing.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/liveblog/update',
        )

    def test_add_microupdate(self):
        self.request.form['title'] = ''
        self.request.form['text'] = 'Extra! Extra! Read All About It!'
        self.liveblog.unrestrictedTraverse('add-microupdate')()
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item published.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/liveblog/update',
        )


class EditMicroUpdateViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.liveblog = api.content.create(
                self.portal, 'Liveblog', 'liveblog')
        adapter = IMicroUpdateContainer(self.liveblog)
        adapter.add(MicroUpdate(u'', u'Edit me!'))

    def test_edit_microupdate(self):
        self.request.form['id'] = '0'
        self.request.form['text'] = 'Edited!'
        self.request.form['form.buttons.save'] = 'Save'
        self.liveblog.unrestrictedTraverse('edit-microupdate')()
        # liveblog was updated
        self.assertNotEqual(self.liveblog._last_microupdate_edition, '0.0')
        # micro-update was modified
        adapter = IMicroUpdateContainer(self.liveblog)
        self.assertEqual(adapter[0].text, 'Edited!')
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item saved.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/liveblog/update',
        )


class DeleteMicroUpdateViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

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
        self.request.form['id'] = '0'
        self.liveblog.unrestrictedTraverse('delete-microupdate')()
        # liveblog was updated
        self.assertNotEqual(self.liveblog._last_microupdate_deletion, '0.0')
        # micro-update was deleted
        adapter = IMicroUpdateContainer(self.liveblog)
        self.assertIsNone(adapter[0])
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item deleted.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/liveblog/update',
        )
