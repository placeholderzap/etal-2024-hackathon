import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from constants import day_of_week_map, months_map, uf_map, regiao_map
import dask.dataframe as dd
import polars as pl

import matplotlib
matplotlib.use('TkAgg')

df = dd.read_json('app/utils/historico123.json')
df_consolidado = df.compute()
df_consolidado.to_parquet(
    "geracao.parquet",
    engine="pyarrow",
    compression="snappy",
)

# db = pl.read_json('app/utils/historico123.json')
# db['data'] = pd.to_datetime(db['data'], format='%Y-%m-%d')

# db['day_of_week'] = db['data'].dt.day_name()
# db['day'] = db['data'].dt.day
# db['month'] = db['data'].dt.month_name()
# db['year'] = db['data'].dt.year


# db['day_of_week'] = db['day_of_week'].map(day_of_week_map)

# db['month'] = db['month'].map(months_map)
# db['uf'] = db['uf'].map(uf_map)
# db['regiao'] = db['regiao'].map(regiao_map)

# def classify(row):
#     if row['geracao'] > 1.2 * row['prognostico']:
#         return '20% acima'
#     elif row['geracao'] < 0.7 * row['prognostico']:
#         return '70% abaixo'
#     else:
#         return 'Entre 70% e 20%'
    
# def detect_outliers(column):
#     Q1 = column.quantile(0.25)
#     Q3 = column.quantile(0.75)
#     IQR = Q3 - Q1
#     return (column < (Q1 - 1.5 * IQR)) | (column > (Q3 + 1.5 * IQR))
    
# db['classificacao'] = db.apply(classify, axis=1)
# db['geracao_outliers'] = detect_outliers(db['geracao'])
# db['prognostico_outliers'] = detect_outliers(db['prognostico'])

# # viés de geração
# counts = db['classificacao'].value_counts()

# sns.barplot(x=counts.index, y=counts.values, palette="viridis")
# plt.title("Número de Usinas por Faixa de Geração")
# plt.xlabel("Classificação")
# plt.ylabel("Número de Usinas")

# count = db.duplicated().sum()
# print(count)
