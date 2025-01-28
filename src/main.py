import os
from dotenv import load_dotenv
from api import get_puuid, get_match_history, get_match_details
from utils import save_to_json
from analysis import create_dataframe, analyze_and_plot

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do ambiente
api_key = os.getenv("RIOT_API_KEY")
nickname = os.getenv("RIOT_NICKNAME")
tagline = os.getenv("RIOT_TAGLINE")

# Número de partidas a serem analisadas
MATCH_COUNT = 100

def main():
    print("Tentando obter o PUUID...")
    puuid = get_puuid(api_key, nickname, tagline)

    if puuid:
        print(f"PUUID obtido com sucesso: {puuid}")
        match_ids = get_match_history(api_key, puuid, count=MATCH_COUNT)

        if match_ids:
            match_data_list = []
            for match_id in match_ids:
                match_details = get_match_details(api_key, match_id)
                if match_details:
                    save_to_json(f"data/match_{match_id}.json", match_details)
                    print(f"Detalhes da Partida {match_id} salvos com sucesso.")
                    match_data_list.append(match_details)

            if match_data_list:
                print("Iniciando análise de dados...")

                # Criar DataFrame com os dados das partidas
                df = create_dataframe(match_data_list, puuid)

                # Realizar análise das botas
                analyze_and_plot(df)
                
            else:
                print("Nenhum dado de partida foi coletado.")
        else:
            print("Falha ao obter o histórico de partidas.")
    else:
        print("Falha ao obter o PUUID.")

if __name__ == "__main__":
    main()
