from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from controlcenter.widgets.charts import (
    BAR,
    LINE,
    PIE,
    BarChart,
    Chart,
    Chartist,
    LineChart,
    PieChart,
    SingleBarChart,
    SingleLineChart,
    SinglePieChart,
)

from . import TestCase


class BaseTest(TestCase):
    def test_chartist(self):
        class Chartist1(Chartist):
            foo = 'foo0'
            bar = 'bar0'
            options = {
                'foo': 'foo0',
                'bar': 'bar0'
            }

        class Chartist2(Chartist):
            foo = 'foo1'
            options = {
                'foo': 'foo1',
                'baz': 'baz1'
            }

            def egg(self):
                return 'egg'

        chartist = Chartist()
        chartist.update(Chartist1)
        chartist.update(Chartist2)

        # Works like python inheritance
        self.assertEqual(chartist.foo, 'foo1')
        self.assertEqual(chartist.bar, 'bar0')

        # Except methods
        with self.assertRaises(AttributeError):
            chartist.egg()

        # We have tested deepmerge in utils
        self.assertItemsEqual(chartist.options, ['bar', 'baz', 'foo'])

    def test_chart(self):
        chart = Chart(request=None)
        self.assertEqual(chart.legend, [])
        self.assertEqual(chart.labels, [])
        self.assertEqual(chart.series, [])

        # Queryset and model are not defined
        with self.assertRaises(ImproperlyConfigured):
            self.assertEqual(chart.values, [])

    def test_chartmeta(self):
        class Chart0(Chart):
            class Chartist:
                foo = 'foo0'
                bar = 'bar0'

        class Chart1(Chart):
            class Chartist:
                foo = 'foo1'
                baz = 'baz1'

        class Chart2(Chart0, Chart1):
            pass

        chart = Chart2(request=None)

        # Class removed
        self.assertFalse(hasattr(chart, 'Chartist'))
        # Attribute created
        self.assertTrue(hasattr(chart, 'chartist'))

        # Chartist inheritance
        self.assertEqual(chart.chartist.foo, 'foo1')
        self.assertEqual(chart.chartist.bar, 'bar0')
        self.assertEqual(chart.chartist.baz, 'baz1')

    def test_linechart(self):
        chart = LineChart(request=None)
        self.assertEqual(chart.chartist.klass, LINE)

    def test_piechart(self):
        chart = PieChart(request=None)
        self.assertEqual(chart.chartist.klass, PIE)

    def test_barchart(self):
        chart = BarChart(request=None)
        self.assertEqual(chart.chartist.klass, BAR)


class WidgetTest(TestCase):
    def setUp(self):
        for i in range(10):
            username = 'user{}'.format(i)
            User.objects.create_user(username, username + '@example.com',
                                     username + 'password')

    def test_singlepiechart(self):
        class Chart0(SinglePieChart):
            model = User

        chart0 = Chart0(request=None)

        # values_list is not defined
        with self.assertRaises(AssertionError):
            chart0.values

        class Chart1(Chart0):
            values_list = ['pk', 'email']
            limit_to = None  # there is limit by default

        chart1 = Chart1(request=None)
        self.assertItemsEqual(chart1.labels,
                              User.objects.values_list('pk', flat=True))

        self.assertItemsEqual(chart1.series,
                              User.objects.values_list('email', flat=True))

        # Override default limit_to
        max_items = 3

        class Chart2(Chart1):
            limit_to = max_items

        chart2 = Chart2(request=None)
        self.assertItemsEqual(
            chart2.labels,
            User.objects.values_list('pk', flat=True)[:max_items])

    def test_singlebarchart(self):
        chart0 = SingleBarChart(request=None)
        self.assertTrue(chart0.chartist.options['distributeSeries'])

    def test_singlelinechart(self):
        class Chart0(SingleLineChart):
            model = User
            values_list = ['pk', 'email']
            limit_to = None

        chart0 = Chart0(request=None)
        self.assertItemsEqual(
            chart0.series,
            [list(User.objects.values_list('email', flat=True))])
