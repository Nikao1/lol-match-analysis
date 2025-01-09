import os
from dotenv import load_dotenv
from utils import save_to_csv, extract_match_data
from api import get_puuid, get_match_history, get_match_details

load_dotenv()

nickname = os.getenv("NICKNAME")
tagline = os.getenv("TAGLINE")

print("Tentando obter o PUUID...")
puuid = get_puuid(nickname, tagline)

if puuid:
    print(f"PUUID obtido com sucesso: {puuid}")

    match_ids = get_match_history(puuid, count=5)
    if match_ids:
        print(f"Histórico de partidas obtido com sucesso! Total de partidas: {len(match_ids)}")
        
        for match_id in match_ids:
            print(f"Obtendo detalhes da partida {match_id}...")

            match_details = get_match_details(match_id)

            if match_details:
                print(f"Detalhes da partida {match_id} obtidos com sucesso!")
                print(f"Detalhes: {match_details}")  # Exibe os detalhes para depuração

                print(f"Processando dados da partida {match_id}...")
                match_data = extract_match_data(match_details, puuid)  # Extrai os dados desejados.
                
                print(f"Salvando dados da partida {match_id} em CSV...")
                # Salva os dados em CSV
                save_to_csv("data/match_data.csv", match_data)

            else:
                print(f"Erro ao obter detalhes da partida {match_id}.")
    else:
        print("Não foi possível obter o histórico de partidas. Verifique o PUUID ou a resposta da API.")
else:
    print("Erro ao obter o PUUID! Verifique se as credenciais estão corretas.")
