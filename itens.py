# Script para percorrer itens no database de versão mais recente do jogo, utilizando a API

import requests

url = "https://ddragon.leagueoflegends.com/cdn/15.2.1/data/en_US/item.json"

response = requests.get(url)
data = response.json()

boots = {}
for item_id, item_data in data["data"].items():
    if "Boots" in item_data.get("tags", []):
        boots[int(item_id)] = item_data["name"]

print("Botas encontradas:")
for item_id, item_name in boots.items():
    print(f"ID: {item_id}, Nome: {item_name}")