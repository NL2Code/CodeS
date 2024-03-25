Dashboards
==========

Django-controlcenter supports unlimited number of dashboards. You can access them by passing those slugs in ``settings.CONTROLCENTER_DASHBOARDS`` to url: ``/admin/dashboards/<slugs>/``.


Dashboard options
-----------------

``Dashboard`` class has only two properties:

``title``
    By default the class name is used as title.

``widgets``
    A list of widgets. To group multiple widgets in one single block pass them in a list or wrap with a special ``Group`` class for additional options.

Here is an example:

.. code-block:: python

    from controlcenter import Dashboard, widgets

    class OrdersDashboard(Dashboard):
        title = 'Orders'
        widgets = (
            NewOrders,
            (OrdersInProgress, FinishedOrders),
            Group([FinishedOrdersChart, ThisWeekOrdersChart],
                  # Makes whole block larger
                  width=widgets.LARGE,
                  # Add html attribute class
                  attrs={'class': 'my_fancy_group'})
        )


The grid
--------

Dashboard is a responsive grid that appropriately scales up to 6 columns as the viewport size increases. It uses Masonry.js_ to make a better grid layout.

===================== ===== ===== ===== ===== ===== =====
Viewport/column width   1     2     3     4     5     6
--------------------- ----- ----- ----- ----- ----- -----
initial                              100%
--------------------- -----------------------------------
> 768px                      50%              100%
--------------------- ----------------- -----------------
> 1000px               25%   33%   50%   66%   75%  100%
===================== ===== ===== ===== ===== ===== =====

Most useful sizes are available in ``widgets`` module:

.. code-block:: python

    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    LARGER = 4
    LARGEST = 5
    FULL = 6


Media class
-----------

``Dashboard`` uses Media_ class from django to include static files on page:

.. code-block:: python

    class OrdersDashboard(Dashboard):
        title = 'Orders'
        widgets = (
            NewOrders,
            ...
        )

        class Media:
            css = {
                'all': 'my.css'
            }

.. _group-options:

Group options
-------------

Every element in ``Dashboard.widgets`` is automatically wrapped with a Group instance even if it's a single widget. This is the necessary process to make possible stack widgets together in one single block. You can define Group manually to control it's html attributes or override widget's width and height properties. For example:

.. code-block:: python

    class MyWidget(widgets.ItemList):
        model = Pizza
        values_list = ('name', 'price')
        width = widgets.LARGE

    class MyDashboard(Dashboard):
        widgets = (
            widgets.Group([MyWidget], width=widgets.LARGER, height=300),
        )

``attrs``
    A dictionary of html attributes to set to the group (``class``, ``id``, ``data-foo``, etc.).


``width``
    An integer specifying the width in *columns*. By default the biggest value within the group is chosen.

``height``
    An integer specifying the ``max-height`` of the block in pixels. If necessary a scroll appears.

    .. note::
        By default Group has the height of the biggest widget within group. Switching tabs (widgets) won't change it, because that will make the whole grid float.

``Group`` supports the following methods:

``get_id``
    Returns ``id`` from ``attrs`` or a joined string of widget slugs (names) with ``_and_`` separator.

``get_class``
    Returns ``class`` from ``attrs``.

``get_attrs``
    Returns ``attrs`` without ``id`` and ``class`` keys.

``get_width``
    Returns ``width`` if provided or biggest value in the group.

``get_height``
    Returns ``height`` if provided or biggest value in the group.

.. _Media: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-asset-definitions
.. _Masonry.js: http://masonry.desandro.com/
