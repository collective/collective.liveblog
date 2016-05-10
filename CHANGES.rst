Changelog
=========

1.1b2 (2016-05-10)
------------------

- Micro-updates are now traversable;
  this allows to share them as separate pieces of content (closes `#19`_).
  [rodfersou, hvelarde]

- Use POST as request method on form used to edit micro-updates.
  [hvelarde]

- A new text field to describe the Liveblog was added.
  [hvelarde]

- Remove dependency on five.grok (closes `#5`_).
  [rodfersou]

- Package is now compatible with Plone 5.0 and Plone 5.1.
  [hvelarde]


1.1b1 (2016-04-19)
------------------

- Update view now uses batch pagination every 20 micro-updates to reduce load time for users with Editor role (closes `#10`_).
  [hvelarde]

- Depend on plone.batching; this drops support for Plone 4.2.
  [hvelarde]

- Use POST as request method on form used to add micro-updates.
  [hvelarde]

- Remove referenceable extra; Archetypes is no longer the default framework in Plone 5.
  Under Plone < 5.0 you should now explicitly add plone.app.referenceablebehavior to the `eggs` part of your buildout configuration.
  [hvelarde]

- The dates of micro-updates older than today were not shown in liveblogs on **private** and **inactive** states (fixes `#14`_).
  [hvelarde]


1.0b3 (2014-09-20)
------------------

- Rendering of ``plone.abovecontenttitle`` and ``plone.belowcontenttitle`` viewlets was removed from the ``update`` view.
  [hvelarde]

- Add styles for responsive (closes `#7`_).
  [agnogueira]

- Bylines on micro-updates now honor security settings and will be displayed to anonymous users only if they are allowed to see this information (closes `#6`_).
  [hvelarde]

- Editors can now edit micro-updates; a full refresh of the view will be scheduled after editing a micro-update to avoid displaying invalid content (closes `#3`_).
  [hvelarde]


1.0b2 (2014-09-13)
------------------

- An adapter listing the URLs to be purged when a Liveblog is modified was added.
  [ericof]

- Refactor ``recent-updates`` view to get rid of the timestamp parameter.
  This way we avoid a potential source of DoS attacks.
  [hvelarde]


1.0b1 (2014-09-05)
------------------

- Timestamp handling was simplified.
  [hvelarde]

- Implement the ``Expires`` header on ``recent-updates`` view.
  This will help us control better how long the page is going to live.
  [hvelarde]

- Add a workflow specific to liveblogs.
  The workflow defines 3 states: private, active and inactive.
  This way we can control when automatic refresh of micro-updates happens.
  [hvelarde]

- Refresh the whole view when a micro-update has been deleted to avoid displaying invalid content.
  [hvelarde]

- The header viewlet was including the ``html`` and ``body`` tags on rendering.
  [hvelarde]

- Lack of ``id`` attribute on field ``text`` was preventing TinyMCE editor from loading on Plone 4.2.
  [hvelarde]

- Fire ``ObjectModifiedEvent`` event on micro-updates deletion to invalidate caching on views.
  [hvelarde]

- Implement handling of ``If-Modified-Since`` request header on ``recent-updates`` view.
  [hvelarde]

- Markup of time tag used on automatic updates was fixed.
  [hvelarde]


1.0a1 (2014-09-01)
------------------

- Initial release.

.. _`#3`: https://github.com/collective/collective.liveblog/issues/3
.. _`#5`: https://github.com/collective/collective.liveblog/issues/5
.. _`#6`: https://github.com/collective/collective.liveblog/issues/6
.. _`#7`: https://github.com/collective/collective.liveblog/issues/7
.. _`#10`: https://github.com/collective/collective.liveblog/issues/10
.. _`#14`: https://github.com/collective/collective.liveblog/issues/14
.. _`#19`: https://github.com/collective/collective.liveblog/issues/19
