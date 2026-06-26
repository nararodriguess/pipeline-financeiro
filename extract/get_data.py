import yfinance as yf
import requests
import pandas as pd
import schedule
import time
import json
from datetime import datetime
from pathlib import Path

ATIVOS_BR = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "WEGE3.SA", "MGLU3.SA"
]

CRIPTO = [
    "bitcoin", "ethereum", "solana",
]

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def coletar_acoes() -> list[dict]:
    registros = []
    timestamp = datetime.utcnow().isoformat()

    for ticker in ATIVOS_BR:
        try:
            ativo = yf.Ticker(ticker)
            info = ativo.fast_info

            preco_atual = info.last_price
            preco_aber = info.open
            preco_max = info.day_high
            preco_min = info.day_low
            volume = info.three_month_average_volume


            variacao_pct = (
                round((preco_atual - preco_aber) / preco_aber * 100, 2)
                if preco_aber else None
            )

            registros.append({
                "event_type": "cotacao",
                "source": "yahoo_finance",
                "collected_at": timestamp,


                "ticker": ticker,
                "mercado": "B3",
                "preco": round(preco_atual, 2) if preco_atual else None,
                "abertura": round(preco_aber,2) if preco_aber else None,
                "maxima": round(preco_max,2) if preco_max else None,
                "minima": round(preco_min, 2) if preco_min else None,
                "variacao_pct": variacao_pct,
                "volume": volume
            })

            print(f"Coletado: {ticker} - Preço: {preco_atual} - Variação: {variacao_pct}%")
        
        except Exception as e: 
            print(f"Erro ao coletar dados para {ticker}: {e}")

    return registros 


def coletar_cripto() -> list[dict]:
    registros = []
    timestamp = datetime.utcnow().isoformat()

    ids = ",".join(CRIPTO)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": "usd,brl",
        "include_24hr_change": "true",
        "include_24hr_vol": "true",
        "include_market_cap": "true"
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        dados = resp.json()
    
        for moeda, valores in dados.items():
            registros.append({
            "event_type":   "cotacao",
            "source":       "coingecko",
            "collected_at": timestamp,
            "ticker":       moeda.upper(),
            "mercado":      "CRIPTO",
            "preco_usd":    valores.get("usd"),
            "preco_brl":    valores.get("brl"),
            "variacao_pct": round(valores.get("usd_24h_change", 0), 2),
            "volume_24h":   valores.get("usd_24h_vol"),
            "market_cap":   valores.get("usd_market_cap")
            })
            print(f"Coletado: {moeda.upper()} - $ {valores.get('usd'):,.2f} - Variação: {valores.get('usd_24h_change', 0):.2f}%")

    except Exception as e:
        print(f"Erro ao coletar dados de criptomoedas: {e}")
    
    return registros

def save_data(registros: list[dict], name_base:str):
    if not registros:
        print(f"No data to save in {name_base}.")
        return
    

    hoje = datetime.utcnow().strftime("%Y-%m-%d")
    filedir = DATA_DIR / f"{name_base}_{hoje}.csv"
    df = pd.DataFrame(registros)
    header = not filedir.exists()

    df.to_csv(filedir, mode='a', header=header, index=False)

def exec_get():
    acoes = coletar_acoes()
    save_data(acoes, "cotacoes_acoes")

    cripto = coletar_cripto()
    save_data(cripto, "cotacoes_cripto")

if __name__ == "__main__":
    exec_get()
    schedule.every(5).minutes.do(exec_get)

    while True:
        schedule.run_pending()
        time.sleep(1)