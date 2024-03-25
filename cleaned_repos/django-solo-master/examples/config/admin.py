from config.models import SiteConfiguration
from django.contrib import admin
from solo.admin import SingletonModelAdmin

admin.site.register(SiteConfiguration, SingletonModelAdmin)
