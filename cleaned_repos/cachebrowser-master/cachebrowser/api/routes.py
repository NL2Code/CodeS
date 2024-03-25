from cachebrowser.api.handlers.bootstrap import (
    add_cdn,
    add_host,
    delete_host,
    get_cdns,
    get_hosts,
)
from cachebrowser.api.handlers.process import close, ping
from cachebrowser.api.handlers.website import (
    disable_website,
    enable_website,
    is_website_enabled,
)

routes = [
    ("/close", close),
    ("/ping", ping),
    ("/hosts", get_hosts),
    ("/hosts/delete", delete_host),
    ("/hosts/add", add_host),
    ("/cdns", get_cdns),
    ("/cdns/add", add_cdn),
    ("/website/enabled", is_website_enabled),
    ("/website/enable", enable_website),
    ("/website/disable", disable_website),
]
