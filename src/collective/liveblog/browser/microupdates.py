# -*- coding: utf-8 -*-
from collective.liveblog import _
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone import api
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

grok.templatedir('templates')


class AddMicroUpdateView(grok.View):

    """Add a micro-update to the Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.name('add-microupdate')
    grok.require('collective.liveblog.AddMicroUpdate')

    def render(self):
        title = self.request.form.get('title', None)
        text = self.request.form.get('text', None)
        if not text:
            msg = _(u'There were some errors. Required input is missing.')
            api.portal.show_message(msg, self.request, type='error')
        else:
            adapter = IMicroUpdateContainer(self.context)
            adapter.add(MicroUpdate(title, text))

            # notify the Liveblog has a new micro-update
            notify(ObjectModifiedEvent(self.context))
            msg = _(u'Item published.')
            api.portal.show_message(msg, self.request)

        update_url = self.context.absolute_url() + '/update'
        self.request.response.redirect(update_url)


class DeleteMicroUpdateView(grok.View):

    """Delete a micro-update from the Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.name('delete-microupdate')
    grok.require('zope2.DeleteObjects')

    def render(self):
        id = self.request.form.get('id', None)
        if not id:
            msg = _(u'There were some errors. Required input is missing.')
            api.portal.show_message(msg, self.request, type='error')
            return
        else:
            try:
                id = int(id)
            except ValueError:
                msg = _(u'Invalid id specified.')
                api.portal.show_message(msg, self.request, type='error')
                return
            adapter = IMicroUpdateContainer(self.context)
            if id >= len(adapter):
                msg = _(u'Invalid id specified.')
                api.portal.show_message(msg, self.request, type='error')
                return
            else:
                adapter.delete(id)
                msg = _(u'Item deleted.')
                api.portal.show_message(msg, self.request)

        update_url = self.context.absolute_url() + '/update'
        self.request.response.redirect(update_url)
