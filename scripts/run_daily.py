from __future__ import annotations
from datetime import datetime, timezone
import pandas as pd
from pathlib import Path
from src.config import SETTINGS
from src.utils.io import append_csv
from src.data_sources.coingecko import get_btc_price
from src.data_sources.rss import fetch_headlines
from src.data_sources.feeds_loader import load_all_feeds, load_feeds_by_category

cfg = SETTINGS.yaml()

market_path = SETTINGS.data_dir / "market_prices.csv"
news_path = SETTINGS.data_dir / "news_raw.csv"

now = datetime.now(timezone.utc)

# 1) Preço BTC
mkt = get_btc_price(cfg["market"]["vs_currency"]) # {price, change_24h}
append_csv(market_path, pd.DataFrame([{
    "ts": now.isoformat(),
    "price": mkt["price"],
    "change_24h": mkt["change_24h"],
}]))

# 2) Notícias (headlines)
feeds_dir = SETTINGS.data_dir / "feeds"          # <— onde ficam os .txt
feeds = load_all_feeds(feeds_dir)                # <— lista plana de URLs
items = fetch_headlines(feeds, limit=5)
for it in items:
    it["ts"] = now.isoformat()
append_csv(news_path, pd.DataFrame(items))
