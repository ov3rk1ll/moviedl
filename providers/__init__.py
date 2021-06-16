from .fbox import FBOX_SLUG, fetcher as fbox_fetcher
from .watchseries import WATCHSERIES_SLUG, fetcher as watchseries_fetcher

current_providers = {
    'fbox': {
        'matcher': FBOX_SLUG,
        'fetcher': fbox_fetcher,
    },
    'twistmoe': {
        'matcher': WATCHSERIES_SLUG,
        'fetcher': watchseries_fetcher,
    }
}

def get_provider(url):
    for provider, provider_data in list(current_providers.items()):
        if provider_data.get('matcher').match(url):
            return provider, provider_data
        
def get_appropriate(session, url, check=lambda *args: True):
    provider_name, provider = get_provider(url)
    return provider.get('fetcher', lambda s, u, c: [])(session, url, check)