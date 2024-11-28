import requests
import json

regions = [
    "Nordeste",
    "Sudeste",
    "Sul",
    "Norte",
    "Centro-Oeste"
]

history_per_region = {
    "Nordeste": [],
    "Sudeste": [],
    "Sul": [],
    "Norte": [],
    "Centro-Oeste": []
}

for region in regions:
    print(f"Coletando dados para a região {region}...")
    res = requests.get(f"http://127.0.0.1:5000/cidades?limit=50&region={region}")
    cidades = res.json()
    
    for cidade in cidades['results']:
        cidade_id = cidade['id']
        print(f"Coletando dados para a cidade {cidade_id}...")
        response = requests.get(f"http://127.0.0.1:5000/cidades/{cidade_id}/usinas")
        usinas = response.json()

        if (isinstance(usinas, dict) and 'message' in usinas) or not usinas:
            print(f"Nenhuma usina encontrada para a cidade {cidade_id}")
            continue

        for usina in usinas:
            usina_id = usina['usina_id']
            res = requests.get(f"http://127.0.0.1:5000/cidades/{usina_id}/historico")
            historico_data = res.json()

            history_per_region[region].extend(historico_data)
    
    print(f"Dados coletados para a região {region}")
    with open(f'{region}_50_cities_history.json', 'w') as f:
        json.dump(history_per_region[region], f)
    
print("Dados coletados para todas as regiões")