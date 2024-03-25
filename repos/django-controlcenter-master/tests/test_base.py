from controlcenter.base import BaseModel

from . import TestCase


class BaseModelTest(TestCase):
    def setUp(self):
        class NoTitleModel(BaseModel):
            pass

        class TitleModel(BaseModel):
            title = 'My Model'

        self.no_title = NoTitleModel()
        self.title = TitleModel()

    def test_no_title(self):
        self.assertEqual(self.no_title.__name__, 'NoTitleModel')
        self.assertEqual(self.no_title.slug, 'notitlemodel')
        self.assertEqual(self.no_title.title, 'No title model')

    def test_with_title(self):
        self.assertEqual(self.title.__name__, 'TitleModel')
        self.assertEqual(self.title.slug, 'titlemodel')
        self.assertEqual(self.title.title, 'My Model')

    def test_str_method(self):
        self.assertEqual(str(self.no_title), 'NoTitleModel')
        self.assertEqual(str(self.title), 'TitleModel')
