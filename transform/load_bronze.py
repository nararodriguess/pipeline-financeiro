import duckdb
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = Path("data/pipeline.duckdb")

def conectar():
    conn = duckdb.connect(DB_PATH)
    return conn

def criar_tabelas(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bronze_acoes (
            event_type VARCHAR,
            souce VARCHAR,
            collected_at TIMESTAMP,
            ticker VARCHAR,
            mercado VARCHAR,
            preco NUMERIC,
            abertura NUMERIC,
            maxima NUMERIC,
            minima NUMERIC,
            variacao_pct NUMERIC,
            volume NUMERIC
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bronze_cripto (
            event_type VARCHAR,
            souce VARCHAR,
            collected_at TIMESTAMP,
            ticker VARCHAR,
            mercado VARCHAR,
            preco_usd NUMERIC,
            preco_brl NUMERIC,
            variacao_pct NUMERIC,
            volume_24h NUMERIC,
            market_cap NUMERIC
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bronze_noticias (         
            event_type VARCHAR,
            souce VARCHAR,
            collected_at TIMESTAMP,
            titulo VARCHAR,
            descricao VARCHAR,
            url VARCHAR,
            publicado_em TIMESTAMP,
            fonte VARCHAR,
            sentimento VARCHAR              
        )
    """)

    print ("Tabelas criadas com sucesso!")


def carregar_dados(conn):
    
    def carregar_dados_incremental(tabela, arquivo):
        ultima_data = conn.execute(f"""
            SELECT MAX(collected_at) FROM {tabela}          
        """).fetchone()[0]

        if ultima_data is None:
            filtro = "1=1"
        else:
            filtro = f"collected_at > '{ultima_data}'"

        conn.execute(f"""
            INSERT INTO {tabela}
            SELECT * FROM read_csv_auto('{arquivo}')
            WHERE {filtro}
        """)
        
    carregar_dados_incremental("bronze_acoes", "data/cotacoes_acoes*.csv")
    carregar_dados_incremental("bronze_cripto", "data/cotacoes_cripto*.csv")
    carregar_dados_incremental("bronze_noticias", "data/noticias*.csv")


if __name__ == "__main__":
    print("Iniciando o processo de carga de dados para o banco de dados DuckDB...")
    conn = conectar()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    criar_tabelas(conn)
    print("Tabelas criadas com sucesso!")
    carregar_dados(conn)
    print("Dados carregados com sucesso!")
    conn.close()
    print("Concluído!")