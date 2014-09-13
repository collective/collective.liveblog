Changelog
=========

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
