Changelog
=========

1.0a2 (unreleased)
------------------

- Add a workflow specific to liveblogs.
  The workflow defines 3 states: private, active and inactive.
  This way we can control when automatic refresh of micro-updates happens.
  [hvelarde]

- Refresh the whole view when a micro-update has been deleted to avoid displaying invalid content.
  [hvelarde]

- The header viewlet was including the html and body tags on rendering.
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
