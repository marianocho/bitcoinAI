from __future__ import annotations
from typing import Iterable
from src.config import SETTINGS

# Fallback simples caso não haja API key

def heuristic_summary(price: float, change: float, headlines: Iterable[str], lang: str = "pt") -> str:
    direction = "alta" if change >= 0 else "queda"
    heads = "\n".join(f"- {h}" for h in headlines)
    if lang == "pt":
        return (
            f"O Bitcoin está em {direction} de {change:+.2f}% nas últimas 24h.\n"
            f"Principais manchetes:\n{heads}\n"
            "Interpretação inicial: as manchetes ajudam a entender se o movimento de preço\n"
            "tem relação com fatores institucionais, regulação ou macro."
        )
    else:
        return (
            f"Bitcoin shows a {direction} of {change:+.2f}% in the last 24h.\n"
            f"Top headlines:\n{heads}\n"
            "Initial take: use headlines to gauge institutional, regulatory or macro drivers."
        )

# Se houver OpenAI API, usa modelo para uma explicação mais natural

def llm_summary(price: float, change: float, headlines: Iterable[str], lang: str = "pt") -> str:
    try:
        if not SETTINGS.openai_key:
            return heuristic_summary(price, change, headlines, lang)
        from openai import OpenAI
        client = OpenAI(api_key=SETTINGS.openai_key)
        prompt = (
            "Você é um educador em Bitcoin. Dado o preço e variação 24h, e as manchetes, "
            "explique em linguagem simples o que pode estar acontecendo hoje. "
            "Evite recomendações financeiras; foque em contexto e possíveis relações.\n\n"
            f"Preço atual: ${price:.2f}\nVariação 24h: {change:+.2f}%\n"
            f"Manchetes:\n- " + "\n- ".join(headlines)
        )
        out = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return out.choices[0].message.content
    except Exception:
        return heuristic_summary(price, change, headlines, lang)