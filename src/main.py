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
            last_processed_index = 0

            # Verifica se há um progresso salvo
            progress_file = "data/last_processed_index.txt"
            if os.path.exists(progress_file):
                with open(progress_file, "r") as f:
                    last_processed_index = int(f.read().strip())

            for i in range(last_processed_index, len(match_ids)):
                match_id = match_ids[i]
                try:
                    # Verifica se os detalhes da partida já foram salvos em cache
                    cache_file = f"data/match_{match_id}.json"
                    if os.path.exists(cache_file):
                        logging.info(f"Carregando detalhes da partida {match_id} do cache...")
                        with open(cache_file, "r") as f:
                            match_details = json.load(f)
                    else:
                        match_details = get_match_details(api_key, match_id)
                        if match_details:
                            save_to_json(cache_file, match_details)
                            logging.info(f"Detalhes da Partida {match_id} salvos com sucesso.")

                    if match_details:
                        match_data_list.append(match_details)

                    # Salva o progresso atual
                    with open(progress_file, "w") as f:
                        f.write(str(i + 1))  # Salva o próximo índice a ser processado

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
