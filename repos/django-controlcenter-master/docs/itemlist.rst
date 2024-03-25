ItemList options
================

``ItemList`` is very similar to django's `ModelAdmin`_. It renders a list of objects returned by :ref:`Widget <widget-options>` ``values`` method. The most awesome thing about this widget is it can handle almost everything: a list of model objects, namedtuples, dictionaries and sequences (generators are not sequences).

.. code-block:: python

    class ModelItemList(widgets.ItemList):
        model = Model
        queryset = model.active_objects.all()
        list_display = ('pk', 'field', 'get_foo')
        list_display_links = ('field', 'get_foo')
        template_name = 'my_custom_template.html'

        def get_foo(self, obj):
            return 'foo'
        get_foo.allow_tags = True
        get_foo.short_description = 'Foo!'

``list_display``
    For model objects, namedtuples and dictionaries, ``list_display`` is a list of fields or keys of object. For sequences index of each item in ``list_display`` becomes a key in object, i.e. ``dict(zip(list_display, sequence))``.

    Widget's and model's class methods can be used in ``list_display`` just like in ``ModelAdmin.list_display``. They must take an extra parameter for the object returned by ``values``. They may have two properties ``allow_tags`` (``True`` or ``False`` to allow or escape html tags) and ``short_description`` (for column name).

``list_display_links``
    Keys or fields should be linked to object's admin page. If nothing is provided ``ItemList`` will try to link the first column.

    .. note::
        If ``ItemList.values`` method doesn't return a list of model objects and ``ItemList.model`` is not defined, therefore there is no way left to build object's url.

``empty_message``
    If no items returned by ``values`` this message is displayed.

``sortable``
    Set ``True`` to make the list sortable.

    .. note::
        ``ModelAdmin`` gets sorted data from the database and ``ItemList`` uses Sortable.js to sort rows in browser and it's not aware about fields data-type. That means you should be careful with sorting stuff like this: ``%d.%m``.

.. _ModelAdmin: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-objects
