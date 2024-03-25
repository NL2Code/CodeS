Chart options
=============

Django-controlcenter uses Chartist.js_ to create beautiful, responsive and dpi independent svg charts. ``Chart`` class has three extra cached methods:

``labels``
    Represents values on x-axis.

``series``
    Represents values on y-axis.

    .. note::
        Except for the ``SingleBarChart`` and ``SinglePieChart`` classes, this method must return a list of lists.

``legend``
    Chartist.js_ doesn't display series on chart which is really odd. As a workaround you can duplicate values on x-axis and then put labels in legend (and vice versa). Here is an example:

    .. code-block:: python

        class MyBarChart(widgets.SingleBarChart):
            def series(self):
                # Y-axis
                return [y for x, y in self.values]

            def labels(self):
                # Duplicates series on x-axis
                return self.series

            def legend(self):
                # Displays labels in legend
                return [x for x, y in self.values]

Chartist
--------

``Chart`` may have a special ``Chartist`` class inside itself to configure Chartist.js_:

.. code-block:: python

    class MyChart(widgets.Chart):
        class Chartist:
            point_labels = True
            options = {
                'reverseData': True,
                ...
            }


When you define ``Chartist`` it inherits chart's parent's ``Chartist`` properties automatically. The reason why hacky inheritance is used is the ``options`` property.

``options``
    It's a nested dictionary of options to be passed to Chartist.js_ constructor. Python dictionaries can't be inherited properly in a classic way. That's why when you define ``options`` in child ``Chartist`` class it deep copies and merges parent's one with it's own.

    .. code-block:: python

        class MyChart(widgets.Chart):
            class Chartist:
                point_labels = True
                options = {
                    'reverseData': True,
                    'foo': {
                        'bar': True
                    }
                }

        class MyNewChart(MyChart):
            class Chartist:
                options = {
                    'fullWidth': True,
                }

        # MyNewChart.Chartist copies MyChart.Chartist attributes
        MyNewChart.chartist.options['reverseData']  # True
        MyNewChart.chartist.options['foo']['bar']  # True
        MyNewChart.chartist.options['fullWidth']  # True
        MyNewChart.chartist.point_labels  # True

``klass``
    Type of the chart. Available values are defined in ``widgets`` module: ``LINE``, ``BAR`` and ``PIE``. Default is ``LINE``.

``scale``
    Aspect ratio of the chart. By default it's ``octave``. See the full list of available values on `official web-site`__ (press 'Show default settings').

``LineChart``
    Displays point labels on ``LINE`` chart.

.. note::
    If you don't want to use Chartist.js_, don't forget to override ``Dashboard.Media`` to make not load useless static files.


LineChart
---------

Line chart with point labels and useful Chartist.js_ settings. This chart type is usually used to display latest data dynamic sorted by date which comes in backward order from database (because you order entries by date and then slice them). ``LineChart`` passes ``'reverseData': True`` option to Chartist constructor which reverses ``series`` and ``labels``.


TimeSeriesChart
---------------

A variant of ``LineChart`` for time-series data.

This chart does not define ``labels``. Instead, each ``series`` must consist of pairs of ``x`` and ``y`` values,
where ``x`` is a POSIX timestamp (as returned by `datetime.timestamp`_).

.. code-block:: python

    class MyTimeSeriesChart(widgets.TimeSeriesChart):

        def series(self):
            return [
                [{'x': when.timestamp(), 'y': value} for (when, value) in samples],
            ]

The X-axis timestamp labels will be formatted using `Date.toLocaleString`_.

To customise the timestamp label formatting, specify ``Date.toLocaleString``'s ``options`` parameter
using the ``timestamp_options`` configuration property.
For example, to only show the year and short month as labels:

.. code-block:: python

    class MyTimeSeriesChart(widgets.TimeSeriesChart):
        class Chartist:
            timestamp_options = {
                'year': 'numeric',
                'month': 'short',
            }

To specify when ticks shown, see the `Chartist.FixedScaleAxis`_ documentation.
For example:

.. code-block:: python

    class MyTimeSeriesChart(widgets.TimeSeriesChart):
        class Chartist:
            options = {
                'axisX': {
                    # Use 'divisions' for a fixed number of sub-division ticks.
                    'divisions': 4,
                    # Alternatively, use 'ticks' to explicitly specify a list of timestamps.
                },
            }



.. _`datetime.timestamp`: https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp
.. _`Date.toLocaleString`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString
.. _`Chartist.FixedScaleAxis`: https://gionkunz.github.io/chartist-js/api-documentation.html#module-chartistfixedscaleaxis


BarChart
--------

Bar type chart.

PieChart
--------

Pie type chart.

.. note::
    ``PieChart.series`` must return a flat list.

SingleBarChart, SinglePieChart, SingleLineChart
-----------------------------------------------

A special classes for charts with a single series. Simply define *label* and *series* fields in ``values_list`` then provide ``model`` or ``queryset``. That's it.

This widget will render a bar chart of top three players:

.. code-block:: python

    class MySingleBarChart(widgets.SingleBarChart):
        # label and series
        values_list = ('username', 'score')
        # Data source
        queryset = Player.objects.order_by('-score')
        limit_to = 3

.. note::
    ``SingleLineChart.series`` must return a list with a single list.


Chartist colors
---------------

There are two themes for charts. See :ref:`customization`.

.. __: https://gionkunz.github.io/chartist-js/getting-started.html#default-settings
.. _Chartist.js: http://gionkunz.github.io/chartist-js/
