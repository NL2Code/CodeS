from ..utils import deepmerge
from .core import Widget, WidgetMeta

__all__ = ['LineChart', 'TimeSeriesChart', 'BarChart', 'PieChart',
           'SingleLineChart', 'SingleBarChart', 'SinglePieChart',
           'LINE', 'BAR', 'PIE']

# Chart types
PIE, BAR, LINE = 'Pie', 'Bar', 'Line'


class Chartist(object):
    def __init__(self):
        self.options = {}

    def update(self, obj):
        for key in dir(obj):
            value = getattr(obj, key)
            if key == 'options':
                self.options = deepmerge(self.options, value)
            elif not key.startswith('__') and not callable(value):
                setattr(self, key, value)


class ChartMeta(WidgetMeta):
    CACHED_ATTRS = WidgetMeta.CACHED_ATTRS + (
        'labels',  # chart x-axis labels
        'series',  # chart y-axis values
        'legend',  # chart legend
    )

    def __new__(mcs, name, bases, attrs):
        # Saves defined configuration
        chartist = attrs.pop('Chartist', None)

        new_class = super(ChartMeta, mcs).__new__(mcs, name, bases, attrs)
        new_class.chartist = Chartist()

        # Copies parents options
        for base in bases:
            if hasattr(base, 'chartist'):
                new_class.chartist.update(base.chartist)

        # Overrides inherited stuff
        if chartist:
            new_class.chartist.update(chartist)
        return new_class


class Chart(Widget, metaclass=ChartMeta):
    template_name = 'chart.html'

    class Chartist:
        klass = LINE
        scale = 'octave'

    def legend(self):
        # Legend for chart
        return []

    def labels(self):
        # List of x-axis labels
        # Do not return generator!
        return []

    def series(self):
        # List of y-axis values
        # Do not return generator!
        return []


class LineChart(Chart):
    class Chartist:
        point_labels = True
        options = {
            # In common cases you need something last ordered by descending,
            # setting `reverseData` all the time is just annoying
            'reverseData': True,
            'axisY': {
                'onlyInteger': True,
            },
            'fullWidth': True,
        }


class TimeSeriesChart(Chart):
    class Chartist:
        point_labels = True
        options = {
            'axisY': {
                'onlyInteger': True,  # Same default as LineChart.
            },
        }
        time_series = True
        timestamp_options = {}


class BarChart(Chart):
    class Chartist:
        klass = BAR


class PieChart(Chart):
    class Chartist:
        klass = PIE


class SinglePieChart(PieChart):
    values_list = None

    def labels(self):
        return [x for x, y in self.values]

    def series(self):
        return [y for x, y in self.values]

    def values(self):
        assert self.values_list, ('Please define {0}.values_list '
                                  'or override {0}.values'.format(self))
        queryset = self.get_queryset().values_list(*self.values_list)
        if self.limit_to:
            return queryset[:self.limit_to]
        return queryset


class SingleBarChart(SinglePieChart, BarChart):
    class Chartist:
        options = {
            'distributeSeries': True
        }


class SingleLineChart(SinglePieChart, LineChart):
    def series(self):
        vals = super(SingleLineChart, self).series
        return [vals]
