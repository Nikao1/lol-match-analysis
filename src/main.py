import requests
import json 

# Definição de chave API e variáveis de configuração (Nickname e Tagline)
api_key = "RGAPI-a9767604-ede1-4525-ad25-607c65f149a7"

nickname = "Nik"
tagline = "Line"

# Região para endpoints globais (Americas nesse caso)
match_base_url = "https://americas.api.riotgames.com"

# Função para obter o PUUID com base no nickname e tagline
def get_puuid(nickname, tagline):
    url = f"{match_base_url}/riot/account/v1/accounts/by-riot-id/{nickname}/{tagline}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("PUUID:", data)
        return data["puuid"]
    else:
        print(f"Erro ao obter PUUID: {response.status_code}")
        print(response.json())
        return None

# Função para obter o histórico de partidas com base no PUUID
def get_match_history(puuid, count=5):
    url = f"{match_base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        match_ids = response.json()
        print(f"Partidas recentes: {match_ids}")
        return match_ids
    else:
        print(f"Erro ao obter histórico de partidas: {response.status_code}")
        print(response.json())
        return None

# Função para obter detalhes de uma partida específica
def get_match_details(match_id):
    url = f"{match_base_url}/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter detalhes da partida:", response.status_code)
        print(response.json())
        return None

# Obter o PUUID
puuid = get_puuid(nickname, tagline)

# Obter histórico de partidas usando o PUUID
if puuid:
    match_ids = get_match_history(puuid)
    if match_ids:
        print("Histórico de Partidas obtido com sucesso!")
        for match_id in match_ids:
            match_details = get_match_details(match_id)
            if match_details:
                print(f"\nDetalhes da Partida {match_id}:")
                
                # Aqui é onde você adiciona o json.dumps para melhorar a legibilidade
                print(json.dumps(match_details, indent=4))
