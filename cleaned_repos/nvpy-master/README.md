nvPY
====

nvpy is a simplenote-syncing note-taking tool inspired by Notational
Velocity (and a little bit by nvALT too) on OSX and ResophNotes on
Windows. It is significantly uglier, but it is cross-platform.  Yes,
you heard right, you can run this on Linux (tested), Windows (tested)
and OS X (lightly tested).

It was written by Charl Botha, who needed a simplenote client on Linux and doesn't mind ugliness (that much). Sjaak Westdijk has contributed significantly to the codebase since right after the 0.8.5 release.
Since nvPY v1.0.0, it is maintained by `yuuki0xff <https://github.com/yuuki0xff>`_.

* nvpy lives happily at https://github.com/cpbotha/nvpy
* For news and discussion, join the `public nvpy google group <https://groups.google.com/d/forum/nvpy>`_ or subscribe to its `RSS topic feed <https://groups.google.com/group/nvpy/feed/rss_v2_0_topics.xml>`_.

Features
========

* Syncs with simplenote.
* Support for simplenote tags and note pinning.
* Partial syncs (whilst notes are being edited) are done by a
  background thread so you can keep on working at light speed.
* Can be used offline, also without simplenote account.
* Search box does realtime gstyle or regular expression searching in all your
  notes. All occurrences of the search string are also
  highlighted in currently active note.
* Markdown rendering to browser.
* Continuous rendering mode: If you activate this before
  starting the markdown rendering, nvpy will render new html of
  the currently open note every few seconds. Due to the refresh
  tag in the generated HTML, the browser will refresh every few
  seconds. MAGIC UPDATES!
* reStructuredText (reST) rendering to browser. Yes, you can use nvPY
  as your reST previewer.
* Automatic hyperlink highlighting in text widget.
* KickAss(tm) inter-note linking with [[note name]]. If note name is
  not found in current list of notes, assumes it's a regular expression
  and sets it in the search bar. See the `screencast <http://youtu.be/NXuVMZr31SI>`_.