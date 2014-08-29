# -*- coding: utf-8 -*-
from collective.liveblog.browser.view import View
from collective.liveblog.interfaces import IBrowserLayer
from collective.liveblog.interfaces import ILiveblog
from five import grok

grok.templatedir('templates')


class Update(View):

    """View to add micro-updates to a Liveblog."""

    grok.context(ILiveblog)
    grok.layer(IBrowserLayer)
    grok.require('collective.liveblog.AddMicroUpdate')
