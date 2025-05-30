import pandas as pd
import numpy as np
import joblib
import os

# --- Carrega o modelo treinado ---
MODELO_PATH = "modelo_bomba.pkl"
if not os.path.exists(MODELO_PATH):
    print("❌ Modelo não encontrado! Execute primeiro o treinar_modelo.py.")
    exit()

modelo = joblib.load(MODELO_PATH)

# --- Recebe a quantidade de minas da jogada ---
try:
    minas = int(input("🪙 Informe a quantidade de minas no jogo atual (1 a 24): "))
    if minas < 1 or minas > 24:
        print("❌ Quantidade inválida! Deve ser entre 1 e 24.")
        exit()
except ValueError:
    print("❌ Entrada inválida! Deve ser um número.")
    exit()

# --- Gera as 25 entradas de previsão com novas features ---
print(f"\n🔮 Prevendo chances de bomba para as 25 casas, com {minas} minas...")

linhas = []
colunas = []
distancias = []

for idx in range(25):
    linha = idx // 5
    coluna = idx % 5
    distancia = np.sqrt((linha - 2)**2 + (coluna - 2)**2)  # distância euclidiana ao centro
    linhas.append(linha)
    colunas.append(coluna)
    distancias.append(distancia)

entradas = pd.DataFrame({
    "linha": linhas,
    "coluna": colunas,
    "distancia": distancias,
    "minas": [minas] * 25
})

# --- Faz as previsões ---
probabilidades = modelo.predict_proba(entradas)[:, 1]  # Prob de bomba

# --- Mostra resultados ---
print("\n📊 Probabilidades de bomba por casa:")
for i, prob in enumerate(probabilidades):
    print(f"Casa {i+1:2}: {prob * 100:.2f}% de chance de bomba")

# --- Sugere as 5 melhores casas ---
indices_melhores = np.argsort(probabilidades)[:5]
print("\n✅ Sugestão: as 5 casas mais seguras para clicar:")

for idx in indices_melhores:
    prob = probabilidades[idx] * 100
    print(f"👉 Casa {idx+1:2} → {prob:.2f}% de chance de bomba")
