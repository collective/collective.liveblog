# -*- coding:utf-8 -*-
from plone import api
from collective.liveblog.config import PROJECTNAME

import logging

logger = logging.getLogger(PROJECTNAME)


def cook_css_resources(context):
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')
