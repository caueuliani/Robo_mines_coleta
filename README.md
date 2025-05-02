# 🤖 Bot de Análise para Mines (BCH.games)

Este projeto coleta jogadas do jogo Mines (site [BCH.games](https://bch.games)), analisa as jogadas realizadas e sugere as melhores casas para clicar com base em estatísticas passadas. Ideal para uso pessoal ou futura adaptação para bot de Telegram.

---

## 📁 Estrutura do Projeto

- `coletor.py`: Script principal que coleta jogadas enquanto você joga manualmente.
- `limpar_csv.py`: Filtra jogadas inválidas e gera o arquivo `jogadas_limpo.csv`.
- `analisador_preditivo.py`: Atualiza uma matriz 5x5 com as probabilidades de bomba por casa.
- `analisar_jogadas.py`: Gera um heatmap visual e um resumo estatístico das jogadas.
- `jogadas.csv`: Arquivo com todas as jogadas brutas coletadas.
- `jogadas_limpo.csv`: Arquivo com jogadas filtradas e válidas.
- `matriz_probabilidades.csv`: Probabilidades normalizadas de bomba por casa.
- `heatmap_jogadas.csv`: Contagem e porcentagem de bombas e diamantes por casa.
- `melhores_casas.txt`: Sugestão das casas com menor chance de bomba.
- `heatmap_bombas.png` e `heatmap_diamantes.png`: Visualizações das probabilidades.

---

## 🚀 Como Usar

1. **Rode o coletor** e jogue manualmente:
   ```bash
   python coletor.py
   ```

2. **Após jogar algumas partidas, rode o script de limpeza:**
   ```bash
   python limpar_csv.py
   ```

3. **Para visualizar os melhores cliques com heatmap:**
   ```bash
   python analisar_jogadas.py
   ```

---

## 🔧 Requisitos

- Python 3.9+
- Pacotes:
  - `pandas`
  - `numpy`
  - `selenium`
  - `webdriver-manager`
  - `matplotlib`
  - `seaborn`

Instale todos com:
```bash
pip install -r requirements.txt
```

---

## 💡 Futuras melhorias

- Adaptar para bot de Telegram.
- Análises separadas por quantidade de minas.
- Sugestões em tempo real.

---

## ⚠️ Aviso

Este projeto é apenas para fins educacionais e estatísticos. **Use com responsabilidade.**
