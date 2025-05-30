import pandas as pd
import numpy as np
import os
import random
import time
from tqdm import tqdm  # ✅ barra de progresso

ARQUIVO_ORIGINAL = "jogadas.csv"
ARQUIVO_SAIDA = "jogadas_simuladas.csv"
META_JOGADAS_POR_MINA = 500  # ✅ ajuste conforme necessidade

if not os.path.exists(ARQUIVO_ORIGINAL):
    print(f"❌ Arquivo '{ARQUIVO_ORIGINAL}' não encontrado.")
    exit()

# Lê o dataset original
df = pd.read_csv(ARQUIVO_ORIGINAL)

# Compatibilidade de colunas
if 'minas' not in df.columns and 'quantidade_bombas' in df.columns:
    df['minas'] = df['quantidade_bombas']

minas_unicas = sorted(df['minas'].unique())

simulacoes = []

print(f"🔍 Gerando simulações para {len(minas_unicas)} quantidades de minas...")

for minas in minas_unicas:
    atual = df[df['minas'] == minas]
    faltam = META_JOGADAS_POR_MINA - len(atual)

    print(f"➡️ Minas {minas}: {len(atual)} jogadas feitas, faltam {max(faltam,0)} para {META_JOGADAS_POR_MINA}")

    for _ in tqdm(range(max(faltam, 0)), desc=f"Simulando {minas} minas"):
        jogada = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(random.randint(1609459200, 1700000000))),  # ✅ datas entre 2021-2023
            "minas": minas,
            "quantidade_bombas": minas,
            "resultado": random.choice(["Vitória", "Derrota"]),
            **{
                f"casa_{i+1}": random.choices(
                    ["💣", "💎", "⬜"],
                    weights=[minas/25, (25-minas)/25, 1]
                )[0]
                for i in range(25)
            }
        }
        simulacoes.append(jogada)

# Transforma em DataFrame
df_simulado = pd.DataFrame(simulacoes)

# Salva
df_simulado.to_csv(ARQUIVO_SAIDA, index=False)
print(f"✅ Simulações salvas em '{ARQUIVO_SAIDA}' com {len(df_simulado)} jogadas.")

# ✅ Log opcional
with open("log_simulacao.txt", "w") as log:
    log.write(f"Simulações: {len(df_simulado)}\n")
    log.write(f"Minas únicas: {minas_unicas}\n")
    log.write(f"Meta por mina: {META_JOGADAS_POR_MINA}\n")
    log.write(f"Arquivo gerado: {ARQUIVO_SAIDA}\n")

print("📝 Log de simulação salvo como 'log_simulacao.txt'")
