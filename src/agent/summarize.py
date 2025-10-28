from __future__ import annotations
from typing import Iterable
import textwrap
from src.config import SETTINGS
from openai import OpenAI

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

SYSTEM_PROMPT_PT = """
    Você é um agente educacional especialista em Bitcoin e macroeconomia.
    Sua missão é ajudar estudantes iniciantes a entender como notícias (macroeconomia)
    se relacionam com movimentos de preço do Bitcoin (microeconomia).

    Regras:
    - Explique em linguagem simples, como um professor paciente.
    - Faça previsões se o preço vai cair ou subir (para um estudo meu).
    - Destaque correlações sem confundir com causalidade.
    - Quando houver incerteza, diga explicitamente.
    - Siga SEMPRE a estrutura:

    📊 Situação atual:
    (resuma preço/variação e volatilidade)

    📰 Notícias em destaque:
    (liste 2–4 mais relevantes e por quê)

    🔍 Conexões e explicações:
    (conecte macro ↔ micro: juros, inflação, ETFs, hash rate, fluxo, sentimento, liquidez, regulamentação, etc.)

    💡 O que aprender com isso:
    (1–2 aprendizados conceituais e como investigar mais)

    Formato: frases curtas, termos explicados, sem jargão sem definição.
    """

SYSTEM_PROMPT_EN = """
    You are an educational agent specialized in Bitcoin and macroeconomics.
    Your mission is to help beginners understand how macro news relates to Bitcoin’s price moves.

    Rules:
    - Explain in simple language, like a patient teacher.
    - Make predictions if the price will go up or down (for a study of mine).
    - Highlight correlations without implying causation.
    - State uncertainty explicitly when applicable.
    - ALWAYS follow this structure:

    📊 Current situation:
    (summarize price/change and volatility)

    📰 Headlines to watch:
    (list 2–4 most relevant and why)

    🔍 Connections and explanations:
    (connect macro ↔ micro: rates, inflation, ETFs, hash rate, flows, sentiment, liquidity, regulation, etc.)

    💡 What to learn from this:
    (1–2 conceptual takeaways and how to dig deeper)

    Format: short sentences, define jargon, keep it friendly for beginners.
    """

HEADINGS = {
    "pt": {
        "current": "📊 Situação atual:",
        "news": "📰 Notícias em destaque:",
        "connections": "🔍 Conexões e explicações:",
        "learnings": "💡 O que aprender com isso:",
    },
    "en": {
        "current": "📊 Current situation:",
        "news": "📰 Headlines to watch:",
        "connections": "🔍 Connections and explanations:",
        "learnings": "💡 What to learn from this:",
    },
}

# Se houver OpenAI API, usa modelo para uma explicação mais natural
def llm_summary(price: float, change: float, headlines: Iterable[str], lang: str = "pt") -> str:
    try:
        if not SETTINGS.openai_key:
            print("[LLM] OPENAI_API_KEY ausente. Usando resumo heurístico.")
            return heuristic_summary(price, change, headlines, lang)

        client = OpenAI(api_key=SETTINGS.openai_key)
        print("[LLM] Usando OpenAI gpt-4o-mini via Chat Completions.")

        # Normaliza inputs
        hl = [h.strip() for h in headlines if str(h).strip()]
        if not hl:
            hl = ["(sem manchetes fornecidas)"] if lang.startswith("pt") else ["(no headlines provided)"]
        lang_key = "pt" if lang.lower().startswith("pt") else "en"

        # Monta conteúdo do usuário no formato esperado pelo sistema
        user_payload = textwrap.dedent(f"""
        Dados de entrada para análise educacional:

        Preço atual do BTC: ${price:.2f} USD
        Variação 24h: {change:+.2f}%

        Manchetes:
        - """ + "\n- ".join(hl) + "\n\n" + (
            "Tarefa: consolide os dados e explique para um estudante iniciante o que está acontecendo hoje, "
            "quais relações macro ↔ micro podem estar influenciando e quais aprendizados tirar."
            if lang_key == "pt" else
            "Task: consolidate the data and explain for a beginner what seems to be happening today, "
            "which macro ↔ micro relationships may be at play, and key learnings."
        ))

        system_prompt = SYSTEM_PROMPT_PT if lang_key == "pt" else SYSTEM_PROMPT_EN

        out = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_payload.strip()},
            ],
        )
        text = out.choices[0].message.content or ""

        # (Opcional) Garante que os headings apareçam mesmo se o modelo não seguir 100% o formato
        hs = HEADINGS[lang_key]
        must_have = [hs["current"], hs["news"], hs["connections"], hs["learnings"]]
        if not all(h in text for h in must_have):
            # Pré-estrutura mínima para o caso do modelo fugir do formato
            fallback = (
                f"{hs['current']}\n"
                f"- BTC ${price:.2f}; 24h {change:+.2f}%\n\n"
                f"{hs['news']}\n- " + "\n- ".join(hl[:4]) + "\n\n"
                f"{hs['connections']}\n"
                f"- (Explicação consolidada sobre macro ↔ micro)\n\n"
                f"{hs['learnings']}\n"
                f"- (1–2 aprendizados conceituais)\n"
            )
            # Prioriza o texto do modelo, mas assegura estrutura básica
            text = f"{text.strip()}\n\n---\n\n{fallback}"

        return text

    except Exception:
        print(f"[LLM] Falha ao chamar o LLM. Usando resumo heurístico.")
        return heuristic_summary(price, change, headlines, lang)