from .models import SiteSettings


def site_settings(request):
    """Make SiteSettings available in every template as `site_settings`."""
    try:
        settings_obj = SiteSettings.objects.first()
        if not settings_obj:
            settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None
    return {"site_settings": settings_obj}
