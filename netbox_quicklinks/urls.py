import django.urls
import django.conf

from netbox_quicklinks import __about__, views


urlpatterns = [
    django.urls.path("<str:category>/<str:value>", views.QuickLinkView.as_view(), name="quick-link")
]