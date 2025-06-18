# Importa as bibliotecas necessárias do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os

id_evento = "158353"  # Define o ID do evento a ser buscado

# Configurações para máxima velocidade do navegador
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Caminho do Chrome
chrome_options.add_argument("--headless=new")  # Executa o Chrome em modo headless (sem interface gráfica)
chrome_options.add_argument("--disable-extensions")  # Desativa extensões
chrome_options.add_argument("--disable-gpu")  # Desativa uso de GPU
chrome_options.add_argument("--no-sandbox")  # Desativa sandbox (necessário em alguns ambientes)
chrome_options.add_argument("--disable-plugins")  # Desativa plugins
chrome_options.add_argument("--disable-popup-blocking")  # Desativa bloqueio de popups
chrome_options.add_argument("--disable-notifications")  # Desativa notificações
chrome_options.add_argument("--disable-dev-shm-usage")  # Evita o uso do /dev/shm (memória compartilhada), útil para evitar problemas de espaço em ambientes Linux ou Docker
chrome_options.add_argument("--no-zygote")               # Impede o uso do processo zygote, reduzindo ainda mais a criação de processos
prefs = {"profile.managed_default_content_settings.images": 2}  # Bloqueia carregamento de imagens
chrome_options.add_experimental_option("prefs", prefs)  # Aplica as preferências

service = Service(r"chromedriver.exe")  # Define o caminho do ChromeDriver

inicio = time.time()  # Marca o início da execução
driver = webdriver.Chrome(service=service, options=chrome_options)  # Inicia o navegador com as opções definidas

try:
    driver.get("https://dashboard.fotop.com")  # Acessa a página inicial do dashboard

    load_dotenv()  # Carrega as variáveis do .env

    perm_cookie_name = os.getenv("COOKIE_NAME")
    perm_cookie_value = os.getenv("COOKIE_VALUE")

    # Define o valor do cookie de autenticação
    driver.add_cookie({
        "name": perm_cookie_name,
        "value": perm_cookie_value,
        "domain": "dashboard.fotop.com",
        "path": "/"
    })

    # Monta a URL do evento específico usando o id_evento
    url_evento = f"https://dashboard.fotop.com/eventos/proximos/?busca={id_evento}&pais=31&uf=SP&internacional=nao&marketplace=fotop&vagas=todos"
    driver.get(url_evento)  # Acessa a página do evento

    # Aguarda o botão "Participar" do evento aparecer (até 2 segundos)
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-participar:not([disabled])"))
    )
    botao_participar = driver.find_element(By.CSS_SELECTOR, "button.btn-participar:not([disabled])")  # Seleciona o botão
    driver.execute_script("arguments[0].scrollIntoView();", botao_participar)  # Rola até o botão
    botao_participar.click()  # Clica no botão "Participar"

    # Aguarda a modal abrir (até 5 segundos)
    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "modalTermos").value_of_css_property("display") == "block"
    )

    # Remove a classe d_none do checkbox para torná-lo visível
    chk_termos = driver.find_element(By.ID, "chkTermos")
    driver.execute_script("arguments[0].classList.remove('d_none');", chk_termos)

    # Aguarda o checkbox ficar visível e clicável (até 2 segundos)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "chkTermos")))

    # Agora clica no checkbox
    chk_termos.click()

    # (Opcional) Pega o valor do token c
    c_token = chk_termos.get_attribute("value")
    print(f"Token c: {c_token}")

    # Aguarda o botão "Concordo e quero participar" ficar clicável e clica (até 5 segundos)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "btnParticiparEvento"))
    )
    btn_modal = driver.find_element(By.ID, "btnParticiparEvento")
    btn_modal.click()

    # Aguarda e aceita o alerta, se aparecer
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())  # Espera até 3 segundos por um alerta
        alert = driver.switch_to.alert  # Muda para o alerta
        print(f"Alerta: {alert.text}")  # Mostra o texto do alerta
        alert.accept()  # Aceita o alerta
    except:
        pass  # Se não aparecer alerta, segue normalmente

    # Aguarda a modal fechar (caso não tenha alerta)
    try:
        WebDriverWait(driver, 1).until(
            lambda d: d.find_element(By.ID, "modalTermos").value_of_css_property("display") == "none"
        )
    except:
        pass

finally:
    fim = time.time()  # Marca o fim da execução
    # Finaliza o navegador e exibe mensagem de conclusão
    print("Processo concluído.")
    print(f"Tempo total de execução: {fim - inicio:.2f} segundos")
    driver.quit()  # Fecha o navegador