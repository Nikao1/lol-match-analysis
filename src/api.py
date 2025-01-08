import requests
from config import api_key

# Função para obter o PUUID com base no nickname e tagline
def get_puuid(nickname, tagline):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tagline}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["puuid"]
    else:
        print(f"Erro ao obter PUUID: {response.status_code}")
        print(response.json())
        return None

# Função para obter histórico de partidas com base no PUUID
def get_match_history(puuid, count=10):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter histórico de partidas: {response.status_code}")
        print(response.json())
        return None

# Função para obter detalhes de uma partida com base no Match ID
def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter detalhes da partida {match_id}: {response.status_code}")
        print(response.json())
        return None
