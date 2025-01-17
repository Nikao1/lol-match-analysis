import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente através do arquivo .env
load_dotenv()

# Obtem a chave API, nickname e tagline através das variáveis de ambiente(.env)
api_key = os.getenv("RIOT_API_KEY")

# Função para obter o PUUID com base no nickname e tagline
def get_puuid(nickname, tagline):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tagline}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")  # Para depuração
    print(f"Resposta da API: {response.text}")    # Para depuração

    if response.status_code == 200:
        try:
            data = response.json()
            return data["puuid"]
        except Exception as e:
            print(f"Erro ao processar a resposta JSON: {e}")
            return None
    elif response.status_code == 500:
        print("Erro interno no servidor da Riot API. Tente novamente mais tarde.")
        return None
    else:
        print(f"Erro ao obter PUUID: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        return None

# Função para obter histórico de partidas com base no PUUID
def get_match_history(puuid, count=10):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=1"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    # Debugging
    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Resposta da API: {response.text}")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("PUUID válido, mas sem histórico de partidas.")
        return None
    elif response.status_code == 403:
        print("Erro de autenticação. Verifique sua chave da API.")
        return None
    elif response.status_code == 429:
        print("Limite de requisições excedido. Aguarde antes de tentar novamente.")
        return None
    else:
        print(f"Erro ao obter histórico de partidas: {response.status_code}")
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
