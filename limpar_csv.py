import pandas as pd
import os
import subprocess

# Caminhos dos arquivos
ARQUIVO_ENTRADA = "jogadas.csv"
ARQUIVO_SAIDA = "jogadas_limpo.csv"

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
df["minas"] = pd.to_numeric(df["minas"], errors="coerce")
df = df.dropna(subset=["minas"])
df["minas"] = df["minas"].astype(int)

# Validação das colunas de casas
casas = [f"casa_{i}" for i in range(1, 26)]
if not all(col in df.columns for col in casas):
    print("❌ Colunas de casas de tabuleiro não encontradas.")
    exit()

# Remove linhas inválidas nas casas (devem ter 💣, 💎 ou ⬜)
def linha_valida(row):
    valores = row[casas].tolist()
    return len(valores) == 25 and all(val in ["💣", "💎", "⬜"] for val in valores)

df = df[df.apply(linha_valida, axis=1)]

# Reseta o índice
df.reset_index(drop=True, inplace=True)

# Salva o novo CSV limpo
df.to_csv(ARQUIVO_SAIDA, index=False)
print(f"✅ CSV limpo salvo em '{ARQUIVO_SAIDA}' com {len(df)} jogadas válidas.")

# Roda os scripts em sequência
for script in ["analisador_preditivo.py", "analisar_jogadas.py"]:
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script}: {e}")
