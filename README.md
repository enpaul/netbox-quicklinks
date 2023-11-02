# netbox-quicklinks

Plugin for [Netbox](https://netbox.dev/) that adds support for quick links based on unique item values

## Configuration

The `quick_links` parameter creates a map of model aliases to a configured link attribute. For example:

```
PLUGINS_CONFIG = {
    "netbox_quicklinks": {
        "quick_links": {
            "dev": {
                "attribute": "dcim.Device.name",
                "case_sensitive": True,
            },
        }
    }
}
```

This configuration allows the URL `https://netbox.example.com/plugins/qlinks/dev/svr01` to redirect to the native URL
for the device with the name `svr01` (which may be, for example, `https://netbox.example.com/dicm/devices/1234/`). The map key (i.e. `dev` in the example above) defines the URL namespace under `qlinks/` that the redirect will be available under. Under each quick link entry are the below settings:

* The value of the `attribute` key defines the model attribute that the lookup will query against
* The boolean under the `case_sensitive` key defines whether the lookup is done with case sensitive values or not
* The boolean under the `error_on_duplicate` key defines the behavior if the expected unique attribute is not found unique; if `True` then the server will respond with [HTTP 409](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409), and if `False` then the client will be redirected to a search page showing all objects that match the request.

