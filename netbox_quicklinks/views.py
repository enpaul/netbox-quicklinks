import django.views.generic
import django.shortcuts
import django.conf
import django.http
import importlib

from netbox_quicklinks import __about__


class QuickLinkView(django.views.generic.View):

    def get(self, request, category: str, value: str):
        try:
            config = django.conf.settings.PLUGINS_CONFIG[__about__.__namespace__]["quick_links"][category]
        except KeyError as err:
            raise django.http.Http404(f"No quick link named {err} is configured") from None
        
        module_name = ".".join(config["attribute"].split(".")[:-2])
        model_name = config["attribute"].split(".")[-2]
        field_name = config["attribute"].split(".")[-1]
        is_case_sensitive = config.get("case_sensitive", True)

        try:
            model = getattr(importlib.import_module(module_name), model_name)
        except ImportError as err:
            raise RuntimeError(f"Configuration error: quick link '{category}' sepcifies non-existent module '{module_name}'") from err
        except AttributeError as err:
            raise RuntimeError(f"Configuration error: quick link '{category}' specifies a non-existent model '{module_name}.{field_name}'") from err

        try:
            query_type = "exact" if is_case_sensitive else "iexact"
            target = model.objects.get(**{f"{field_name}__{query_type}": value})
            return django.shortcuts.redirect(target)

        except model.DoesNotExist:
            raise django.http.Http404(f"No {model_name} with {field_name} '{value}' found")
        
        except model.MultipleObjectsReturned:
            # TODO: Add support for redirecting to search page when multiple results are found
            raise RuntimeError(f"Multiple {model_name}s found with {field_name} '{value}'")

        

