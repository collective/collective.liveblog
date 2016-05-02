# -*- coding: utf-8 -*-
from collective.liveblog import _
from collective.liveblog.browser.view import View
from collective.liveblog.config import BATCH_SIZE
from collective.liveblog.config import ORPHAN
from plone import api
from plone.batching import Batch
from zope.i18n import translate
from zope.security import checkPermission


class Update(View):

    """View to add micro-updates to a Liveblog."""

    @property
    def batch(self):
        """Encapsulate sequence in batches of size."""
        return Batch(self.updates(), BATCH_SIZE, self.start, orphan=ORPHAN)

    def can_edit_objects(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def can_delete_objects(self):
        return checkPermission('zope2.DeleteObjects', self.context)

    def delete_confirmation(self):
        msg = _(u'Do you really want to delete this item?')
        msg = translate(msg, 'collective.liveblog', context=self.request)
        return u"return confirm('{0}')".format(msg)

    @property
    def automatic_updates_enabled(self):
        """Check if the Livelog must be updated automatically.
        Automatic updates should be enabled on first page of batch.
        """
        enabled = super(Update, self).automatic_updates_enabled
        return enabled and self.start == 0

    def __call__(self):
        self.start = int(self.request.get('b_start', 0))
        if self.start != 0:
            msg = _(u'You must be on the first page of the batch to add micro-updates.')
            api.portal.show_message(msg, self.request, type='info')
        return self.index()
