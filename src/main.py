import requests

# Substitua por sua chave de API correta
api_key = "RGAPI-beb34903-41a5-4cde-9eab-92ba57511b77"
summoner_name = "Nik"
base_url = "https://americas.api.riotgames.com/lol"  # Atualizando a URL para usar a região 'americas'

def get_summoner_id(summoner_name):
    url = f"{base_url}/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    # Adicionando o print para verificar a resposta JSON
    if response.status_code == 200:
        data = response.json()
        print(data)  # Isso irá mostrar a resposta completa da API
        return data["id"]
    else:
        print(f"Erro ao obter o ID do invocador: {response.status_code}")
        print(response.json())  # Isso irá mostrar a resposta de erro (se houver)
        return None

summoner_id = get_summoner_id(summoner_name)
