def __getattr__(key):
    if key in {
        "ApplicationContent",
        "app_reverse",
        "app_reverse_lazy",
        "permalink",
        "UnpackTemplateResponse",
        "standalone",
        "unpack",
    }:
        from feincms.content.application import models

        return getattr(models, key)

    raise AttributeError("Unknown attribute '%s'" % key)
