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
                "Abertura": round(preco_aber,2) if preco_aber else None,
                "maxima": round(preco_max,2) if preco_max else None,
                "minima": round(preco_min, 2) if preco_min else None,
                "variacao_pct": variacao_pct,
                "volume": volume
            })

            print(f"Coletado: {ticker} - Preço: {preco_atual} - Variação: {variacao_pct}%")
        
        except Exception as e: 
            print(f"Erro ao coletar dados para {ticker}: {e}")

    return registros 


if __name__=="__main__":
    resultado = coletar_acoes()
    print(resultado)