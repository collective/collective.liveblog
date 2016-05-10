********
Liveblog
********

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A liveblog is a blog post which is intended to provide a rolling textual coverage of an ongoing event.

A liveblog is continuously updated with timestamped micro-updates which are placed above previous micro-updates.

Typical use case is the following:

- The publisher of a news site creates a liveblog
- Editors add micro-updates to the liveblog as the event goes on
- Visitors of the site on the liveblog get micro-updates automatically via AJAX calls

Who is using it?
----------------

These are some of the sites using ``collective.liveblog``:

- `CartaCapital <http://www.cartacapital.com.br/>`_ (BR)
- `Portal Brasil 2016 <http://www.brasil2016.gov.br/>`_ (BR)

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.liveblog.svg
    :target: https://pypi.python.org/pypi/collective.liveblog

.. image:: https://img.shields.io/travis/collective/collective.liveblog/master.svg
    :target: http://travis-ci.org/collective/collective.liveblog

.. image:: https://img.shields.io/coveralls/collective/collective.liveblog/master.svg
    :target: https://coveralls.io/r/collective/collective.liveblog

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

After installing the package you will see a new content type available: Liveblog.

A liveblog has a title, a description and an image field.
The image field is used to set up a header on the liveblog.

.. figure:: https://raw.github.com/collective/collective.liveblog/master/create-liveblog.png
    :align: center
    :height: 440px
    :width: 640px

Before feeding the liveblog with micro-updates you will need to activate it.
Now, go to the Update tab and start writing micro-updates.

A micro-update is basically a text that should optionally have a title.
The date and time of the micro-update is automatically recorded for you.
After publishing a micro-update you will see it on top of your liveblog before all previous micro-updates.

.. figure:: https://raw.github.com/collective/collective.liveblog/master/create-microupdate.png
    :align: center
    :height: 580px
    :width: 640px

All people viewing your liveblog will receive automatic updates every minute.

.. figure:: https://raw.github.com/collective/collective.liveblog/master/anonymous-view.png
    :align: center
    :height: 560px
    :width: 640px

Micro-updates can be viewed as separate pieces of content;
this makes easy to share them in social networks.

.. figure:: https://raw.github.com/collective/collective.liveblog/master/microupdate.png
    :align: center
    :height: 480px
    :width: 640px

Many editors can update the liveblog safely.
When another editor adds a micro-update you will see it automatically on your screen even if you are writing a new one.

You can delete micro-updates also.
This will trigger a complete page refresh on all current viewers to avoid the displaying of invalid content in your liveblog.
The page refresh will happen withing the next minute.
If another editor deletes a micro-update you will see a message on your screen but no content refresh will take place.
This way we avoid interrupting editors from their work.

.. figure:: https://raw.github.com/collective/collective.liveblog/master/remote-delete.png
    :align: center
    :height: 500px
    :width: 640px

When a liveblog is not going to be updated anymore you should deactivate it.

Workflow
--------

The package defines a workflow to be used with the content type (Liveblog Workflow).

The workflow defines 3 states: private, active and inactive.
Liveblogs are created in the private state.
When activated, the liveblog will be published and automatic refresh of micro-updates will be enabled.
When deactivated, the liveblog will remain public, but automatic refresh of micro-updates will be disabled.
No micro-updates can be added to a liveblog in inactive state.
To continue adding micro-updates, just activate the liveblog again.

How does it work
----------------

TBD.
