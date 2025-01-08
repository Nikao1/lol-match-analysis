import csv
import os

def extract_match_data(match_details, puuid):
    """
    Extrai dados relevantes da partida para salvar no CSV.
    """
    participants = match_details["info"]["participants"]
    player_data = next(p for p in participants if p["puuid"] == puuid)  
    # Localiza o jogador pela PUUID.

    # Extração dos dados desejados
    match_data = {
        "game_id": match_details["metadata"]["matchId"],
        "summoner_name": player_data["summonerName"],
        "damage": player_data["totalDamageDealtToChampions"],
        "kda": f"{player_data['kills']}/{player_data['deaths']}/{player_data['assists']}",
        "wards": player_data["wardsPlaced"],
        "farm": player_data["totalMinionsKilled"] + player_data["neutralMinionsKilled"],
        "items": [
            player_data.get(f"item{i}", 0) for i in range(6)  # Extrai itens (máximo 6 slots).
        ]
    }
    return match_data

def save_to_csv(filename, match_data):
    """
    Salva os dados da partida em um arquivo CSV organizado por colunas.
    """
    file_exists = os.path.isfile(filename)  # Verifica se o arquivo já existe.
    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["game_id", "summoner_name", "damage", "kda", "wards", "farm", 
                      "item_1", "item_2", "item_3", "item_4", "item_5", "item_6"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:  # Se o arquivo não existe, escreve o cabeçalho.
            writer.writeheader()

        # Organiza itens em colunas separadas
        row = {
            "game_id": match_data["game_id"],
            "summoner_name": match_data["summoner_name"],
            "damage": match_data["damage"],
            "kda": match_data["kda"],
            "wards": match_data["wards"],
            "farm": match_data["farm"],
        }
        for i, item in enumerate(match_data["items"], start=1):
            row[f"item_{i}"] = item
        writer.writerow(row)
