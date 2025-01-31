import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Define um backend sem interface gráfica
import matplotlib.pyplot as plt
import numpy as np
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# IDs das botas padrão
DEFAULT_BOOTS_IDS = {
    3006: "Grevas do Berserker",
    3009: "Botas da Rapidez",
    3158: "Botas Ionianas da Lucidez",
    3111: "Passos de Mercúrio",
    3020: "Sapatos do Feiticeiro",
    3013: "Almas Sincronizadas",
    3047: "Botas Galvanizadas de Aço",
}

# IDs das novas botas no jogo
NEW_BOOTS_IDS = {
    3170: "Marcha Célere",
    3171: "Lucidez Escarlate",
    3172: "Grevas Bélicas",
    3173: "Esmagadores Acorrentados",
    3174: "Mobilização Blindada",
    3175: "Sapatos Enfeitiçados",
    3176: "Sempre Avante"
}

ALL_BOOTS_IDS = {**DEFAULT_BOOTS_IDS, **NEW_BOOTS_IDS}

def get_boot_name(items):
    """Identifica qual bota foi comprada pelo jogador."""
    for item in items:
        if item in NEW_BOOTS_IDS:
            return NEW_BOOTS_IDS[item]
    for item in items:
        if item in DEFAULT_BOOTS_IDS:
            return DEFAULT_BOOTS_IDS[item]
    return "Sem Botas"



def create_dataframe(match_data_list, puuid):
    """
    Cria um DataFrame apenas com dados essenciais para os campeões Ahri, Syndra e Taliyah:
    - Campeão jogado
    - Vitória ou derrota
    - Itens comprados (para identificar botas)
    - Nome da bota utilizada
    """
    filtered_champions = {"Ahri", "Syndra", "Taliyah"}  # Conjunto com os campeões desejados
    extracted_data = []

    for match_data in match_data_list:
        participants = match_data.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                champion = participant.get("championName")
                if champion in filtered_champions:  # Filtra apenas os campeões desejados
                    items = [
                        participant.get("item0"),
                        participant.get("item1"),
                        participant.get("item2"),
                        participant.get("item3"),
                        participant.get("item4"),
                        participant.get("item5")
                    ]
                    boot_name = get_boot_name(items)  # Obtém o nome da bota

                    extracted_data.append({
                        "champion": champion,
                        "win": participant.get("win"),
                        "boots": boot_name,
                        "items": items
                    })

    return pd.DataFrame(extracted_data)



def analyze_champion_boots_win_rate(df):
    """Analisa o win rate por campeão dependendo da bota utilizada."""
    data = []

        # Verifica se a coluna "boots" existe
    if "boots" not in df.columns:
        print("A coluna 'boots' não existe no DataFrame.")
        return pd.DataFrame()  # Retorna um DataFrame vazio para evitar erro
    
    for champion in df["champion"].unique():
        champ_data = df[df["champion"] == champion]

        for boot_name in ALL_BOOTS_IDS.values():
            boot_data = champ_data[champ_data["boots"] == boot_name]
            total_with_boot = len(boot_data)
            wins_with_boot = boot_data["win"].sum()

            no_boot_data = champ_data[champ_data["boots"] != boot_name]
            total_without_boot = len(no_boot_data)
            wins_without_boot = no_boot_data["win"].sum()

            win_rate_with_boot = (wins_with_boot / total_with_boot) * 100 if total_with_boot > 0 else None
            win_rate_without_boot = (wins_without_boot / total_without_boot) * 100 if total_without_boot > 0 else None

            data.append({
                "champion": champion,
                "boots": boot_name,
                "win_rate_with_boot": win_rate_with_boot,
                "win_rate_without_boot": win_rate_without_boot,
                "total_with_boot": total_with_boot,
                "total_without_boot": total_without_boot
            })

    return pd.DataFrame(data)

def plot_champion_boots_win_rate(df, output_path="outputs/winrate_campeoes_botas.png"):
    """Cria um gráfico de barras comparando win rate com e sem botas."""
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
    plt.savefig(output_path)
    plt.close()

def analyze_and_plot(df):
    """Executa a análise e gera os gráficos."""
    boots_win_rate_df = analyze_champion_boots_win_rate(df)
    
    logging.info("\nWin Rate por Campeão e Botas:")
    logging.info(boots_win_rate_df)
    
    plot_champion_boots_win_rate(boots_win_rate_df)