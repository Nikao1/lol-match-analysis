import os
import logging
from dotenv import load_dotenv
from api import get_puuid, get_match_history, get_match_details
from utils import save_to_json
from analysis import create_dataframe, analyze_and_plot

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do ambiente
api_key = os.getenv("RIOT_API_KEY")
nickname = os.getenv("RIOT_NICKNAME")
tagline = os.getenv("RIOT_TAGLINE")

# Número de partidas a serem analisadas
MATCH_COUNT = 100

def main():
    logging.info("Tentando obter o PUUID...")
    puuid = get_puuid(api_key, nickname, tagline)

    if puuid:
        logging.info(f"PUUID obtido com sucesso: {puuid}")
        match_ids = get_match_history(api_key, puuid, count=MATCH_COUNT)

        if match_ids:
            match_data_list = []
            for match_id in match_ids:
                try:
                    match_details = get_match_details(api_key, match_id)
                    if match_details:
                        save_to_json(f"data/match_{match_id}.json", match_details)
                        logging.info(f"Detalhes da Partida {match_id} salvos com sucesso.")
                        match_data_list.append(match_details)
                except Exception as e:
                    logging.error(f"Erro ao obter detalhes da partida {match_id}: {e}")

            if match_data_list:
                logging.info("Iniciando análise de dados...")

                # Criar DataFrame com os dados das partidas
                df = create_dataframe(match_data_list, puuid)

                # Realizar análise das botas
                analyze_and_plot(df)
                
            else:
                logging.warning("Nenhum dado de partida foi coletado.")
        else:
            logging.error("Falha ao obter o histórico de partidas.")
    else:
        logging.error("Falha ao obter o PUUID.")

if __name__ == "__main__":
    main()