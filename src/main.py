from utils import save_to_csv, extract_match_data
from api import get_puuid, get_match_history, get_match_details
from config import nickname, tagline

print("Tentando obter o PUUID...")
puuid = get_puuid(nickname, tagline)
if puuid:
    print(f"PUUID obtido com sucesso: {puuid}")

    match_ids = get_match_history(puuid, count=5)
    if match_ids:
        print("Histórico de partidas obtido com sucesso!")
        for match_id in match_ids:
            match_details = get_match_details(match_id)
            if match_details:
                print(f"Processando detalhes da partida {match_id}...")
                match_data = extract_match_data(match_details, puuid)  # Extrai os dados desejados.


                # Salva os dados em CSV
                save_to_csv("data/match_data.csv", match_data)

        print("Processamento concluído! Dados salvos.")
