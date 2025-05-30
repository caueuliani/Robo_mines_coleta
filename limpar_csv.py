import pandas as pd
import os
import subprocess

ARQUIVO_ENTRADA = "jogadas_completas.csv"
PASTA_SAIDA = "dados"

# Verifica se o arquivo de entrada existe
if not os.path.exists(ARQUIVO_ENTRADA):
    print(f"❌ Arquivo '{ARQUIVO_ENTRADA}' não encontrado.")
    exit()

# Lê o CSV original
df = pd.read_csv(ARQUIVO_ENTRADA)

# Remove linhas com campos essenciais ausentes
colunas_obrigatorias = ["timestamp", "minas", "resultado"]
df = df.dropna(subset=colunas_obrigatorias)

# Converte o campo 'minas' para inteiro válido
df["minas"] = pd.to_numeric(df["minas"], errors="coerce").dropna().astype(int)

# Validação das colunas de casas
casas = [f"casa_{i}" for i in range(1, 26)]
if not all(col in df.columns for col in casas):
    print("❌ Colunas de casas de tabuleiro não encontradas.")
    exit()

# Função para validar linha
def linha_valida(row):
    return all(row[f"casa_{i}"] in {"💣", "💎", "⬜"} for i in range(1, 26))

# Aplica a validação
df = df[df.apply(linha_valida, axis=1)].reset_index(drop=True)

# --- Separação por quantidade de minas ---
minas_unicas = sorted(df["minas"].unique())
print(f"✅ Encontradas jogadas com as seguintes quantidades de minas: {minas_unicas}")

for minas in minas_unicas:
    df_subset = df[df["minas"] == minas]
    pasta_destino = os.path.join(PASTA_SAIDA, f"{minas}_minas")
    os.makedirs(pasta_destino, exist_ok=True)
    
    arquivo_saida = os.path.join(pasta_destino, "jogadas_limpo.csv")
    df_subset.to_csv(arquivo_saida, index=False)
    
    print(f"✅ Salvo {len(df_subset)} jogadas válidas em '{arquivo_saida}'.")

print("✅ Separação e limpeza concluídas com sucesso!")

# 🚀 Chama o pipeline automaticamente
try:
    subprocess.run(["python", "pipeline.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Erro ao executar pipeline.py: {e}")
