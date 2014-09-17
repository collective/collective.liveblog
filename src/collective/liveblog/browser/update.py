# -*- coding: utf-8 -*-
from collective.liveblog import _
from collective.liveblog.browser.view import View
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from zope.i18n import translate
from zope.security import checkPermission

grok.templatedir('templates')


class Update(View):

    """View to add micro-updates to a Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('collective.liveblog.AddMicroUpdate')

    def can_edit_objects(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def can_delete_objects(self):
        return checkPermission('zope2.DeleteObjects', self.context)

    def delete_confirmation(self):
        msg = _(u'Do you really want to delete this item?')
        msg = translate(msg, 'collective.liveblog', context=self.request)
        return u"return confirm('{0}')".format(msg)
