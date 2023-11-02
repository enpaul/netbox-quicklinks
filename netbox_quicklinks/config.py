"""Define the required ``PluginConfig`` class and set parameters

See here for more info: https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig
"""
import extras.plugins

from netbox_quicklinks import __about__


class NetboxQuickLinksConfig(
    extras.plugins.PluginConfig
):  # pylint: disable=too-few-public-methods
    """Configuration for the Netbox-Quicklinks plugin"""

    name = __about__.__namespace__
    verbose_name = "Netbox Quick Links"
    description = __about__.__summary__
    version = __about__.__version__
    base_url = "links"
    min_version = "3.6"
    default_settings = {
        "quick_links": {
            "seriral": {
                "field": "dcim.models.Device.serial",
                "case_sensitive": True,
            },
            "dev": {
                "field": "dcim.models.Device.name",
                "case_sensitive": False,
            },
        },
    }
