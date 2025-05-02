import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Carrega o CSV LIMPO ---
print("\n📂 Lendo jogadas_limpo.csv...")
try:
    df = pd.read_csv("jogadas_limpo.csv")
except FileNotFoundError:
    print("❌ Arquivo 'jogadas_limpo.csv' não encontrado. Execute o limpar_csv.py primeiro!")
    exit()

print(f"✅ {len(df)} jogadas carregadas.")

# --- Inicializa labels das casas ---
casa_labels = [f"casa_{i}" for i in range(1, 26)]

# --- Agrupa jogadas por quantidade de minas ---
if "minas" not in df.columns:
    print("❌ Coluna 'minas' não encontrada no CSV.")
    exit()

minas_unicas = df["minas"].dropna().unique()
minas_unicas.sort()

print(f"\n🔢 Quantidades de minas detectadas: {', '.join(minas_unicas)}")

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

# --- Processa cada grupo separadamente ---
for minas in minas_unicas:
    grupo = df[df["minas"] == minas]
    total = len(grupo)
    if total == 0:
        continue

    print(f"\n🎯 Processando {total} jogadas com {minas} minas...")

    bombas_por_casa = {label: 0 for label in casa_labels}
    diamantes_por_casa = {label: 0 for label in casa_labels}

    for _, row in grupo.iterrows():
        for casa in casa_labels:
            val = row[casa]
            if val == "💣":
                bombas_por_casa[casa] += 1
            elif val == "💎":
                diamantes_por_casa[casa] += 1

    prob_bombas = {c: round((bombas_por_casa[c] / total) * 100, 2) for c in casa_labels}
    prob_diamantes = {c: round((diamantes_por_casa[c] / total) * 100, 2) for c in casa_labels}

    # Cria pasta de saída
    pasta = f"heatmaps/{minas}_minas"
    os.makedirs(pasta, exist_ok=True)

    # Salva CSV
    heatmap_df = pd.DataFrame({
        "casa": casa_labels,
        "bombas": [bombas_por_casa[c] for c in casa_labels],
        "diamantes": [diamantes_por_casa[c] for c in casa_labels],
        "%_bomba": [prob_bombas[c] for c in casa_labels],
        "%_diamante": [prob_diamantes[c] for c in casa_labels],
    })

    csv_saida = os.path.join(pasta, "heatmap_jogadas.csv")
    heatmap_df.to_csv(csv_saida, index=False)
    print(f"✅ Arquivo salvo: {csv_saida}")

    # Gera gráficos
    gerar_heatmap(
        heatmap_df["%_bomba"].tolist(),
        f"% Bomba ({minas} minas)",
        os.path.join(pasta, "heatmap_bombas.png"),
        cmap="Reds"
    )
    gerar_heatmap(
        heatmap_df["%_diamante"].tolist(),
        f"% Diamante ({minas} minas)",
        os.path.join(pasta, "heatmap_diamantes.png"),
        cmap="Greens"
    )

    print("🧨 Heatmap de bombas e 💎 diamantes salvos.")

print("\n✅ Análise finalizada para todas as quantidades de minas.")
