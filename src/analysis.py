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
    # Converte a lista de itens para um conjunto
    items_set = set(items)
    
    # Verifica se há alguma bota nos itens
    boots_found = items_set.intersection(ALL_BOOTS_IDS.keys())
    
    if boots_found:
        # Retorna o nome da primeira bota encontrada
        return ALL_BOOTS_IDS[list(boots_found)[0]]
    return "Sem Botas"



def create_dataframe(match_data_list, puuid):
    """
    Cria um DataFrame apenas com dados essenciais para os campeões desejados:
    - Campeão jogado
    - Vitória ou derrota
    - Itens comprados (para identificar botas)
    - Nome da bota utilizada
    """
    filtered_champions = {"Ahri"}  # Conjunto com os campeões desejados
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

                    # Adiciona os dados apenas se o jogador comprou botas
                    if boot_name != "Sem Botas":
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

    for champion in df["champion"].unique():
        champ_data = df[df["champion"] == champion]

        for boot_name in ALL_BOOTS_IDS.values():
            # Win rate COM a bota específica
            boot_data = champ_data[champ_data["boots"] == boot_name]
            total_with_boot = len(boot_data)
            wins_with_boot = boot_data["win"].sum()

            # Win rate SEM a bota específica (excluindo outras botas)
            no_boot_data = champ_data[
                (champ_data["boots"] != boot_name) &  # Não está usando a bota específica
                (champ_data["boots"] != "Sem Botas")  # Exclui partidas sem botas
            ]
            total_without_boot = len(no_boot_data)
            wins_without_boot = no_boot_data["win"].sum()

            # Calcula o win rate
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
    
    # Remove botas sem partidas
    df = df[df["total_with_boot"] > 0]

    # Remove valores NaN apenas para colunas de win rate
    df = df.dropna(subset=["win_rate_with_boot", "win_rate_without_boot"], how="all")

    if df.empty:
        print("Nenhum dado válido para plotar.")
        return

    champions = df["champion"].unique()
    boots_used = df["boots"].unique()  # Botas realmente utilizadas

    x = np.arange(len(champions))  
    width = 0.8 / len(boots_used)  # Ajuste dinâmico do espaçamento

    fig, ax = plt.subplots(figsize=(16, 8))

    legend_labels = []

    for i, boot in enumerate(boots_used):
        boot_data = df[df["boots"] == boot]

        win_rates_with = [boot_data[boot_data["champion"] == champ]["win_rate_with_boot"].values[0] 
                          if champ in boot_data["champion"].values else np.nan for champ in champions]
        
        win_rates_without = [boot_data[boot_data["champion"] == champ]["win_rate_without_boot"].values[0] 
                             if champ in boot_data["champion"].values else np.nan for champ in champions]

        # Evita criar barras para valores NaN
        if not np.isnan(win_rates_with).all():
            bars1 = ax.bar(x + i * width - (len(boots_used) * width / 2), 
                   [wr if not np.isnan(wr) else 0 for wr in win_rates_with], 
                   width=width, 
                   label=f"{boot} (Com)", 
                   alpha=0.7)
            legend_labels.append(f"{boot} (Com)")

        if not np.isnan(win_rates_without).all():
            bars2 = ax.bar(x + i * width - (len(boots_used) * width / 2) + width/2, 
                   [wr if not np.isnan(wr) else 0 for wr in win_rates_without], 
                   width=width, 
                   label=f"{boot} (Sem)", 
                   alpha=0.7)
            legend_labels.append(f"{boot} (Sem)")

    ax.set_xlabel("Campeões")
    ax.set_ylabel("Win Rate (%)")
    ax.set_title("Win Rate por Campeão e Tipo de Botas")
    ax.set_xticks(range(len(champions))) 
    ax.set_xticklabels(champions, rotation=45, ha="right")

    if legend_labels:  
        ax.legend(legend_labels, fontsize=8, loc="upper left", bbox_to_anchor=(1,1))
    
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