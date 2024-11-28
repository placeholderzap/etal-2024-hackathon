import pandas as pd
from sqlalchemy import create_engine
from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

MAIN_PATH = "./raw"
FILE = "unidade_consumidora"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

chunk_size = 10_000

for chunk in pd.read_csv(f"{MAIN_PATH}/{FILE}", chunksize=chunk_size):
    chunk.to_sql(f'{FILE}', con=engine, if_exists='append', index=False)
    print(f"Processado mais um pedaço com {len(chunk)} linhas.")