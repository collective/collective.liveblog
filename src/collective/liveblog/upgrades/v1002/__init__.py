# -*- coding:utf-8 -*-
from collective.liveblog.interfaces import ILiveblog
from collective.liveblog.logger import logger
from ftw.upgrade.workflow import WorkflowChainUpdater
from plone import api


def migrate_liveblog_workflow(context):
    """Migrate liveblog workflow."""
    review_state_mapping = {
        ('liveblog_workflow', 'simple_publication_workflow'): {
            'private': 'private',
            'active': 'published',
            'inactive': 'published',
        }
    }

    catalog = api.portal.get_tool('portal_catalog')
    query = dict(object_provides=ILiveblog.__identifier__)
    results = catalog.unrestrictedSearchResults(**query)
    objects = (b.getObject() for b in results)

    # all existing liveblogs must use now simple_publication_workflow
    wtool = api.portal.get_tool('portal_workflow')
    with WorkflowChainUpdater(objects, review_state_mapping):
        wtool.setChainForPortalTypes(
            ('Liveblog',), ('simple_publication_workflow',))
        logger.info('Liveblog objects now use simple_publication_workflow')

    # remove liveblog_workflow
    if 'liveblog_workflow' in wtool:
        api.content.delete(obj=wtool.liveblog_workflow)
        logger.info('Liveblog workflow removed')
