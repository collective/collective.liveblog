# -*- coding: utf-8 -*-
from collective.liveblog.adapters import IMicroUpdateContainer
from collective.liveblog.interfaces import ILiveblog
from five import grok
from plone import api
from plone.dexterity.content import Container


class Liveblog(Container):

    """A liveblog is a blog post which is intended to provide a rolling
    textual coverage of an ongoing event.

    The _last_microupdate_edition and _last_microupdate_deletion attributes
    are used to detect if a hard refresh of the views is needed.
    """

    grok.implements(ILiveblog)

    _last_microupdate_edition = '0.0'
    _last_microupdate_deletion = '0.0'

    def get_microupdates(self):
        """Return the list of micro-updates in the Liveblog in reverse order."""
        container = IMicroUpdateContainer(self)
        updates = []
        for id, update in enumerate(container):
            if update is None:
                continue  # update has been removed
            updates.append(dict(
                id=id,
                creator=update.creator,
                timestamp=update.timestamp,  # 1409223490.21,
                datetime=api.portal.get_localized_time(update.created, True),  # 28/08/2014 10h58
                date=api.portal.get_localized_time(update.created),  # 28/08/2014
                time=api.portal.get_localized_time(update.created, time_only=True),  # 10h58
                isoformat=update.created.isoformat()[:-3],  # 2014-08-28T10:58:10.209468
                title=update.title,
                text=update.text,
            ))
        updates.reverse()  # show micro-updates in reverse order
        return updates
