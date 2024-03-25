# django-admin-interface
django-admin-interface is a modern **responsive flat admin interface customizable by the admin itself**.

## Features
- Beautiful default **django-theme**
- Themes management and customization *(you can **customize admin title, logo and colors**)*
- Responsive
- Related modal *(instead of the old popup window)*
- Environment name/marker
- Language chooser
- Foldable apps *(accordions in the navigation bar)*
- Collapsible fieldsetscan have their initial state expanded instead of collapsed
- `NEW` Collapsible inlines
- `NEW` Tabbed fieldsets and inlines
- `NEW` List filter removal links
- `NEW` List filter highlight selected options
- List filter dropdown
- List filter sticky
- Form controls sticky *(pagination and save/delete buttons)*
- Compatibility / style optimizations for:
  - `django-ckeditor`
  - `django-dynamic-raw-id`
  - `django-json-widget`
  - `django-modeltranslation`
  - `django-rangefilter`
  - `django-streamfield`
  - `django-tabbed-admin`
  - `sorl-thumbnail`
- Translated in many languages: `de`, `es`, `fa`, `fr`, `it`, `pl`, `pt_BR`, `ru`, `tr`

### Optional features
To make a fieldset start expanded with a `Hide` button to collapse, add the class `"expanded"` to its classes:
```python
class MyModelAdmin(admin.ModelAdmin):
    # ...
    fieldsets = [
        ("Section title", {
            "classes": ("collapse", "expanded"),
            "fields": (...),
        }),
    ]
    # ...
```
