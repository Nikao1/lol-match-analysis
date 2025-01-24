import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Define o backend para um que não exige interface gráfica
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de estilo dos gráficos
sns.set(style="whitegrid")

# Funções de análise podem e serão adicionadas aqui
def extract_participant_stats(match_data, puuid):
    """
    Extrai as estatísticas do jogador com base no PUUID em uma partida.
    """
    participants = match_data.get("info", {}).get("participants", [])
    for participant in participants:
        if participant.get("puuid") == puuid:
            return participant
    return None


def create_dataframe(match_data_list, puuid):
    """
    Cria um DataFrame pandas a partir de uma lista de dados das partidas,
    extraindo as informações relevantes para o jogador com base no PUUID.
    """
    extracted_data = []

    for match_data in match_data_list:
        participant_stats = extract_participant_stats(match_data, puuid)
        if participant_stats:
            # Extrair as informações desejadas (exemplo: KDA, win, champion, etc.)
            extracted_data.append({
                "champion": participant_stats.get("championName"),
                "kills": participant_stats.get("kills"),
                "deaths": participant_stats.get("deaths"),
                "assists": participant_stats.get("assists"),
                "kda": (participant_stats.get("kills") + participant_stats.get("assists")) / max(1, participant_stats.get("deaths")),
                "win": participant_stats.get("win"),
                "totalDamageDealt": participant_stats.get("totalDamageDealt"),
                "goldEarned": participant_stats.get("goldEarned"),
                "cs": participant_stats.get("totalMinionsKilled") + participant_stats.get("neutralMinionsKilled"),
                 # Adicionando informações dos itens
                "item0": participant_stats.get("item0"),
                "item1": participant_stats.get("item1"),
                "item2": participant_stats.get("item2"),
                "item3": participant_stats.get("item3"),
                "item4": participant_stats.get("item4"),
                "item5": participant_stats.get("item5"),
            })

    return pd.DataFrame(extracted_data)

# IDs das novas botas implementadas no jogo
NEW_BOOTS_IDS = {
    3170: "Swiftmarch",
    3171: "Crimson Lucidity",
    3172: "Gunmetal Greaves",
    3173: "Chainlaced Crushers",
    3174: "Armored Advance",
    3175: "Spellslinger's Shoes"
}

def extract_boots_stats(df):
    """
    Extrai as informações das novas botas e calcula a taxa de vitórias.
    """
    # Filtrar as colunas de itens
    item_columns = [f'item{i}' for i in range(6)]  # item0 a item5
    item_columns = [col for col in item_columns if col in df.columns]
    boots_data = []

    for _, row in df.iterrows():
        for col in item_columns:
            item_id = row[col]
            if item_id in NEW_BOOTS_IDS:  # Verificar se é uma das novas botas
                boots_data.append({
                    "boot": NEW_BOOTS_IDS[item_id],
                    "win": row["win"]
                })

    # Criar DataFrame das botas
    boots_df = pd.DataFrame(boots_data)

    # Calcular taxa de vitórias
    boots_win_rate = boots_df.groupby("boot")["win"].mean() * 100

    return boots_win_rate

def plot_boots_win_rate(boots_win_rate):
    """
    Gera um gráfico de barras da taxa de vitórias das novas botas.
    """
    plt.figure(figsize=(10, 6))
    boots_win_rate.sort_values().plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Taxa de Vitórias (%) por Tipo de Bota", fontsize=16)
    plt.xlabel("Tipo de Bota", fontsize=12)
    plt.ylabel("Taxa de Vitórias (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def analyze_boots_win_rate(df):
    """
    Função principal para análise das botas.
    """
    boots_win_rate = extract_boots_stats(df)
    print("Win rate by boot type:")
    print(boots_win_rate)
    plot_boots_win_rate(boots_win_rate)

