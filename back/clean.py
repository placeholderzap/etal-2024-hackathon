import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from constants import day_of_week_map, months_map, uf_map, regiao_map
import matplotlib
matplotlib.use('TkAgg')
db = pd.read_json('app/utils/historico_data.json')
db['data'] = pd.to_datetime(db['data'], format='%Y-%m-%d')
db['day_of_week'] = db['data'].dt.day_name()
db['day'] = db['data'].dt.day
db['month'] = db['data'].dt.month_name()
db['year'] = db['data'].dt.year
db['day_of_week'] = db['day_of_week'].map(day_of_week_map)
db['month'] = db['month'].map(months_map)
db['uf'] = db['uf'].map(uf_map)
db['regiao'] = db['regiao'].map(regiao_map)
db = db.sort_values(by='data').reset_index(drop=True)
db["geracao_media"] = db["geracao"].rolling(window=30).mean()
db = db.dropna(subset=["geracao_media"])
print("Dados Faltantes: ")
print(db.isna().sum())
# geracao pelo tempo
# sns.lineplot(x='data', y='geracao_media', data=db)
# plt.title("Geração de Energia ao Longo dos Anos")
# plt.xlabel("Ano")
# plt.ylabel("Geração de Energia")
# plt.show()
print(db.head(10))
# db.info()
# db.describe()
# print(db.corr())
# sns.heatmap(db.corr(), annot=True)
# sns.boxplot(x='geracao', y='prognostico', data=db)
def classify(row):
    if row['geracao'] > 1.2 * row['prognostico']:
        return '20% acima'
    elif row['geracao'] < 0.7 * row['prognostico']:
        return '70% abaixo'
    else:
        return 'Entre 70% e 20%'
    
def detect_outliers(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    return (column < (Q1 - 1.5 * IQR)) | (column > (Q3 + 1.5 * IQR))
    
db['classificacao'] = db.apply(classify, axis=1)
db['geracao_outliers'] = detect_outliers(db['geracao'])
db['prognostico_outliers'] = detect_outliers(db['prognostico'])
# db['geracao_zscore'] = stats.zscore(db['geracao'])
# db['prognostico_zscore'] = stats.zscore(db['prognostico'])
# db['geracao_outliers_zscore'] = db['geracao_zscore'].apply(lambda x: x < -3 or x > 3)
# db['prognostico_outliers_zscore'] = db['prognostico_zscore'].apply(lambda x: x < -3 or x > 3)
# outiliers_count = db['geracao_outliers'].sum() + db['prognostico_outliers'].sum()
# print("Número de Outliers: ", outiliers_count)
outiliers_geracao_count = db['geracao_outliers'].sum()
outiliers_prognostico_count = db['prognostico_outliers'].sum()
print(db[db['geracao_outliers'] == True])
counts = db['classificacao'].value_counts()
# boxplot
# plt.figure(figsize=(10, 6))
# plt.boxplot([db['geracao'], db['prognostico']], labels=['Geração', 'Prognóstico'])
# plt.title("Boxplot de Geração e Prognóstico")
# plt.ylabel("Values")
# plt.show()
# viés de geração
sns.barplot(x=counts.index, y=counts.values, palette="viridis")
plt.title("Número de Usinas por Faixa de Geração")
plt.xlabel("Classificação")
plt.ylabel("Número de Usinas")
count = db.duplicated().sum()
print(count)
def train_split(df):
    X = df.drop(columns=['geracao', 'classificacao', 'geracao_outliers', 'prognostico_outliers', 'geracao_media', "data", "prognostico"])
    y = df['geracao_media']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test
X_train, X_test, y_train, y_test = train_split(db)
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)
r2 = r2_score(y_test, model.predict(X_test))
print("R2: ", r2)
X = db.drop(columns=['geracao', 'classificacao', 'geracao_outliers', 'prognostico_outliers', 'geracao_media', "data", "prognostico"])
future_dates = pd.date_range(start=db['data'].max(), periods=100, freq='D')
future_features = pd.DataFrame({
    'day_of_week': future_dates.day_name().map(day_of_week_map),
    'day': future_dates.day,
    'month': future_dates.month,
    'year': future_dates.year,
    'uf': 20,
    'regiao': 2,
    'estado_id': 20,
    'id_cidade': 30,
    'usina_id': 428717
})
future_features = future_features[X.columns]
future_predictions = model.predict(future_features)
predicted_db = pd.DataFrame({
    'data': future_dates,
    'geracao_prevista': future_predictions
})
plt.figure(figsize=(10, 6))
plt.plot(db['data'], db['geracao_media'], label='Real', color='blue')
plt.plot(predicted_db['data'], predicted_db['geracao_prevista'], label='Previsto', color='red')
plt.title("Previsão de Geração de Energia")
plt.xlabel("Data")
plt.ylabel("Geração de Energia")
plt.legend()
plt.show()