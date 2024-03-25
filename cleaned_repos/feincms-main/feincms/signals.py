from django.dispatch import Signal

# ------------------------------------------------------------------------
# This signal is sent when an item editor managed object is completely
# saved, especially including all foreign or manytomany dependencies.

itemeditor_post_save_related = Signal()

# ------------------------------------------------------------------------
