# Funções de análise podem ser adicionadas aqui

def extract_participant_stats(match_data, puuid):
    """
    Extrai as estatísticas do jogador com base no PUUID em uma partida.
    """
    participants = match_data.get("info", {}).get("participants", [])
    for participant in participants:
        if participant.get("puuid") == puuid:
            return participant
    return None
