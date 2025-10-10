# Agente Bitcoin — MVP Free

MVP educativo que coleta preço do BTC (CoinGecko) e manchetes (RSS), gera um sinal simples (MA30) e uma explicação diária (LLM opcional).

## Quickstart
1. Python 3.11+
2. `pip install -r requirements.txt`
3. **Rodar UI**: `streamlit run app/streamlit_app.py`
4. **Construir histórico**: agende `python scripts/run_daily.py` 1x/dia (cron, Task Scheduler)

## Estrutura
Veja o diagrama no cabeçalho deste repositório.

## Automação diária
- Linux/Mac (cron): `0 9 * * * /usr/bin/python /caminho/agent-bitcoin-mvp/scripts/run_daily.py`
- Windows: Agendador de Tarefas → ação executando `python scripts/run_daily.py` às 09:00.

## Aviso
Projeto **educacional**. Não fornece aconselhamento financeiro.