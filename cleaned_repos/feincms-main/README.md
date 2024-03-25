FeinCMS - An extensible Django-based CMS
========================================

When was the last time, that a pre-built software package you wanted to
use got many things right, but in the end, you still needed to modify
the core parts of the code just because it wasn't (easily) possible to
customize the way, a certain part of the system behaved?

Django came to rescue all of us, who were not happy with either doing
everything on our own or customizing another software package until it
was impossible to update.

The biggest strength of a framework-like design is, that it tries not
to have a too strong view of what the user should do. It should make some
things easy, but just GET OUT OF THE WAY most of the time.

Just after discovering the benefits of a framework-like approach to
software design, we fall back into the rewrite everything all the time
mindset and build a CMS which has very strong views how content should
be structured. One rich text area, a media library and some templates,
and we have a simple CMS which will be good enough for many pages. But
what if we want more? If we want to be able to add custom content? What
if the user can't be trusted to resize images before uploading them?
What if you'd like to add a gallery somewhere in between other content?
What if the user should be able to administer not only the main content,
but also a sidebar, the footer?

With FeinCMS, this does not sound too good to be true anymore. And it's
not even complicated.


FeinCMS is an extremely stupid content management system. It knows
nothing about content -- just enough to create an admin interface for
your own page content types. It lets you reorder page content blocks
using a drag-drop interface, and you can add as many content blocks
to a region (f.e. the sidebar, the main content region or something
else which I haven't thought of yet). It provides helper functions,
which provide ordered lists of page content blocks. That's all.
