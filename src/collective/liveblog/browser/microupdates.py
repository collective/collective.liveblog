# -*- coding: utf-8 -*-
from collective.liveblog import _
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.adapters import MicroUpdate
from datetime import datetime
from plone import api
from Products.Five.browser import BrowserView
from time import time
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class BaseMicroUpdateView(BrowserView):

    """Base view with helper methods for micro-updates."""

    def _redirect_with_status_message(self, msg, type='info'):
        api.portal.show_message(msg, self.request, type=type)
        update_url = self.context.absolute_url() + '/update'
        self.request.response.redirect(update_url)

    def _validate_microupdate_id(self):
        """Validate the micro-update id for the request."""
        id = self.request.form.get('id', None)
        if id is None:
            msg = _(u'No micro-update selected.')
            api.portal.show_message(msg, self.request, type='error')
            return False
        else:
            try:
                id = int(id)
            except ValueError:
                msg = _(u'Micro-update id is not an integer.')
                api.portal.show_message(msg, self.request, type='error')
                return False
            adapter = IMicroUpdateContainer(self.context)
            if id >= len(adapter):
                msg = _(u'Micro-update id does not exist.')
                api.portal.show_message(msg, self.request, type='error')
                return False
        return True


class AddMicroUpdateView(BaseMicroUpdateView):

    """Add a micro-update to the Liveblog."""

    def __call__(self):
        return self.render()

    def render(self):
        title = self.request.form.get('title', '')
        text = self.request.form.get('text', None)

        if text is None:  # something went wrong
            msg = _(u'Required text input is missing.')
            self._redirect_with_status_message(msg, type='error')
            return

        adapter = IMicroUpdateContainer(self.context)
        adapter.add(MicroUpdate(title, text))
        # XXX: why do we need to handle this again here?
        #      we're already firing an event on the adapter
        # notify the Liveblog has a new micro-update
        notify(ObjectModifiedEvent(self.context))
        msg = _(u'Item published.')
        self._redirect_with_status_message(msg)


class EditMicroUpdateView(BaseMicroUpdateView):

    """Edit a micro-update in the Liveblog."""

    def __call__(self):

        if 'form.buttons.save' in self.request.form:  # Save changes
            return self.save()

        if 'form.buttons.cancel' in self.request.form:  # Cancel edit?
            return self.cancel()

        if self._validate_microupdate_id():
            return self.render()

    def render(self):
        id = self.request.form.get('id')
        adapter = IMicroUpdateContainer(self.context)
        self._title = adapter[id].title
        self._text = adapter[id].text
        return self.index()

    def save(self):
        if self._validate_microupdate_id():
            id = self.request.form.get('id')
            title = self.request.form.get('title', '')
            text = self.request.form.get('text', None)

            if text is None:  # something went wrong
                msg = _(u'Required text input is missing.')
                self._redirect_with_status_message(msg, type='error')
                return

            # save the changes and return
            adapter = IMicroUpdateContainer(self.context)
            adapter[id].title = title
            adapter[id].text = text
            adapter[id].modified = datetime.now()
            notify(ObjectModifiedEvent(self.context))
            # schedule a hard refresh
            self.context._last_microupdate_edition = str(time())
            msg = _(u'Item saved.')
            self._redirect_with_status_message(msg)

    def cancel(self):
        msg = _(u'Edit cancelled.')
        self._redirect_with_status_message(msg)

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text


class DeleteMicroUpdateView(BaseMicroUpdateView):

    """Delete a micro-update from the Liveblog."""

    def __call__(self):
        if self._validate_microupdate_id():
            return self.render()

    def render(self):
        id = self.request.form.get('id', None)
        adapter = IMicroUpdateContainer(self.context)
        adapter.delete(id)
        # XXX: why do we need to handle this again here?
        #      we're already firing an event on the adapter
        notify(ObjectModifiedEvent(self.context))
        # schedule a hard refresh
        self.context._last_microupdate_deletion = str(time())
        msg = _(u'Item deleted.')
        self._redirect_with_status_message(msg)
