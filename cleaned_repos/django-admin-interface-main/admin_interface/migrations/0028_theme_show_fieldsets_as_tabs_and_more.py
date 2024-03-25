from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_interface", "0027_theme_list_filter_removal_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="show_fieldsets_as_tabs",
            field=models.BooleanField(
                default=False,
                verbose_name="fieldsets as tabs",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="show_inlines_as_tabs",
            field=models.BooleanField(
                default=False,
                verbose_name="inlines as tabs",
            ),
        ),
    ]
