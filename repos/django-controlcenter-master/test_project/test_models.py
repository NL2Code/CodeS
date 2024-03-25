from django.db import models


class TestUser0(models.Model):
    username = models.CharField(max_length=255)
    test_field = models.CharField('My title', max_length=255)

    class Meta:
        app_label = 'controlcenter'

    def foo(self):
        return 'original foo value'
    foo.short_description = 'original foo label'

    def bar(self):
        return 'original bar value'
    bar.short_description = 'original bar label'

    def baz(self):
        pass
    baz.short_description = ''

    def egg(self):
        return 'original egg value'


class TestUser1(models.Model):
    primary = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)

    class Meta:
        app_label = 'controlcenter'
