from __future__ import annotations
import requests


COINGECKO_SIMPLE = (
    "https://api.coingecko.com/api/v3/simple/price?"
    "ids=bitcoin&vs_currencies={vs}&include_24hr_change=true"
)


def get_btc_price(vs: str = "usd") -> dict:
    url = COINGECKO_SIMPLE.format(vs=vs)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    return {
        "price": float(j["bitcoin"][vs]),
        "change_24h": float(j["bitcoin"][f"{vs}_24h_change"]),
    }