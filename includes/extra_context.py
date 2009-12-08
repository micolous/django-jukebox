"""
These are extra context processors that add extra things to the global
template context. Make -sure- not to add anything here unless it's absolutely
necessary, anything here is used on every single page load. This can cause
severe performance degradation in the case of a query.
"""
from django.conf import settings

def common_urls(request):
    """
    Populates some other common URLs.
    """
    return {
        'YUI_URL': settings.YUI_URL,
    }