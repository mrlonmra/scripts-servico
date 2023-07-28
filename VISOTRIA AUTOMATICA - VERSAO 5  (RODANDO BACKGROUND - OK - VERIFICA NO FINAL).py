import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore

# Initialize colorama to work with ANSI escape sequences on Windows
init(autoreset=True)

# Dados de login
login_url = 'https://hibrida.ileva.com.br/sistema/adm/inspectionmodel/edit/id/46'
username = 'suporte03'
password = 'Negaazul1!'

# Configurar as opções do Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # Evita problemas de sandbox no ambiente de testes
chrome_options.add_argument('executable_path=caminho/para/o/chromedriver.exe')  # Caminho do Chrome WebDriver
chrome_options.add_argument('--headless')  # Enable headless mode
chrome_options.add_argument('--log-level=3')

# Passar os cookies da sessão para o WebDriver
print(Fore.RED + "Inicializando o Navegador..." + Fore.RESET)
driver = webdriver.Chrome(options=chrome_options)

# Fazer login no site
print(Fore.RED + "Autenticando..." + Fore.RESET)
driver.get(login_url)
wait = WebDriverWait(driver, 10)

# Realizar o login no site
print(Fore.RED + "Adicionando Usuário e Senha no Input..." + Fore.RESET)
username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="ctrl.data.username"]')))
password_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="ctrl.data.password"]') 

username_input.send_keys(username)
password_input.send_keys(password)

# Clicar no botão de login
print(Fore.RED + "Button Logar..." + Fore.RESET)
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()

print(Fore.RED + "LOGADO !" + Fore.RESET)

# Esperar até que o botão "itemModal" seja clicável
print(Fore.RED + "Esperar até que o botão 'itemModal' seja clicável..." + Fore.RESET)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']"))).click()

# Pasta contendo as fotos a serem enviadas
pasta_com_fotos = 'C:/Users/Híbrida/Desktop/1'

# Lista todos os arquivos na pasta
lista_arquivos = os.listdir(pasta_com_fotos)

def upload_photo_with_description(item_name, caminho_da_imagem, descricao):
    # Enviar a foto
    print(Fore.RED + f"Enviando a Foto: {caminho_da_imagem}" + Fore.RESET)
    input_file = driver.find_element(By.CSS_SELECTOR, "input[type='file'][fileread='ctrl.item.imagem_exemplo']")
    input_file.send_keys(caminho_da_imagem)

    # Aguardar mais alguns segundos para que a foto seja anexada ao modal

    # Simular o clique no botão "Abrir" da janela de seleção de arquivo (opcional)
    # pyautogui.press('enter')

    # Esperar até que o elemento "loading-overlay-content" desapareça da página
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay-content")))

    # Aguardar mais alguns segundos para o processamento adicional (se houver)

    # Codigo JavaScript para adicionar descricao e tornar foto obrigatoria
    print(Fore.YELLOW + f"Adicionando Descricao: {descricao}" + Fore.RESET)
    script = """
        var checkbox = document.getElementById('required');
        var scope = angular.element(checkbox).scope();
        scope.$apply(function () {
            scope.ctrl.item.required = "1";
        });
        angular.element(checkbox).triggerHandler('change');

        // Set the description using JavaScript
        var input_descricao = document.querySelector('input[ng-model="ctrl.item.descricao"]');
        input_descricao.setAttribute('value', arguments[0]);
        var event = new Event('input', { bubbles: true });
        input_descricao.dispatchEvent(event);        

        // Trigger the AngularJS digest cycle (if necessary)
        var elemScope = angular.element(input_descricao).scope();
        if (elemScope) {
            elemScope.$apply();
        }
    """
    driver.execute_script(script, descricao)

    # Aguarda alguns segundos

    # Envia o formulário da modal usando JavaScript
    print(Fore.RED + "Enviando Formulario..." + Fore.RESET)

    script = """
        var modalFooter = document.querySelector('.modal-dialog .modal-footer');
        var salvarButton = modalFooter.querySelector('button[type="submit"]');
        salvarButton.click();
    """
    driver.execute_script(script)

    print(Fore.YELLOW + "FOTO ENVIADA !" + Fore.RESET)

    # Aguardar mais alguns segundos para que a foto seja anexada ao modal
    time.sleep(5)

# Loop through the files in the folder and upload photos with descriptions
for arquivo in lista_arquivos:
    caminho_da_imagem = os.path.join(pasta_com_fotos, arquivo)
    descricao = os.path.splitext(arquivo)[0]  # Uses the name of the file (without the extension) as description

    # Upload the photo and add description
    upload_photo_with_description(None, caminho_da_imagem, descricao)

    # Check if the element "Sem imagem" exists within the "panel-body"
    sem_imagem_elements = driver.find_elements(By.CSS_SELECTOR, "div.panel-body p.ng-scope")
    sem_imagem_exists = any(element.text.strip() == "Sem imagem" for element in sem_imagem_elements)

    if sem_imagem_exists:
        # Retrieve the item name from the "panel-title"
        item_name_element = driver.find_element(By.CSS_SELECTOR, "div.panel-heading h4.panel-title")
        item_name = item_name_element.text.strip()

        if item_name == descricao:
            # Print a message about re-sending the photo
            print(Fore.YELLOW + f"A foto do item '{item_name}' não foi enviada. Reenviando a Foto: {caminho_da_imagem}" + Fore.RESET)

            # Repeat the photo upload process for the item with the same description
            upload_photo_with_description(item_name, caminho_da_imagem, descricao)
        else:
            print(Fore.YELLOW + f"Aviso: O item '{item_name}' não corresponde ao nome do arquivo. Nenhuma foto será enviada para este item." + Fore.RESET)

# Fechar o navegador
driver.quit()