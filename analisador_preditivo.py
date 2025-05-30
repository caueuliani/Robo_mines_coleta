import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def inicializar_matriz():
    return pd.DataFrame(
        np.zeros((5, 5)),
        columns=[f"C{i+1}" for i in range(5)],
        index=[f"L{i+1}" for i in range(5)]
    )

def atualizar_matriz(matriz, jogadas):
    for _, linha in jogadas.iterrows():
        for idx in range(25):
            valor = linha[f"casa_{idx+1}"]
            row = idx // 5
            col = idx % 5
            if valor == "💣":
                matriz.iloc[row, col] += 1
    return matriz

def calcular_probabilidades(matriz, total):
    return matriz / total

def gerar_heatmap(matriz_prob, path_heatmap, minas):
    plt.figure(figsize=(6, 5))
    sns.heatmap(matriz_prob, annot=True, fmt=".2f", cmap="Reds", cbar=True, linewidths=.5)
    plt.title(f"Heatmap % Bombas - {minas} Minas")
    plt.xticks(np.arange(5) + 0.5, [f"C{i+1}" for i in range(5)])
    plt.yticks(np.arange(5) + 0.5, [f"L{i+1}" for i in range(5)], rotation=0)
    plt.tight_layout()
    plt.savefig(path_heatmap)
    plt.close()

def analisar_grupo(minas, grupo_df, path_dir):
    if len(grupo_df) == 0:
        print(f"⚠️ Nenhuma jogada para {minas} minas. Pulando...")
        return

    print(f"\n🔎 Analisando {len(grupo_df)} jogadas com {minas} minas...")

    matriz_bombas = atualizar_matriz(inicializar_matriz(), grupo_df)
    matriz_prob = calcular_probabilidades(matriz_bombas, len(grupo_df))

    os.makedirs(path_dir, exist_ok=True)

    path_contagem = os.path.join(path_dir, "contagem.csv")
    path_probabilidades = os.path.join(path_dir, "probabilidades.csv")
    path_sugestoes = os.path.join(path_dir, "melhores_casas.txt")
    path_heatmap = os.path.join(path_dir, "heatmap_probabilidades.png")

    matriz_bombas.to_csv(path_contagem)
    matriz_prob.to_csv(path_probabilidades)

    print(f"✅ Contagem salva em {path_contagem}")
    print(f"✅ Probabilidades salvas em {path_probabilidades}")

    print("\n🔢 Matriz de Probabilidades (% de bomba):")
    for i in range(5):
        print(" ".join(f"{matriz_prob.iloc[i, j]*100:6.2f}%" for j in range(5)))

    print("\n🎯 Melhores casas para clicar:")
    matriz_linear = matriz_prob.values.flatten()
    indices_melhores = np.argsort(matriz_linear)[:5]
    sugestoes = []
    for idx in indices_melhores:
        linha = idx // 5
        coluna = idx % 5
        prob = matriz_prob.iloc[linha, coluna] * 100
        sugestoes.append(f"Casa {idx+1} (Linha {linha+1}, Coluna {coluna+1}) → {prob:.2f}% de bomba")
        print(sugestoes[-1])

    with open(path_sugestoes, "w", encoding="utf-8") as f:
        f.write("\n".join(sugestoes))
    print(f"✅ Sugestões salvas em {path_sugestoes}")

    gerar_heatmap(matriz_prob, path_heatmap, minas)
    print(f"🖼️ Heatmap salvo em {path_heatmap}")

def main():
    if len(sys.argv) < 2:
        print("❌ Por favor, informe o caminho da pasta como argumento.")
        print("Exemplo: python analisador_preditivo.py dados/8_minas")
        return

    pasta = sys.argv[1]
    arquivo_limp = os.path.join(pasta, "jogadas_limpo.csv")

    if not os.path.exists(arquivo_limp):
        print(f"❌ Arquivo '{arquivo_limp}' não encontrado.")
        return

    df = pd.read_csv(arquivo_limp)
    if "minas" not in df.columns:
        print("❌ Coluna 'minas' não encontrada no CSV.")
        return

    minas = df["minas"].iloc[0]  # todas jogadas são do mesmo tipo
    analisar_grupo(minas, df, pasta)

if __name__ == "__main__":
    main()
