from scripts import settings, streaming

queries = {
    "ETH": ["ETH", "Ethereum"],
    "LTC": ["LTC", "Litecoin"],
    "BTC": ["BTC", "Bitcoin"],
    "XRP": ["XRP", "Ripple"],
    "XLM": ["XLM", "Stellar"],
}

# Aggregate volume and sentiment every 15 minutes
refresh = 15 * 60

streaming.streamer(settings.credentials, queries, refresh, sentiment=True, debug=True)
