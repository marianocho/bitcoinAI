import streamlit as st
from src.data_sources.rss import fetch_headlines
from src.features.indicators import moving_average, educational_signal
from src.agent.summarize import llm_summary
from src.report.daily import load_market_history

cfg = SETTINGS.yaml()

st.set_page_config(page_title="Agente Bitcoin (MVP)", page_icon="₿", layout="centered")
st.title("Agente Bitcoin — MVP Educacional")

# 1) Coleta ao vivo (não persiste — isso fica a cargo do script diário)
with st.spinner("Coletando preço e manchetes..."):
    mkt = get_btc_price(cfg["market"]["vs_currency"]) # {price, change_24h}
    headlines_items = fetch_headlines(cfg["news"]["feeds"], limit=5)
    headlines_texts = [x["title"] for x in headlines_items]

st.metric("Preço BTC (USD)", f"${mkt['price']:.2f}", f"{mkt['change_24h']:+.2f}% / 24h")

with st.expander("Manchetes de hoje"):
    for it in headlines_items:
        st.write(f"- **{it['source']}** — [{it['title']}]({it['link']})")

# 2) Histórico local para média móvel
market_csv = SETTINGS.data_dir / "market_prices.csv"
df = load_market_history(market_csv)
if df.empty:
    st.info("Ainda sem histórico salvo. Rode `python scripts/run_daily.py` 1x por dia para construir o CSV.")
else:
    df["ma30"] = moving_average(df["price"], window=cfg["app"]["signal"]["ma_window"]) # 30 por padrão
    st.line_chart(df.set_index("ts")["price"], height=200)
    st.line_chart(df.set_index("ts")["ma30"], height=200)
    last_ma = float(df["ma30"].iloc[-1]) if not pd.isna(df["ma30"].iloc[-1]) else float("nan")
else_ma = float("nan")

# 3) Sinal educacional
last_ma = df["ma30"].iloc[-1] if not df.empty else float("nan")
label, reason = educational_signal(
    price=mkt["price"],
    ma=float(last_ma) if not pd.isna(last_ma) else float("nan"),
    bullish_threshold=cfg["app"]["signal"]["bullish_threshold"],
    bearish_threshold=cfg["app"]["signal"]["bearish_threshold"],
)

st.subheader("Sinal educacional")
st.write(label)
st.caption(reason)

# 4) Explicação do agente (LLM se disponível; senão heurístico)
with st.spinner("Gerando explicação educativa..."):
    explanation = llm_summary(
        price=mkt["price"],
        change=mkt["change_24h"],
        headlines=headlines_texts,
        lang=SETTINGS.app_lang,
    )

st.subheader("Resumo do agente")
st.write(explanation)

st.divider()
st.caption(
    "MVP educativo. Não é recomendação financeira. Dados gratuitos (CoinGecko + RSS). "
    "Histórico local em data/ (via scripts/run_daily.py)."
)