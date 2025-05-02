import pandas as pd
import numpy as np
import os

ARQUIVO_LIMPO = "jogadas_limpo.csv"
PASTA_SAIDA = "analises_por_minas"
os.makedirs(PASTA_SAIDA, exist_ok=True)

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

def analisar_grupo(minas, grupo_df):
    print(f"\n🔎 Analisando {len(grupo_df)} jogadas com {minas} minas...")
    matriz_bombas = atualizar_matriz(inicializar_matriz(), grupo_df)
    matriz_prob = calcular_probabilidades(matriz_bombas, len(grupo_df))

    path_base = os.path.join(PASTA_SAIDA, f"minas_{minas}")
    matriz_bombas.to_csv(f"{path_base}_contagem.csv")
    matriz_prob.to_csv(f"{path_base}_probabilidades.csv")

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

    with open(f"{path_base}_melhores_casas.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sugestoes))

def main():
    if not os.path.exists(ARQUIVO_LIMPO):
        print("❌ Arquivo jogadas_limpo.csv não encontrado.")
        return

    df = pd.read_csv(ARQUIVO_LIMPO)
    if "minas" not in df.columns:
        print("❌ Coluna 'minas' não encontrada no CSV.")
        return

    grupos = df.groupby("minas")
    print(f"📊 Analisando {len(df)} jogadas em {len(grupos)} grupos de minas...")

    for minas, grupo in grupos:
        analisar_grupo(minas, grupo)

if __name__ == "__main__":
    main()
