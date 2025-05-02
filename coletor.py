import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------- Funcoes auxiliares -------------------------

def inicializar_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://bch.games/account/settings")
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")
    time.sleep(10)  # tempo para login manual
    return driver

def check_game_over(driver):
    try:
        mult = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="sc-jznrGB dSGwfN"]/div[1]//a[@class="sc-gdZYDh fszAEG"]'))
        )
        text = mult.text.strip()
        color = mult.value_of_css_property('color')
        if text == "x0.00": return "Derrota"
        elif "119, 255, 168" in color: return "Vitória"
        return "Em andamento"
    except: return "Erro ao verificar"

def get_seed_value(driver, label_text):
    try:
        label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//label[text()="{label_text}"]')))
        return label.find_element(By.XPATH, 
            './ancestor::div[@class="sc-WwxRR jDcWFc"]//div[@class="sc-hLMZRY xjPGZ"]'
            '//div[@class="sc-bWxZAa lozsED"]//div[@class="sc-kcdLor dSTEgF"]'
        ).text.strip()
    except: return "erro"

def get_nonce_value(driver):
    try:
        label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Nonce"]')))
        return label.find_element(By.XPATH, 
            './ancestor::div[@class="sc-WwxRR jDcWFc"]//div[@class="sc-hLMZRY xjPGZ"]'
            '//input[@class="sc-jwqMsZ ezUapy"]').get_attribute('value')
    except: return "erro"

def get_board_state(driver):
    try:
        grid = driver.find_element(By.XPATH, '//div[contains(@class, "sc-ewMzwg")]')
        cells = grid.find_elements(By.XPATH, './div[contains(@class, "sc-gnlKGm")]')
        board = []
        for cell in cells:
            try:
                if cell.find_element(By.XPATH, './/div[contains(@class, "sc-bCCZMN")]').is_displayed():
                    board.append('💎')
                    continue
            except: pass
            try:
                if cell.find_element(By.XPATH, './/div[contains(@class, "sc-ggPeai")]').is_displayed():
                    board.append('💣')
                    continue
            except: pass
            board.append('⬜')
        return board
    except: return []

def contar_bombas(tabuleiro):
    return tabuleiro.count('💣')

def imprimir_tabuleiro(tabuleiro):
    print("\n🧩 Tabuleiro:")
    for i in range(0, 25, 5):
        print(' '.join(tabuleiro[i:i+5]))

def salvar_dados_csv(dados_atuais, caminho="jogadas.csv"):
    nova_jogada = pd.DataFrame([dados_atuais])
    if os.path.exists(caminho):
        df_existente = pd.read_csv(caminho)
        df_final = pd.concat([df_existente, nova_jogada], ignore_index=True)
    else:
        df_final = nova_jogada
    df_final.to_csv(caminho, index=False)

# ------------------------- Execução principal -------------------------

def main():
    driver = inicializar_driver()
    try:
        while True:
            input("\n✅ Jogue uma rodada e pressione [Enter] para coletar...")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Salvar HTML
            with open("pagina_apos_jogada.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            resultado = check_game_over(driver)
            print(f"✅ Resultado: {resultado}")

            url = driver.current_url
            minas = url.split("mines=")[1].split("&")[0] if "mines=" in url else "desconhecido"

            try:
                minas = int(minas)
            except:
                minas = -1

            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)

            tabuleiro = get_board_state(driver)
            imprimir_tabuleiro(tabuleiro)
            qtd_bombas = contar_bombas(tabuleiro)

            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[starts-with(text(), "x") and contains(text(), ".")]'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Client seed"]')))
                time.sleep(2)
            except:
                print("❌ Erro ao abrir modal.")
                continue

            client = get_seed_value(driver, 'Client seed')
            server = get_seed_value(driver, 'Server seed')
            nonce = get_nonce_value(driver)

            try:
                ActionChains(driver).move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()
                ActionChains(driver).move_by_offset(10, 10).click().perform()
                time.sleep(1)
            except:
                pass

            jogada = {
                "timestamp": timestamp,
                "minas": minas,
                "quantidade_bombas": qtd_bombas,
                "resultado": resultado,
                "server_seed": server,
                "client_seed": client,
                "nonce": nonce,
                **{f"casa_{i+1}": tabuleiro[i] for i in range(25)}
            }
            salvar_dados_csv(jogada)
            print("\n✅ Rodada salva!")

    except KeyboardInterrupt:
        print("\n⛔ Encerrando coleta.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
