import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options  # Modificamos esta linha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from colorama import init, Fore

# Initialize colorama to work with ANSI escape sequences on Windows
init(autoreset=True)

# Dados de login
login_url = 'https://hibrida.ileva.com.br/sistema/adm/inspectionmodel/edit/id/63'
username = 'suporte03'
password = 'Negaazul1!'

edge_options = Options()  # Modificamos esta linha
edgedriver_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/MicrosoftEdgeDriver.exe'  # Altere para o caminho correto
edge_options.add_argument('--no-sandbox')  # Evita problemas de sandbox no ambiente de testes
edge_options.add_argument('--headless')  # Evita problemas de sandbox no ambiente de testes
# Você pode precisar ajustar algumas opções específicas do Chrome que não são relevantes para o Edge

print("Inicializando o Navegador...")
driver = webdriver.Edge(options=edge_options)  # Modificamos esta linha

# Fazer login no site
print("Autenticando...")
driver.get(login_url)
wait = WebDriverWait(driver, 10)

# Realizar o login no site
print("Adicionando Usuário e Senha no Input...")
username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="ctrl.data.username"]')))
password_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="ctrl.data.password"]') 

username_input.send_keys(username)
password_input.send_keys(password)

# Clicar no botão de login
print("Button Logar...")
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
login_button.click()

print(Fore.RED + "LOGADO !" + Fore.RESET)

# Esperar até que o botão "itemModal" seja clicável
print("Esperar até que o botão 'itemModal' seja clicável...")
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']"))).click()

# Pasta contendo as fotos a serem enviadas
pasta_com_fotos = 'C:/Users/Híbrida/Desktop/1'

# Lista todos os arquivos na pasta
lista_arquivos = os.listdir(pasta_com_fotos)

for arquivo in lista_arquivos:
    caminho_da_imagem = os.path.join(pasta_com_fotos, arquivo)
    descricao = os.path.splitext(arquivo)[0]  # Uses the name of the file (without the extension) as description

    # Enviar a foto
    print(Fore.RED + f"Enviando a Foto: {caminho_da_imagem}" + Fore.RESET)
    input_file = driver.find_element(By.CSS_SELECTOR, "input[type='file'][fileread='ctrl.item.imagem_exemplo']")
    input_file.send_keys(caminho_da_imagem)

    # Aguardar mais alguns segundos para que a foto seja anexada ao modal
    time.sleep(2)

    # Simular o clique no botão "Abrir" da janela de seleção de arquivo (opcional)
    pyautogui.press('enter')

    # Esperar até que o elemento "loading-overlay-content" desapareça da página
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay-content")))

    # Aguardar mais alguns segundos para o processamento adicional (se houver)
    time.sleep(2)

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
    time.sleep(2)

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

# Fechar o navegador
driver.quit()