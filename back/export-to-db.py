import pandas as pd
from sqlalchemy import create_engine

MAIN_PATH = "./raw"
FILE = "endereco"
# PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/etal')

chunk_size = 10_000  # Número de linhas por pedaço

for chunk in pd.read_csv(f"{MAIN_PATH}/{FILE}", chunksize=chunk_size):
    # Salva no banco, criando a tabela 'geracao' (ou insere nela)
    chunk.to_sql(f'{FILE}', con=engine, if_exists='append', index=False)
    print(f"Processado mais um pedaço com {len(chunk)} linhas.")