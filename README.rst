********
Liveblog
********

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A liveblog is a blog post which is intended to provide a rolling textual coverage of an ongoing event.

A liveblog is continuously updated with timestamped micro-updates which are placed above previous micro-updates.

Typical use case is the following:

- the publisher of a news site creates a liveblog
- editors add micro-updates to the liveblog as the event goes on
- visitors of the liveblog get micro-updates automatically via AJAX calls

Mostly Harmless
===============

.. image:: https://secure.travis-ci.org/collective/collective.liveblog.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.liveblog

.. image:: https://coveralls.io/repos/collective/collective.liveblog/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.liveblog

.. image:: https://pypip.in/d/collective.liveblog/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.liveblog/

Todo list
---------

- Do not load all micro-updates by default as the page could grow huge
- Implement infinite scrolling
- Prettify the prepend of micro-updates
- Use fuzzy dates

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.liveblog/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.liveblog

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.liveblog`` and click the 'Activate' button.

.. Note::
    You may have to empty your browser cache and save your resource registries in order to see the effects of the product installation.

Usage
-----

TBD
