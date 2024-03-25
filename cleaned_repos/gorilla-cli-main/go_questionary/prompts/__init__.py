from go_questionary.prompts import (
    autocomplete,
    checkbox,
    confirm,
    password,
    path,
    rawselect,
    select,
    text,
)

AVAILABLE_PROMPTS = {
    "autocomplete": autocomplete.autocomplete,
    "confirm": confirm.confirm,
    "text": text.text,
    "select": select.select,
    "rawselect": rawselect.rawselect,
    "password": password.password,
    "checkbox": checkbox.checkbox,
    "path": path.path,
    "list": select.select,
    "rawlist": rawselect.rawselect,
    "input": text.text,
}


def prompt_by_name(name):
    return AVAILABLE_PROMPTS.get(name)
