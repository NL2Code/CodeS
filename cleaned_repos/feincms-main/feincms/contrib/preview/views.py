from django.http import Http404
from django.shortcuts import get_object_or_404
from feincms.views import Handler


class PreviewHandler(Handler):
    """
    Preview handler

    The methods used in this handler should not be considered official API.

    *** Everything here is subject to change. ***
    """

    def get_object(self):
        """Get the page by the id in the url here instead."""

        page = get_object_or_404(self.page_model, pk=self.args[1])

        self.request.path = page.get_absolute_url()

        return page

    def handler(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Not found (not allowed)")
        response = super().handler(request, *args, **kwargs)
        response["Cache-Control"] = "no-cache, must-revalidate, no-store, private"
        return response
