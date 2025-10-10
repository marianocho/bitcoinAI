from __future__ import annotations
import pandas as pd

# Indicadores simples para MVP
def moving_average(prices: pd.Series, window: int = 30) -> pd.Series:
    return prices.rolling(window).mean()

def educational_signal(price: float, ma: float, bullish_threshold=0.0, bearish_threshold=0.0) -> tuple[str, str]:
    # Regra didática: acima da MA → otimista; abaixo → cautela.
    # thresholds permitem futurar refinamentos.
    if pd.isna(ma):
        return ("Neutro", "Sem histórico suficiente para média móvel.")
    diff = price - ma
    if diff > bullish_threshold:
        return ("📈 Levemente otimista", f"Preço atual acima da média ({price:.2f} > {ma:.2f}).")
    elif diff < bearish_threshold:
        return ("⚠️ Cautela", f"Preço atual abaixo da média ({price:.2f} < {ma:.2f}).")
    return ("Neutro", "Preço próximo da média móvel; aguarde confirmação.")