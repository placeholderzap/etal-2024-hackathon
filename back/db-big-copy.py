import os
import pandas as pd
import psycopg2
from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

MAIN_PATH = "C:/Users/vitor/Downloads"
FILE = "geracao"
CHUNK_SIZE = 500_000

# conn = psycopg2.connect(f"dbname={DB_PORT} user='postgres' password='postgres' host='localhost' port='5432'")
conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}")
cursor = conn.cursor()

for i, chunk in enumerate(pd.read_csv(f"{MAIN_PATH}/{FILE}", chunksize=CHUNK_SIZE)):
    # Salvar o chunk como CSV temporário
    temp_csv = f"temp_chunk_{i}.csv"
    chunk.to_csv(temp_csv, index=False, header=(i == 0))  # Escreve header apenas no primeiro chunk

    # Usar COPY para inserir no banco
    with open(temp_csv, 'r') as f:
        cursor.copy_expert(f"COPY geracao_detalhe FROM STDIN WITH CSV HEADER", f)

    os.remove(temp_csv)

    conn.commit()
    print(f"Processado chunk {i+1} com {len(chunk)} linhas.")

cursor.close()
conn.close()
