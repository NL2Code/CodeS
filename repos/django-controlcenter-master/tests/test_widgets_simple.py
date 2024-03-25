from controlcenter.widgets.contrib import simple

from . import TestCase


class ValueListTest(TestCase):
    def setUp(self):
        self.widget = ExampleValueList(request=None)

    def test_basic(self):
        self.assertIsNotNone(self.widget.template_name)

    def test_default_not_sortable(self):
        self.assertFalse(self.widget.sortable)

    def test_get_data(self):
        self.assertItemsEqual(self.widget.items(), ['Label 1', 'Label 2'])


class KeyValueListTest(TestCase):
    def setUp(self):
        self.widget = ExampleKeyValueList(request=None)

    def test_basic(self):
        self.assertIsNotNone(self.widget.template_name)

    def test_default_not_sortable(self):
        self.assertFalse(self.widget.sortable)

    def test_get_data(self):
        self.assertItemsEqual(
            self.widget.items(),
            {'Key 1': 'Value 1', 'Key 2': 'Value 2'}.items(),
        )


class ExampleValueList(simple.ValueList):
    title = 'Value list widget'

    def get_data(self):
        return ['Label 1', 'Label 2']


class ExampleKeyValueList(simple.KeyValueList):
    title = 'Key-value list widget'

    def get_data(self):
        return {'Key 1': 'Value 1', 'Key 2': 'Value 2'}
