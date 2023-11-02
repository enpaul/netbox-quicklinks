"""Define the lookup and redirection view for the plugin"""
import importlib

import django.conf
import django.http
import django.shortcuts
import django.views.generic

from netbox_quicklinks import __about__


class QuickLinkView(
    django.views.generic.View
):  # pylint: disable=too-few-public-methods
    """Handle a plugin request by looking up the requested object and redirecting

    This class is the full logic of the plugin. It responds to queries specified in the
    application configuration and looks up a requested object (handling potential errors)
    and then redirects the client to the actual object page for the discovered object.

    The class only handles ``GET`` requests.
    """

    def get(
        self, request, category: str, value: str
    ):  # pylint: disable=unused-argument
        """Handle a ``GET`` request

        :param request: Unused, passed by the Django handler
        :param category: The entry in ``PLUGINS_CONFIG`` that will handle the lookup
        :param value: The value to be queried against the model configured in ``PLUGINS_CONFIG``
        :returns: Redirect to object discovered from ``category`` and ``value``
        """
        try:
            config = django.conf.settings.PLUGINS_CONFIG[__about__.__namespace__][
                "quick_links"
            ][category]
        except KeyError as err:
            raise django.http.Http404(
                f"No quick link named {err} is configured"
            ) from None

        # TODO: handle a keyerror here
        module_name = ".".join(config["field"].split(".")[:-2])
        model_name = config["field"].split(".")[-2]
        field_name = config["field"].split(".")[-1]
        is_case_sensitive = config.get("case_sensitive", True)

        try:
            model = getattr(importlib.import_module(module_name), model_name)
        except ImportError as err:
            raise RuntimeError(
                f"Configuration error: quick link '{category}' sepcifies non-existent module '{module_name}'"
            ) from err
        except AttributeError as err:
            raise RuntimeError(
                f"Configuration error: quick link '{category}' specifies a non-existent model '{module_name}.{field_name}'"
            ) from err

        try:
            query_type = "exact" if is_case_sensitive else "iexact"
            target = model.objects.get(**{f"{field_name}__{query_type}": value})
            return django.shortcuts.redirect(target)

        except model.DoesNotExist:
            raise django.http.Http404(
                f"No {model_name} with {field_name} '{value}' found"
            ) from None

        except model.MultipleObjectsReturned as err:
            # TODO: Add support for redirecting to search page when multiple results are found
            raise RuntimeError(
                f"Multiple {model_name}s found with {field_name} '{value}'"
            ) from err
