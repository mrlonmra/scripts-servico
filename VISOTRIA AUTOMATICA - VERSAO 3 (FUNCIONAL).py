import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

# Dados de login
login_url = 'https://hibrida.ileva.com.br/sistema/adm/inspectionmodel/edit/id/34'
username = 'suporte03'
password = 'Negaazul1!'

# Configurar as opções do Chrome WebDriver
chrome_options = Options()
chromedriver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
chrome_options.add_argument('--no-sandbox')  # Evita problemas de sandbox no ambiente de testes
chrome_options.add_argument('executable_path=caminho/para/o/chromedriver.exe')  # Caminho do Chrome WebDriver

# Passar os cookies da sessão para o WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Passar os cookies da sessão para o WebDriver
driver.get(login_url)
wait = WebDriverWait(driver, 10)

# Realizar o login no site
username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="ctrl.data.username"]')))
password_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="ctrl.data.password"]')

username_input.send_keys(username)
password_input.send_keys(password)

# Clicar no botão de login
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']"))).click()

# Pasta contendo as fotos a serem enviadas
pasta_com_fotos = 'C:/Users/Híbrida/Desktop/1'

# Lista todos os arquivos na pasta
lista_arquivos = os.listdir(pasta_com_fotos)

# Loop para enviar cada foto
for arquivo in lista_arquivos:
    caminho_da_imagem = os.path.join(pasta_com_fotos, arquivo)
    descricao = os.path.splitext(arquivo)[0]  # Usa o nome do arquivo (sem a extensão) como descrição

    # Preenche a descrição com o nome do arquivo
    input_descricao = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[ng-model='ctrl.item.descricao']")))
    input_descricao.clear()
    input_descricao.send_keys(descricao)

    # Enviar a foto
    input_file = driver.find_element(By.CSS_SELECTOR, "input[type='file'][fileread='ctrl.item.imagem_exemplo']")
    input_file.send_keys(caminho_da_imagem)

    # Aguardar mais alguns segundos para que a foto seja anexada ao modal
    time.sleep(3)

    # Simular o clique no botão "Abrir" da janela de seleção de arquivo (opcional)
    pyautogui.press('enter')

    # Esperar até que o elemento "loading-overlay-content" desapareça da página
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay-content")))

    # Aguardar mais alguns segundos para o processamento adicional (se houver)
    time.sleep(5)

    # Clicar no botão para adicionar outra foto
    modal_button = driver.find_element(By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']")
    modal_button.click()

    # Aguardar mais alguns segundos para que a foto seja anexada ao modal
    time.sleep(3)

# Fechar o navegador
driver.quit()