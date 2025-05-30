import pandas as pd
import os

ARQUIVO_REAL = "jogadas.csv"
ARQUIVO_SIMULADO = "jogadas_simuladas.csv"
ARQUIVO_MESTRE = "jogadas_completas.csv"

# Confere se os arquivos existem
if not os.path.exists(ARQUIVO_REAL):
    print(f"❌ Arquivo '{ARQUIVO_REAL}' não encontrado.")
    exit()

if not os.path.exists(ARQUIVO_SIMULADO):
    print(f"❌ Arquivo '{ARQUIVO_SIMULADO}' não encontrado.")
    exit()

# Carrega os datasets
df_real = pd.read_csv(ARQUIVO_REAL)
df_fake = pd.read_csv(ARQUIVO_SIMULADO)

# Mescla os dois
df_total = pd.concat([df_real, df_fake], ignore_index=True)

# Embaralha as linhas para evitar viés
df_total = df_total.sample(frac=1, random_state=42).reset_index(drop=True)

# Salva o dataset completo
df_total.to_csv(ARQUIVO_MESTRE, index=False)

print(f"✅ Dataset mesclado salvo em '{ARQUIVO_MESTRE}' com {len(df_total)} jogadas.")
