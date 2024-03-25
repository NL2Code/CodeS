# django-tui

Inspect and run Django Commands in a text-based user interface (TUI), built with [Textual](https://github.com/Textualize/textual) & [Trogon](https://github.com/Textualize/trogon).

------

## Features

- Run Django commands in a text-based user interface (TUI)
- Inspect Django configs, models, and more

## Installation

```console
pip install django-tui
```

Add `"django_tui"` to your `INSTALLED_APPS` setting in `settings.py` like this:


```python
INSTALLED_APPS = [
    ...,
    "django_tui",
]
```

Now you can run the TUI with:

```console
python manage.py tui
```