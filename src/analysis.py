import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Define um backend sem interface gráfica
import matplotlib.pyplot as plt
import numpy as np
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# IDs das novas botas no jogo
NEW_BOOTS_IDS = {
    3170: "Swiftmarch",
    3171: "Crimson Lucidity",
    3172: "Gunmetal Greaves",
    3173: "Chainlaced Crushers",
    3174: "Armored Advance",
    3175: "Spellslinger's Shoes"
}

def create_dataframe(match_data_list, puuid):
    """
    Cria um DataFrame apenas com dados essenciais:
    - Campeão jogado
    - Vitória ou derrota
    - Itens comprados (para identificar botas)
    """
    extracted_data = []

    for match_data in match_data_list:
        participants = match_data.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                extracted_data.append({
                    "champion": participant.get("championName"),
                    "win": participant.get("win"),
                    "items": [
                        participant.get("item0"),
                        participant.get("item1"),
                        participant.get("item2"),
                        participant.get("item3"),
                        participant.get("item4"),
                        participant.get("item5")
                    ]
                })

    return pd.DataFrame(extracted_data)

def analyze_champion_boots_win_rate(df):
    """
    Analisa o win rate por campeão dependendo da bota utilizada.
    Retorna um DataFrame pronto para visualização.
    """
    data = []

    for champion in df["champion"].unique():
        champ_data = df[df["champion"] == champion]

        for boot_id, boot_name in NEW_BOOTS_IDS.items():
            boot_data = champ_data[champ_data["items"].apply(lambda items: boot_id in items)]
            no_boot_data = champ_data[champ_data["items"].apply(lambda items: boot_id not in items)]

            # Win rate com a bota
            total_with_boot = len(boot_data)
            wins_with_boot = boot_data["win"].sum()
            win_rate_with_boot = (wins_with_boot / total_with_boot) * 100 if total_with_boot > 0 else None

            # Win rate sem a bota
            total_without_boot = len(no_boot_data)
            wins_without_boot = no_boot_data["win"].sum()
            win_rate_without_boot = (wins_without_boot / total_without_boot) * 100 if total_without_boot > 0 else None

            data.append({
                "champion": champion,
                "boots": boot_name,
                "win_rate_with_boot": win_rate_with_boot,
                "win_rate_without_boot": win_rate_without_boot
            })

    return pd.DataFrame(data)

def plot_champion_boots_win_rate(df):
    """
    Cria um gráfico de barras agrupadas para comparar a taxa de vitória com e sem cada tipo de bota.
    """
    df = df.dropna()

    if df.empty:
        logging.warning("Nenhum dado válido para plotar.")
        return

    champions = df["champion"].unique()
    boots = df["boots"].unique()
    
    x = np.arange(len(champions)) 
    width = 0.15  

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, boot in enumerate(boots):
        boot_data = df[df["boots"] == boot]

        win_rates_with = {champ: boot_data[boot_data["champion"] == champ]["win_rate_with_boot"].values[0] 
                          if champ in boot_data["champion"].values else 0 for champ in champions}
        
        win_rates_without = {champ: boot_data[boot_data["champion"] == champ]["win_rate_without_boot"].values[0] 
                             if champ in boot_data["champion"].values else 0 for champ in champions}

        
        ax.bar(x + i * width - (len(boots) * width / 2), 
               list(win_rates_with.values()), 
               width=width, 
               label=f"{boot} (Com)", 
               alpha=0.7)

        ax.bar(x + i * width - (len(boots) * width / 2) + width/2, 
               list(win_rates_without.values()), 
               width=width, 
               label=f"{boot} (Sem)", 
               alpha=0.7)

    ax.set_xlabel("Campeões")
    ax.set_ylabel("Win Rate (%)")
    ax.set_title("Win Rate por Campeão e Tipo de Botas")
    ax.set_xticks(x)
    ax.set_xticklabels(champions, rotation=45)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig("outputs/winrate_campeoes_botas.png")
    plt.close()

# Fluxo principal
def analyze_and_plot(df):
    """
    Função central que analisa os dados e gera os gráficos.
    """
    boots_win_rate_df = analyze_champion_boots_win_rate(df)

    logging.info("\nWin Rate por Campeão e Botas:")
    logging.info(boots_win_rate_df)

    plot_champion_boots_win_rate(boots_win_rate_df)