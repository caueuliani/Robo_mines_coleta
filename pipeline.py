import os
import subprocess

PASTA_DADOS = "dados"

# Lista todas as subpastas dentro de 'dados'
subpastas = [os.path.join(PASTA_DADOS, d) for d in os.listdir(PASTA_DADOS) if os.path.isdir(os.path.join(PASTA_DADOS, d))]

if not subpastas:
    print("❌ Nenhuma subpasta encontrada em 'dados'. Execute primeiro o limpar_csv.py.")
    exit()

for pasta in subpastas:
    print(f"\n🚀 Processando pasta: {pasta}")

    # Define variáveis de ambiente para que os scripts saibam qual pasta usar
    os.environ["PASTA_ANALISE"] = pasta  

    # Executa analisador_preditivo.py
    try:
        subprocess.run(["python", "analisador_preditivo.py", pasta], check=True)
        print("✅ analisador_preditivo.py executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar analisador_preditivo.py em {pasta}: {e}")

    # Executa analisar_jogadas.py
    try:
        subprocess.run(["python", "analisar_jogadas.py", pasta], check=True)
        print("✅ analisar_jogadas.py executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar analisar_jogadas.py em {pasta}: {e}")

# 🚀 Após processar tudo, treina modelo ML
print("\n🎯 Treinando modelo de Machine Learning...")

try:
    subprocess.run(["python", "treinar_modelo.py"], check=True)
    print("✅ Modelo treinado com sucesso.")
except subprocess.CalledProcessError as e:
    print(f"❌ Erro ao treinar modelo: {e}")

print("\n✅ Pipeline completo!")
