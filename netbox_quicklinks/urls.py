import django.conf
import django.urls

from netbox_quicklinks import __about__
from netbox_quicklinks import views


urlpatterns = [
    django.urls.path(
        "<str:category>/<str:value>", views.QuickLinkView.as_view(), name="quick-link"
    )
]
