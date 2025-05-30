import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# --- Função para gerar heatmaps ---
def gerar_heatmap(valores, titulo, arquivo, cmap):
    matriz = np.array(valores).reshape((5, 5))
    plt.figure(figsize=(6, 5))
    sns.heatmap(matriz, annot=True, fmt=".2f", cmap=cmap, cbar=True, linewidths=.5)
    plt.title(titulo)
    plt.xticks(np.arange(5) + 0.5, [f"C{i+1}" for i in range(5)])
    plt.yticks(np.arange(5) + 0.5, [f"L{i+1}" for i in range(5)], rotation=0)
    plt.tight_layout()
    plt.savefig(arquivo)
    plt.close()

def main():
    if len(sys.argv) < 2:
        print("❌ Por favor, informe o caminho da pasta como argumento.")
        print("Exemplo: python analisar_jogadas.py dados/8_minas")
        return

    pasta = sys.argv[1]
    arquivo_csv = os.path.join(pasta, "jogadas_limpo.csv")

    print(f"\n📂 Lendo {arquivo_csv}...")

    try:
        df = pd.read_csv(arquivo_csv)
    except FileNotFoundError:
        print(f"❌ Arquivo '{arquivo_csv}' não encontrado.")
        return

    print(f"✅ {len(df)} jogadas carregadas.")

    casa_labels = [f"casa_{i}" for i in range(1, 26)]

    if "minas" not in df.columns:
        print("❌ Coluna 'minas' não encontrada no CSV.")
        return

    minas = df["minas"].iloc[0]
    total = len(df)

    print(f"\n🎯 Processando {total} jogadas com {minas} minas...")

    bombas_por_casa = {label: 0 for label in casa_labels}
    diamantes_por_casa = {label: 0 for label in casa_labels}

    for _, row in df.iterrows():
        for casa in casa_labels:
            val = row[casa]
            if val == "💣":
                bombas_por_casa[casa] += 1
            elif val == "💎":
                diamantes_por_casa[casa] += 1

    prob_bombas = {c: round((bombas_por_casa[c] / total) * 100, 2) for c in casa_labels}
    prob_diamantes = {c: round((diamantes_por_casa[c] / total) * 100, 2) for c in casa_labels}

    # Cria pasta de saída
    pasta_saida = os.path.join(pasta, "heatmaps")
    os.makedirs(pasta_saida, exist_ok=True)

    heatmap_df = pd.DataFrame({
        "casa": casa_labels,
        "bombas": [bombas_por_casa[c] for c in casa_labels],
        "diamantes": [diamantes_por_casa[c] for c in casa_labels],
        "%_bomba": [prob_bombas[c] for c in casa_labels],
        "%_diamante": [prob_diamantes[c] for c in casa_labels],
    })

    csv_saida = os.path.join(pasta_saida, "heatmap_jogadas.csv")
    heatmap_df.to_csv(csv_saida, index=False)
    print(f"✅ Arquivo salvo: {csv_saida}")

    gerar_heatmap(
        heatmap_df["%_bomba"].tolist(),
        f"% Bomba ({minas} minas)",
        os.path.join(pasta_saida, "heatmap_bombas.png"),
        cmap="Reds"
    )
    gerar_heatmap(
        heatmap_df["%_diamante"].tolist(),
        f"% Diamante ({minas} minas)",
        os.path.join(pasta_saida, "heatmap_diamantes.png"),
        cmap="Greens"
    )

    print("🧨 Heatmap de bombas e 💎 diamantes salvos.")
    print("\n✅ Análise finalizada.")

if __name__ == "__main__":
    main()
