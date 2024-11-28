import datetime
import psycopg2
from datetime import timedelta
import matplotlib.pyplot as plt

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect("dbname='etal' user='postgres' password='postgres' host='localhost' port='5432'")
cursor = conn.cursor()

# Definir o ID da usina e o ano atual
usina_id = int(input("Insira o ID da usina: "))
ano_atual = datetime.datetime.now().year

# Inicializar o mapper para armazenar as somas
mapper = {}
anos = []
geracao_real = []
geracao_esperada = []
desvios_percentuais = []

# Query para pegar os valores iniciais de start_date
cursor.execute("""
    SELECT 
        uh.start_date::DATE
    FROM usina_historico AS uh
    WHERE uh.plant_id = %s
    ORDER BY uh.start_date::DATE;
""", (usina_id,))

# Pegar o resultado da query (start_date inicial)
resultados = cursor.fetchall()

ano_counter = 1
soma_total_gerada = 0  # Variável para armazenar a soma de gerações totais

# Para cada start_date, iterar até o ano atual
for row in resultados:
    start_date = row[0]
    data_fim = start_date + timedelta(days=365)  # Data fim para o primeiro período de 12 meses

    while data_fim.year <= ano_atual:
        # Gerar a query dinâmica com o start_date e data_fim
        query_dinamica = f"""
        SELECT 
            '{start_date}'::DATE AS start_date, 
            '{data_fim}'::DATE AS data_fim,
            SUM(g.quantidade) AS soma_total_12_meses
        FROM geracao AS g
        JOIN usina AS u ON g.id_usina = u.id
        JOIN usina_historico AS uh ON uh.plant_id = u.id
        WHERE 
            u.id = {usina_id}
            AND g.data >= '{start_date}'::DATE
            AND g.data < '{data_fim}'::DATE
        GROUP BY  
            '{start_date}'::DATE
        ORDER BY '{start_date}'::DATE;
        """

        # Executar a query dinâmica
        cursor.execute(query_dinamica)
        resultado = cursor.fetchone()

        # Armazenar a soma no mapper (dicionário) com a chave como 'ano_1', 'ano_2', etc.
        if resultado:
            # Gerar a chave como 'ano_1', 'ano_2', etc.
            chave = f"ano_{ano_counter}"
            soma_total = resultado[2]  # Soma total de 12 meses

             # Adicionar ano e geração real
            anos.append(ano_counter)
            geracao_real.append(soma_total)

            if ano_counter == 1:
                # Para o primeiro ano, a geração esperada é igual à geração real
                geracao_esperada.append(soma_total)
                desvios_percentuais.append(0)  # Não há desvio no primeiro ano

            elif ano_counter == 2:
                # Para o ano 2, aplicar uma depreciação de 2,5%
                deprecado_esperado = soma_total * (1 - 0.025)
                geracao_esperada.append(deprecado_esperado)
                desvio = soma_total - deprecado_esperado
                percentual_desvio = (desvio / deprecado_esperado) * 100 if deprecado_esperado != 0 else 0
                desvios_percentuais.append(percentual_desvio)

            elif ano_counter > 2:
                # Para os anos subsequentes (ano 3 em diante), aplicar uma depreciação de 0,5%
                deprecado_esperado = soma_total * (1 - 0.005)
                geracao_esperada.append(deprecado_esperado)
                desvio = soma_total - deprecado_esperado
                percentual_desvio = (desvio / deprecado_esperado) * 100 if deprecado_esperado != 0 else 0
                desvios_percentuais.append(percentual_desvio)

            # Armazenar a soma no mapper (dicionário) com a chave como 'ano_1', 'ano_2', etc.
            mapper[chave] = soma_total
            soma_total_gerada += soma_total

        # Atualizar start_date para o próximo período de 12 meses
        start_date = data_fim
        data_fim = start_date + timedelta(days=365)  # Próximo intervalo de 12 meses

        # Incrementar o contador para o próximo ano
        ano_counter += 1

# Fechar a conexão
cursor.close()
conn.close()

# Exibir o mapper com os resultados
print("Resultados do mapeamento de geração por ano:")
print(mapper)

# Criar gráficos de análise
plt.figure(figsize=(12, 6))

# Gráfico de Geração Real vs Geração Esperada
plt.subplot(1, 2, 1)
plt.plot(anos, geracao_real, label="Geração Real", marker='o')
plt.plot(anos, geracao_esperada, label="Geração Esperada", marker='x')
plt.xlabel('Ano')
plt.ylabel('Geração (kWh)')
plt.xticks(anos)  # Adiciona os anos reais como rótulos no eixo x
plt.title('Geração Real vs Geração Esperada')
plt.legend()

# Gráfico de Desvio Percentual
plt.subplot(1, 2, 2)
plt.plot(anos[1:], desvios_percentuais[1:], label="Desvio Percentual", color='red', marker='s')
plt.xlabel('Ano')
plt.ylabel('Desvio Percentual (%)')
plt.xticks(anos[1:])  # Adiciona os anos reais como rótulos no eixo x
plt.title('Desvio Percentual ao Longo dos Anos')
plt.legend()

# Ajustar o layout dos gráficos para melhor exibição
plt.tight_layout()

# Exibir os gráficos
plt.show()