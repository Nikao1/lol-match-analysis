import os
from dotenv import load_dotenv
from api import get_puuid, get_match_history, get_match_details
from utils import save_to_json

# Carregar variáveis de ambiente
load_dotenv()

api_key = os.getenv("RIOT_API_KEY")
nickname = os.getenv("RIOT_NICKNAME")
tagline = os.getenv("RIOT_TAGLINE")

print("Tentando obter o PUUID...")
puuid = get_puuid(api_key, nickname, tagline)

if puuid:
    print(f"PUUID obtido com sucesso: {puuid}")
    match_ids = get_match_history(api_key, puuid)
    if match_ids:
        for match_id in match_ids:
            match_details = get_match_details(api_key, match_id)
            if match_details:
                save_to_json(f"data/match_{match_id}.json", match_details)
                print(f"Detalhes da Partida {match_id} salvos com sucesso.")
else:
    print("Falha ao obter o PUUID.")
