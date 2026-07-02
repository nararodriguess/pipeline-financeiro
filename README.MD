# 📈 Real-Time Financial Data Pipeline

A data engineering project that collects, processes, and stores real-time financial data from Brazilian stocks (B3), cryptocurrencies, and financial news.

Built to learn and practice the most in-demand tools in the data engineering market.

---

## 🏗️ Architecture

```
Data Sources
    ↓
[Extract]       Yahoo Finance · CoinGecko · NewsAPI
    ↓
[Load]          CSV files (raw data)
    ↓
[Transform]     DuckDB — Bronze → Silver → Gold layers
    ↓
[Orchestrate]   Apache Airflow (coming soon)
    ↓
[Visualize]     Streamlit Dashboard (coming soon)
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Extraction | Python, yfinance, requests |
| Scheduling | Apache Airflow (coming soon) |
| Streaming | Apache Kafka (coming soon) |
| Processing | PySpark + dbt (coming soon) |
| Storage | DuckDB + Parquet |
| Visualization | Streamlit + Grafana (coming soon) |

---

## 📂 Project Structure

```
pipeline-financeiro/
├── extract/
│   └── get_data.py          # Collects stocks, crypto and news
├── transform/
│   └── load_bronze.py       # Loads CSVs into DuckDB (bronze layer)
├── queries/
│   └── teste.sql            # SQL queries for data exploration
├── streaming/               # Kafka producers and consumers (coming soon)
├── dags/                    # Airflow DAGs (coming soon)
├── dashboard/               # Streamlit app (coming soon)
├── data/                    # Generated CSV files and DuckDB database
├── .env                     # Environment variables (not versioned)
├── requirements.txt
└── README.md
```

---

## 📊 Data Sources

| Source | Data | Cost |
|---|---|---|
| Yahoo Finance | B3 stocks prices | Free |
| CoinGecko API | Crypto prices | Free |
| NewsAPI | Financial news | Free tier |
| BCB / FRED | Macro indicators | Free (coming soon) |

---

## 🗄️ Data Architecture — Medallion

```
Bronze  →  raw data, exactly as collected from sources
Silver  →  cleaned data, no duplicates, correct types (coming soon)
Gold    →  aggregated data, ready for analysis (coming soon)
```

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/nararodriguess/pipeline-financeiro.git
cd pipeline-financeiro
```

**2. Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:
```
NEWSAPI_KEY=your_key_here
```
Get your free API key at [newsapi.org](https://newsapi.org)

**5. Run the collector**
```bash
python extract/get_data.py
```

**6. Load data into DuckDB**
```bash
python transform/load_bronze.py
```

---

## 📦 Current Status

- [x] Project structure
- [x] B3 stocks collector (Yahoo Finance)
- [x] Crypto collector (CoinGecko)
- [x] News collector (NewsAPI)
- [x] CSV storage with daily partitioning
- [x] DuckDB bronze layer with incremental load
- [ ] Kafka streaming
- [ ] PySpark processing
- [ ] dbt transformations (Silver + Gold layers)
- [ ] Airflow orchestration
- [ ] Streamlit dashboard
- [ ] Grafana monitoring

---

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nara-rodriguess/?locale=pt)