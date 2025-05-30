import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

PASTA_DADOS = "dados"
MODELO_SAIDA = "modelo_bomba.pkl"

# Preparar dataset
X = []
y = []

print("🔍 Preparando dataset para treino...")

for pasta in os.listdir(PASTA_DADOS):
    caminho = os.path.join(PASTA_DADOS, pasta, "jogadas_limpo.csv")
    if not os.path.exists(caminho):
        continue

    df = pd.read_csv(caminho)
    minas = int(pasta.split("_")[0])  # Ex: "8_minas" → 8

    for _, row in df.iterrows():
        for idx in range(25):
            linha = idx // 5
            coluna = idx % 5
            distancia = np.sqrt((linha - 2) ** 2 + (coluna - 2) ** 2)  # Distância ao centro

            X.append([linha, coluna, distancia, minas])
            y.append(1 if row[f"casa_{idx+1}"] == "💣" else 0)

X = np.array(X)
y = np.array(y)

print(f"✅ Dataset com {len(X)} amostras.")

# Treinamento
print("🌳 Treinando modelo de RandomForestClassifier...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

# Salvar modelo
joblib.dump(modelo, MODELO_SAIDA)
print(f"✅ Modelo salvo como {MODELO_SAIDA}")
