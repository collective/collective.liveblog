# -*- coding:utf-8 -*-
from collective.liveblog.logger import logger
from plone import api


def cook_css_resources(context):  # pragma: no cover
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')
