import collections
import json

from django import VERSION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from controlcenter import app_settings, widgets
from controlcenter.templatetags.controlcenter_tags import (
    _method_prop,
    attrlabel,
    attrvalue,
    change_url,
    changelist_url,
    external_link,
    is_sequence,
    jsonify,
)
from test_models import TestUser0, TestUser1

from . import TestCase


class SimpleTagsTest(TestCase):
    def test_jsonify(self):
        data = {'a': None, 'b': 0}
        json_data = jsonify(data)

        # Marked safe
        self.assertTrue(hasattr(json_data, '__html__'))
        self.assertEqual(json_data, json.dumps(data))

    def test_is_sequence(self):
        self.assertTrue(is_sequence(list()))
        self.assertTrue(is_sequence(tuple()))
        self.assertFalse(is_sequence(dict()))
        self.assertFalse(is_sequence(User()))

    def test_changelist_url(self):
        widget = widgets.ItemList(request=None)
        widget.changelist_url = 'test'

        # Original
        admin_changelist_url = '/admin/auth/user/'

        # String test
        self.assertEqual(changelist_url(widget), 'test')

        # Model test
        widget.changelist_url = User
        self.assertEqual(changelist_url(widget),
                         admin_changelist_url + '')

        # Tuple with params test
        widget.changelist_url = (User, {'username__exact': 'user0'})
        self.assertEqual(changelist_url(widget),
                         admin_changelist_url + '?username__exact=user0')

        # Same with string no question sign
        widget.changelist_url = (User, 'username__exact=user0')
        self.assertEqual(changelist_url(widget),
                         admin_changelist_url + '?username__exact=user0')

        # Same with question sign
        widget.changelist_url = (User, '?username__exact=user0')
        self.assertEqual(changelist_url(widget),
                         admin_changelist_url + '?username__exact=user0')

        # Asserts first item is a Model
        widget.changelist_url = (None, {'username__exact': 'user0'})
        with self.assertRaises(AssertionError):
            self.assertEqual(changelist_url(widget), admin_changelist_url)

        # Asserts last items is either basestring or dict
        widget.changelist_url = (User, None)
        with self.assertRaises(AssertionError):
            self.assertEqual(changelist_url(widget), admin_changelist_url)

    def test_method_prop(self):
        class Test(object):
            foo = True

            def bar(self):
                pass
            bar.allow_tags = True

            def baz(self):
                pass
            baz.allow_tags = False

            def egg(self):
                pass

        test = Test()

        # Attribute is not callable
        self.assertIsNone(_method_prop(test, 'foo', 'allow_tags'))

        # Has the property
        self.assertEqual(_method_prop(test, 'bar', 'allow_tags'), True)

        # Has it but it's False
        self.assertFalse(_method_prop(test, 'baz', 'allow_tags'))

        # Doesn't have
        self.assertIsNone(_method_prop(test, 'egg', 'allow_tags'))

        # Doesn't exist
        self.assertIsNone(_method_prop(test, 'doesnt_exist', 'allow_tags'))


class AttrTagsTest(TestCase):
    def setUp(self):
        class TestUserWidget0(widgets.ItemList):
            model = TestUser0
            list_display = ('foo', 'egg')

            # Should override models method
            def foo(self, obj):
                return 'new foo value'
            foo.short_description = 'new foo label'

            # Doesn't have description
            def bar(self, obj):
                return 'new bar value'

            def allows_tags(self, obj):
                return '<br>'
            allows_tags.allow_tags = True

            def no_tags(self, obj):
                return '<br>'

        class TestUserWidget1(TestUserWidget0):
            list_display = None

        class TestUserWidget2(TestUserWidget0):
            list_display = ((app_settings.SHARP, ) +
                            TestUserWidget0.list_display)

        class TestUserWidget3(TestUserWidget2):
            model = TestUser1

        self.user0 = TestUser0(username='user0')
        self.widget0 = TestUserWidget0(request=None)
        self.widget1 = TestUserWidget1(request=None)
        self.widget2 = TestUserWidget2(request=None)
        self.widget3 = TestUserWidget3(request=None)

        self.mapping = {'baz': 'mapping baz'}
        self.sequence = ['foo value', 'egg value']
        self.namedtuple = collections.namedtuple('User', ['egg'])('egg value')

    def test_attrlabel(self):
        # Widget overrides
        self.assertEqual(attrlabel(self.widget0, 'foo'), 'new foo label')

        # Widget's has no description, takes model's one
        self.assertEqual(attrlabel(self.widget0, 'bar'), 'original bar label')

        # Empty description
        self.assertEqual(attrlabel(self.widget0, 'baz'), '')

        # Field's verbose name
        self.assertEqual(attrlabel(self.widget0, 'test_field'), 'My title')

        # No description found
        self.assertEqual(attrlabel(self.widget0, 'egg'), 'egg')

        # No attribute found
        self.assertEqual(attrlabel(self.widget0, 'unknown'), 'unknown')

        # Pk field
        self.assertEqual(attrlabel(self.widget0, 'id'), 'ID')
        self.assertEqual(attrlabel(self.widget0, 'pk'), 'ID')

        # Id is not defined
        self.assertEqual(attrlabel(self.widget3, 'id'), 'id')
        self.assertEqual(attrlabel(self.widget3, 'pk'), 'primary')

    def test_attrvalue(self):
        # New method
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'foo'), 'new foo value')

        # Old method
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'egg'), 'original egg value')

        # Allow tags test
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'allows_tags'), '<br>')
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'no_tags'), '&lt;br&gt;')

        # Attribute test
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'username'), 'user0')

        # 1) if method wasn't found in widget,
        #    doesn't pass instance to it's method
        # 2) returns empty value because gots None
        self.assertEqual(attrvalue(self.widget0, self.user0, 'baz'), '')

        # No attribute found -- empty value
        self.assertEqual(
            attrvalue(self.widget0, self.user0, 'unknown'), '')

        # Mapping test
        self.assertEqual(
            attrvalue(self.widget0, self.mapping, 'baz'), 'mapping baz')

        # Key not found, not KeyError
        self.assertEqual(
            attrvalue(self.widget0, self.mapping, 'unknown'), '')

        # Requires list_display to map it to values
        self.assertEqual(
            attrvalue(self.widget0, self.sequence, 'egg'), 'egg value')
        self.assertEqual(attrvalue(self.widget1, self.sequence, 'egg'), '')

        # Namedtuple doesn't require it
        # with list_display
        self.assertEqual(
            attrvalue(self.widget0, self.namedtuple, 'egg'), 'egg value')
        # without list_display
        self.assertEqual(
            attrvalue(self.widget1, self.namedtuple, 'egg'), 'egg value')

        # Sharp test
        self.assertEqual(
            attrvalue(self.widget2, self.sequence, 'egg'), 'egg value')

        # IndexError test
        self.assertEqual(
            attrvalue(self.widget2, self.sequence[:-1], 'egg'), '')


class ChangeurlTest(TestCase):
    def setUp(self):
        for i in range(10):
            username = 'user{}'.format(i)
            User.objects.create_user(username, username + '@example.com',
                                     username + 'password')

        self.obj = User.objects.first()
        self.obj_url = '/admin/auth/user/{}/'.format(self.obj.pk)
        if VERSION > (1, 9):
            self.obj_url += 'change/'

        # Model queryset
        class ModelQuerySet(widgets.ItemList):
            queryset = User.objects.all()

        # Deferred queryset
        class DeferredQuerySet(widgets.ItemList):
            queryset = User.objects.defer('email')

        # Dict
        class ValuesDict(widgets.ItemList):
            queryset = User.objects.values('pk', 'email')

        # List
        class ValuesList(widgets.ItemList):
            queryset = User.objects.values_list('pk', 'email')

        # List
        class ValuesListNoPk(widgets.ItemList):
            queryset = User.objects.values_list('email')

        # Namedtuple
        class NamedtupleList(ValuesList):
            klass = collections.namedtuple('User', 'pk email')

            def values(self):
                vals = super(NamedtupleList, self).values
                return [self.klass._make(x) for x in vals]

        self.widgets = [
            ModelQuerySet,
            DeferredQuerySet,
            ValuesDict,
            ValuesList,
            NamedtupleList,
        ]

        for widget in self.widgets:
            setattr(self, widget.__name__, widget)

    def equal(self, klass, value):
        widget = klass(request=None)
        self.assertEqual(change_url(widget, widget.values[0]), value)

    def test_non_registered(self):
        # It's not registered so no reverse is possible
        class NonRegisteredModel(widgets.ItemList):
            queryset = ContentType.objects.all()

        self.equal(NonRegisteredModel, None)

    def test_no_model(self):
        # Model queryset + Deferred
        self.equal(self.ModelQuerySet, self.obj_url)
        self.equal(self.DeferredQuerySet, self.obj_url)

        # widget.model is not defined, so it can't build
        # change_url from Dict, List, Namedtuple
        self.equal(self.ValuesDict, None)
        self.equal(self.ValuesList, None)
        self.equal(self.NamedtupleList, None)

    def test_with_model(self):
        for widget in self.widgets:
            class Widget(widget):
                model = User

            if widget is self.ValuesList:
                # No widget.values_list_defined
                self.equal(Widget, None)
            else:
                self.equal(Widget, self.obj_url)

    def test_with_model_and_list_display(self):
        for widget in self.widgets:
            class Widget(widget):
                model = User
                list_display = (app_settings.SHARP, 'pk', 'email')

            # Need pk to build url for ValuesList
            self.equal(Widget, self.obj_url)

            class IdWidget(Widget):
                list_display = ('id', 'email')

            # Alias test pk == id and also no sharp sign in list_display
            self.equal(IdWidget, self.obj_url)

    def test_no_pk(self):
        class NoPkList(self.NamedtupleList):
            klass = collections.namedtuple('User', 'email')
            model = User
            queryset = model.objects.values_list('email')

        self.equal(NoPkList, None)


class ExternalLinkTest(TestCase):
    def test_no_label(self):
        self.assertEqual(
            external_link('http://example.com'),
            '<a href="http://example.com" target="_blank" '
            'rel="noreferrer" rel="noopener">http://example.com</a>',
        )

    def test_with_label(self):
        self.assertEqual(
            external_link('http://example.com', 'my-example-link'),
            '<a href="http://example.com" target="_blank" '
            'rel="noreferrer" rel="noopener">my-example-link</a>',
        )
