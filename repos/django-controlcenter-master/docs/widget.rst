.. _widget-options:

Widget options
==============

``Widget`` is a base class of all widgets. It was designed to handle as many cases as possible, it's very flexible and doesn't expect all properties to be set.

Available properties:

``title``
    If not provided class name is used instead.

``model``
    The model to display data for.

``queryset``
    A ``QuerySet``. If not provided ``model._default_manager`` is called.

``changelist_url``
    Adds a clickable arrow at the corner of the widget with the link to model's admin changelist page. There are several ways to build the url:

    .. code-block:: python

        class ModelItemList(widgets.ItemList):
            # Pass the model to get plain 'changelist' url
            changelist_url = Model

            # Add GET params in dictionary to filter and order the queryset
            changelist_url = model, {'status__exact': 0, 'o': '-7.-1'}

            # Or pass them as a string
            changelist_url = model, 'status__exact=0&o=-7.-1'

            # No model required at all
            changelist_url = '/admin/model/'

            # External url example
            changelist_url = 'https://duckduckgo.com/'

``cache_timeout``
    Widget's body cache timeout in seconds. Default is ``None``.

``template_name``
    Template file name.

``template_name_prefix``
    A path to the directory with widget's template.

``limit_to``
    An integer specifying how many items should be returned by ``Widget.values`` method. By default it's ``10``.

``width``
    Widget's width. See :ref:`group-options` width.

``height``
    Widget's height. See :ref:`group-options` height.

``request``
    Every widget gets request object on initialization and stores it inside itself. This is literally turns ``Widget`` into a tiny ``View``:

    .. code-block:: python

        class OrderWidget(widgets.Widget):
            model = Order

            def get_queryset(self):
                queryset = super(MyWidget, self).get_queryset()
                if not self.request.user.is_superuser:
                    # Limits queryset for managers.
                    return queryset.filter(manager=self.request.user)

                # Superusers can filter by status.
                status = self.request.GET.get('status')
                if status in Order.STATUSES:
                    return queryset.filter(status=status)
                return queryset

Available methods:

``get_template_name``
    Returns the template file path.

``values``
    This method is automatically wrapped with cached_property_ descriptor to prevent multiple connections with whatever you use as a database.
    This also guarantees that the data won't be updated/changed during widget render process.

    .. note::
        Everything you wrap with cached_property_ becomes a property and can be only accessed as an attribute (without brackets).
        Don't use yield or return generator, they can't be cached properly (or cache them on you own).

    .. code-block:: python

        class OrderWidget(widgets.Widget)
            def values(self):
                vals = super(MyWidget, self).values  # No brackets!
                return [(date.strftime('%m.%d'), order)
                        for date, order in vals]  # No yield or generators!

            def dates(self):
                return [date for date, order in self.values]

            # `values` are cached and can be accessed
            # as many times as you want
            def orders(self):
                return [order for date, order in self.values]

    .. note::
        By default ``limit_to`` is used to limit queryset in here and not in ``get_queryset`` because if ``QuerySet`` is sliced ones it's can't be adjusted anymore, i.e. calling ``super(...).get_queryset()`` makes no sense in a subclass.

.. _cached_property: https://docs.djangoproject.com/en/1.9/ref/utils/#django.utils.functional.cached_property