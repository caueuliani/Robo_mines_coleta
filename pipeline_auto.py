import subprocess
import os
import pandas as pd

# Passos do pipeline completo

def gerar_simulacao():
    print("🎲 Gerando jogadas simuladas...")
    subprocess.run(["python", "gerar_simulacoes.py"], check=True)
    print("✅ Simulação concluída.")

def mesclar_datasets():
    print("🗂️ Mesclando datasets real + simulado...")

    ARQUIVO_REAL = "jogadas.csv"
    ARQUIVO_SIMULADO = "jogadas_simuladas.csv"
    ARQUIVO_MESTRE = "jogadas_completas.csv"

    if not os.path.exists(ARQUIVO_REAL) or not os.path.exists(ARQUIVO_SIMULADO):
        print("❌ Arquivos de entrada não encontrados!")
        exit()

    df_real = pd.read_csv(ARQUIVO_REAL)
    df_fake = pd.read_csv(ARQUIVO_SIMULADO)

    df_total = pd.concat([df_real, df_fake], ignore_index=True)
    df_total = df_total.sample(frac=1, random_state=42).reset_index(drop=True)
    df_total.to_csv(ARQUIVO_MESTRE, index=False)

    print(f"✅ Dataset mesclado salvo como '{ARQUIVO_MESTRE}' com {len(df_total)} jogadas.")

def limpar_dados():
    print("🧹 Limpando dados...")

    ARQUIVO_ENTRADA = "jogadas_completas.csv"
    ARQUIVO_DESTINO = "jogadas.csv"  # sobrescreve ou cria novo jogadas.csv

    if os.path.exists(ARQUIVO_DESTINO):
        os.remove(ARQUIVO_DESTINO)

    os.rename(ARQUIVO_ENTRADA, ARQUIVO_DESTINO)
    subprocess.run(["python", "limpar_csv.py"], check=True)
    print("✅ Dados limpos.")


def executar_pipeline():
    print("🚀 Executando pipeline de análise...")
    subprocess.run(["python", "pipeline.py"], check=True)
    print("✅ Pipeline completo.")

if __name__ == "__main__":
    print("\n⚙️ Iniciando pipeline automático...")

    gerar_simulacao()
    mesclar_datasets()
    limpar_dados()
    executar_pipeline()

    print("\n🏁 Pipeline automático finalizado com sucesso!")
