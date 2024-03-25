import itertools

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet

from controlcenter import widgets
from controlcenter.widgets.core import BaseWidget, WidgetMeta

from . import TestCase


class WidgetMetaTest(TestCase):
    def test_property_cache(self):
        class TestWidget(metaclass=WidgetMeta):
            def values(self):
                return next(itertools.count())

        widget = TestWidget()

        # self.values is a cached property
        for i in range(2):
            self.assertEqual(widget.values, 0)


class BaseWidgetTest(TestCase):
    def setUp(self):
        self.options = {'foo': 'bar'}
        self.widget0 = BaseWidget(request=None, **self.options)
        self.widget1 = BaseWidget(request=None, **self.options)

        for i in range(10):
            username = 'user{}'.format(i)
            User.objects.create_user(username, username + '@example.com',
                                     username + 'password')

    def test_init(self):
        # First argument is request
        with self.assertRaises(TypeError):
            BaseWidget()

        # Init options
        self.assertEqual(self.widget0.init_options, self.options)

    def test_template_name(self):
        # No template_name
        with self.assertRaises(AssertionError):
            self.widget0.get_template_name()

        # Simple test
        self.widget0.template_name_prefix = 'prefix'
        self.widget0.template_name = 'test.html'
        self.assertEqual(self.widget0.get_template_name(),
                         'prefix/test.html')

        # Slash test
        self.widget0.template_name_prefix = 'prefix/////'
        self.widget0.template_name = '//test.html'
        self.assertEqual(self.widget0.get_template_name(),
                         'prefix/test.html')

    def test_queryset(self):
        # No queryset was provided
        with self.assertRaises(ImproperlyConfigured):
            self.widget0.get_queryset()

        # Model is defined, queryset is NOT
        self.widget0.model = User
        self.assertItemsEqual(self.widget0.get_queryset(),
                              User._default_manager.all())

        # Both are defined
        self.widget0.queryset = User.objects.filter(username='user0')
        self.assertItemsEqual(self.widget0.get_queryset(),
                              User._default_manager.filter(username='user0'))

    def test_values(self):
        # Setup
        self.widget0.model = User
        self.widget0.limit_to = limit = 4

        # It's not a bound method or something
        self.assertIsInstance(self.widget0.values, QuerySet)

        # Limits values
        self.assertEqual(len(self.widget0.values), limit)

        # Drops limit
        self.widget1.model = User
        self.widget1.limit_to = None
        self.assertEqual(len(self.widget1.values), User.objects.count())


class ItemListTest(TestCase):
    # TODO: template test

    def setUp(self):
        self.widget = widgets.ItemList(request=None)

    def test_basic(self):
        # Required attributes
        self.assertIsNotNone(self.widget.template_name)
        self.assertIsNotNone(self.widget.empty_message)


class GroupTest(TestCase):
    def setUp(self):
        self.widget0 = widgets.ItemList(request=None)
        self.widget1 = widgets.ItemList(request=None)
        self.widget1.width = widgets.LARGE
        self.widget1.height = 300

    def test_empty_group(self):
        group = widgets.Group()

        # It's empty and immutable
        self.assertEqual(group.widgets, ())

        # __iter__ test
        self.assertItemsEqual(group, [])
        self.assertEqual(len(group), 0)

        # Attributes test
        self.assertEqual(group.get_id(), '')
        self.assertEqual(group.get_class(), '')
        self.assertEqual(group.get_attrs(), {})
        self.assertIsNone(group.get_width())
        self.assertIsNone(group.get_height())

    def test_nonempty_group(self):
        group = widgets.Group([self.widget0])

        # It's empty and immutable
        self.assertEqual(group.widgets, (self.widget0,))

        # __iter__
        self.assertItemsEqual(group, (self.widget0,))
        self.assertEqual(len(group), 1)

        # Attributes test
        self.assertEqual(group.get_id(), 'itemlist')
        self.assertEqual(group.get_class(), '')
        self.assertEqual(group.get_attrs(), {})
        self.assertEqual(group.get_width(), widgets.Widget.width)
        self.assertIsNone(group.get_height())

    def test_concatenation(self):
        group = (widgets.Group([self.widget0]) +
                 widgets.Group([self.widget1],
                               attrs={'class': 'clearfix', 'data-prop': '2'}))

        # It's empty and immutable
        self.assertEqual(group.widgets, (self.widget0, self.widget1))

        # __iter__
        self.assertItemsEqual(group, (self.widget0, self.widget1))
        self.assertEqual(len(group), 2)

        # Attributes test
        self.assertEqual(group.get_id(), 'itemlist_and_itemlist')
        self.assertEqual(group.get_class(), 'clearfix')
        self.assertEqual(group.get_attrs(), {'data-prop': '2'})
        self.assertEqual(group.get_width(), widgets.LARGE)
        self.assertEqual(group.get_height(), 300)

        # Unknown attr
        self.assertIsNone(group._get_size('length'))

        # Overwrite width
        self.assertEqual(widgets.Group(width=500).get_width(), 500)

        # test repr
        self.assertEqual(repr(group),
                         '<Group of widgets: {}>'
                         .format((self.widget0, self.widget1)))
