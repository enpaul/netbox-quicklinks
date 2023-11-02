"""Configure URL registration for the plugin"""
import django.conf
import django.urls

from netbox_quicklinks import __about__
from netbox_quicklinks import views


# Magic variable name
#
# See: https://docs.netbox.dev/en/stable/plugins/development/views/#url-registration
urlpatterns = [
    django.urls.path(
        "<str:category>/<str:value>", views.QuickLinkView.as_view(), name="quick-link"
    )
]
