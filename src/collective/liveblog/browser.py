# -*- coding: utf-8 -*-
from collective.liveblog import _
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone import api
from plone.memoize import ram
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

grok.templatedir('templates')


def _render_updates_cachekey(method, self):
    return len(self._updates())


class View(grok.View):

    """Default view for Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('zope2.View')

    @property
    def can_add_microupdate(self):
        """Return True if the user has permission to add a micro-update."""
        mt = api.portal.get_tool('portal_membership')
        return mt.checkPermission(
            'collective.liveblog.AddMicroUpdate', self.context)

    def _updates(self):
        """Return the list of micro-updates in the Liveblog in reverse order."""
        container = IMicroUpdateContainer(self.context)
        updates = []
        for id, update in enumerate(container):
            if update is None:
                continue  # update has been removed
            updates.append(dict(
                id=id + 1,
                creator=update.creator,
                created=api.portal.get_localized_time(update.created, True),
                time_only=api.portal.get_localized_time(update.created, time_only=True),
                title=update.title,
                text=update.text,
            ))
        updates.reverse()  # show micro-updates in reverse order
        return updates

    @ram.cache(_render_updates_cachekey)
    def updates(self):
        return self._updates()

    @property
    def has_updates(self):
        return len(self.updates()) > 0


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

        self.request.response.redirect(self.context.absolute_url())
