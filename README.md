# netbox-quicklinks

Plugin for [Netbox](https://netbox.dev/) that adds support for quick links based on unique
item values

## Introduction

This plugin adds a very simple URL shim into Netbox which allows users to link directly to
a device with a known parameter (for example the name or serial number) without knowing
the Netbox ID. This is solve the very specific problem of creating permalinks in places
that aren't easily updated (such as un-automated documentation or physical labels).

For example, maybe we have a server named `svr01` in our rack. The physical server is old
and gets replaced with a newer generation of hardware. For lifecycle management reason I
want to decomission the existing device with Netbox ID 1234 and create a brand new device
with Netbox ID 4321. When I make this change, any place that I have a link to `svr01` as
`https://netbox.example.com/dcim/devices/1234/` will still point to the old device. I
could add a note to the old device that it's been replaced and the new one is located at
`https://netbox.example.com/dcim/devices/4321/`, but it'd be more convenient if I could
permalink directly to `svr01` regardless of what device currently holds that name.

This is the functionality that this plugin adds.

## Configuration

The `quick_links` parameter creates a map of link aliases to a configured fully quallified
field attribute. For example:

```
PLUGINS_CONFIG = {
    "netbox_quicklinks": {
        "quick_links": {
            "dev": {
                "field": "dcim.models.Device.name",
                "case_sensitive": True,
            },
        }
    }
}
```

This configuration allows the URL `https://netbox.example.com/plugins/links/dev/svr01` to
redirect to the native URL for the device with the name `svr01` (which may be, for
example, `https://netbox.example.com/dicm/devices/1234/`). The map key (i.e. `dev` in the
example above) defines the URL namespace under `links/` that the redirect will be
available under. Under each quick link entry are the below settings:

- The value of the `attribute` key defines the model attribute that the lookup will query
  against
- The boolean under the `case_sensitive` key defines whether the lookup is done with case
  sensitive values or not

### Adding quick links to the UI

It may be desirable to expose the configured quick links within the UI so that users can
easily copy them. This can be easily acheived using the
[Custom Links](https://docs.netbox.dev/en/stable/customization/custom-links/) feature.

To do this, create a new custom link with the Content Type set to the object defined in
the plugin config. Then set the Link URL to
`/plugins/links/<quick_link entry>/{{ object.<field> }}` where `<quick_link entry>` is the
key of the config under `PLUGINS_CONFIG['netbox_quicklinks']['quick_links']` and `<field>`
is the field configured under
`PLUGINS_CONFIG['netbox_quicklinks']['quick_links'][<quick_link entry>]['field']`.

For example, to create a quick link for the configuration entry `dev` shown above in the
[Configuration](#configuration) section, you would create a custom link with a Content
Type of `DCIM > Device` and a Link URL of `/plugins/links/dev/{{ object.name }}`.

## Limitations

- This plugin does not support complex queries or redirects. For example, while you can
  create an alias for IP addresses (using `"field": "ipam.models.IPAddress.address"`) this
  can only link to the IP Address object itself, there is no support for redirecting to
  the device that is assigned the IP.
- Netbox makes no guarantee about the uniqueness of any field not noted as such. It is
  possible to configure quick links based on fields that may match multiple objects, in
  which case an error will be raised.

## Developer Documentation

All project contributors and participants are expected to adhere to the
[Contributor Covenant Code of Conduct, v2](CODE_OF_CONDUCT.md)
([external link](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)).

The `main` branch has the latest (and potentially unstable) changes. The stable releases
are tracked on [Github](https://github.com/enpaul/netbox-quicklinks/releases),
[PyPi](https://pypi.org/project/netbox-quicklinks/#history), and in the
[Changelog](CHANGELOG.md).

- To report a bug, request a feature, or ask for assistance, please
  [open an issue on the Github repository](https://github.com/enpaul/netbox-quicklinks/issues/new).
- To report a security concern or code of conduct violation, please contact the project
  author directly at **‌me \[at‌\] enp dot‎ ‌one**.
- To submit an update, please
  [fork the repository](https://docs.github.com/en/enterprise/2.20/user/github/getting-started-with-github/fork-a-repo)
  and [open a pull request](https://github.com/enpaul/netbox-quicklinks/compare).

Developing this project requires [Python 3.11+](https://www.python.org/downloads/) and
[Poetry 1.5](https://python-poetry.org/docs/#installation) or later. GNU Make can
optionally be used to quickly setup a local development environment using `make dev`, but
this is not required. See `make help` for other available targets.

In addition, developers will require a development installation of Netbox. See setup
instructions
[here](https://github.com/netbox-community/netbox-plugin-tutorial/blob/main/tutorial/step01-initial-setup.md)
for getting started.

> ℹ️ **Note:** The pre-commit hooks require dependencies in the Poetry environment to run.
> To make a commit with the pre-commit hooks, you will need to run `poetry run git commit`
> or, alternatively,
> [launch an environment shell](https://python-poetry.org/docs/cli/#shell).
