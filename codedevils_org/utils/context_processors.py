from django.conf import settings


def settings_context(_request):
    return {"settings": settings}


def language_path_context(_request):
    """Removes the language from the path"""
    path: str = _request.path
    try:
        return {"no_lang_path": path.split("/", 2)[2]}
    except:  # noqa: E722
        return {}
