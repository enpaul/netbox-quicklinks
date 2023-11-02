import extras.plugins

from netbox_quicklinks import __about__


class NetboxQuickLinksConfig(extras.plugins.PluginConfig):
    name = __about__.__namespace__
    verbose_name = "Netbox Quick Links"
    description = __about__.__summary__
    version = __about__.__version__
    base_url = "links"
    min_version = "3.6"
    default_settings = {
        "quick_links": {
            "seriral": {
                "attribute": "dcim.models.Device.serial",
                "case_sensitive": True,
            },
            "dev": {
                "attribute": "dcim.models.Device.name",
                "case_sensitive": False,
            },
        },
    }
