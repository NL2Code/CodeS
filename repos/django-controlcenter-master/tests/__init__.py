from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'assertItemsEqual'):
            self.assertItemsEqual = self.assertCountEqual
        super(TestCase, self).__init__(*args, **kwargs)
