from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


# Dados de login
login_url = 'https://hibrida.ileva.com.br/sistema/adm/inspectionmodel/edit/id/32'
username = 'suporte03'
password = 'Negaazul1!'

# Configurar as opções do Chrome WebDriver
chrome_options = Options()
chromedriver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
chrome_options.add_argument('--no-sandbox')  # Evita problemas de sandbox no ambiente de testes
chrome_options.add_argument('executable_path=caminho/para/o/chromedriver.exe')  # Caminho do Chrome WebDriver

# Passar os cookies da sessão para o WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Realizar o login no site
driver.get(login_url)
wait = WebDriverWait(driver, 10)

# Preencher os campos de login e senha e fazer o login
username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="ctrl.data.username"]')))
password_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="ctrl.data.password"]')

username_input.send_keys(username)
password_input.send_keys(password)

# Clicar no botão de login
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()

# Verificar se o login foi bem-sucedido (opcional)
if 'Seja bem-vindo' not in driver.page_source:
    print("Erro: A autenticação falhou.")
else:
    print("Autenticação bem-sucedida.")

wait = WebDriverWait(driver, 10)

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']"))).click()

# Encontrar e preencher o campo de descrição
descricao = "BATERIA - MARCA"
input_descricao = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[ng-model='ctrl.item.descricao']")))
input_descricao.clear()
input_descricao.send_keys(descricao)

# Encontrar o campo de seleção de arquivo da foto e enviar o caminho da imagem
caminho_da_imagem = 'C:/Users/Híbrida/Desktop/1.jpeg'
input_file = driver.find_element(By.CSS_SELECTOR, "input[type='file'][fileread='ctrl.item.imagem_exemplo']")
input_file.send_keys(caminho_da_imagem)

# Simular o clique no botão "Abrir" da janela de seleção de arquivo
pyautogui.press('enter')

# Aguardar um curto intervalo para que a imagem seja enviada
driver.implicitly_wait(1)


# Esperar até que o elemento "loading-overlay-content" desapareça da página
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay-content")))

# Aguardar mais alguns segundos para o processamento adicional (se houver)
driver.implicitly_wait(5)

# Fechar o navegador
driver.quit()
