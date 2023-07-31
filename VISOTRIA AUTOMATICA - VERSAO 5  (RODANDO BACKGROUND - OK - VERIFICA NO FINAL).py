import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import PhotoImage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
import threading

# Initialize colorama to work with ANSI escape sequences on Windows
init(autoreset=True)

def get_login_info():
    root = tk.Tk()
    root.title("Automatizador de Vistoria - Marlon (Ver. 1.5)")
    root.geometry("500x485")  # Definindo as dimensões da janela

    # Adicionando um background com cor específica (#0F1120)
    root.configure(bg="#0F1120")

    # Redimensionando a imagem da logo
    logo_path = "logo.png"  # Substitua pelo caminho da sua logo
    logo_image = tk.PhotoImage(file=logo_path)  # Redimensiona a imagem para 200x200
    logo_label = tk.Label(root, image=logo_image, bg="#0F1120")  # Definindo a cor de fundo do label da logo
    logo_label.pack(pady=10)  # Adicionando espaçamento no topo

    # Criando um frame para agrupar os campos de URL, usuário e senha
    input_frame = tk.Frame(root, bg="#0F1120")  # Definindo a cor de fundo do frame
    input_frame.pack(padx=10, pady=10)  # Adicionando espaçamento interno

    url_label = tk.Label(input_frame, text="URL da Vistoria:", bg="#0F1120", fg="#FFFFFF")  # Definindo a cor de fundo e do texto
    url_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)  # Alinhando o label à esquerda, adding padding

    url_entry = tk.Entry(input_frame)
    url_entry.grid(row=0, column=1, padx=5, pady=5)  # Adicionando espaçamento à direita, adding padding

    username_label = tk.Label(input_frame, text="Usuario:", bg="#0F1120", fg="#FFFFFF")  # Definindo a cor de fundo e do texto
    username_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)  # Alinhando o label à esquerda, adding padding

    username_entry = tk.Entry(input_frame)
    username_entry.grid(row=1, column=1, padx=5, pady=5)  # Adicionando espaçamento à direita, adding padding

    password_label = tk.Label(input_frame, text="Senha:", bg="#0F1120", fg="#FFFFFF")  # Definindo a cor de fundo e do texto
    password_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)  # Alinhando o label à esquerda, adding padding

    password_entry = tk.Entry(input_frame, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)  # Adicionando espaçamento à direita, adding padding

    # Adicionamos um widget 'scrolledtext' para exibir as informações do console
    global console_text
    console_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=50)
    console_text.pack(pady=10)  # Add vertical spacing before the scrolledtext area

    def submit_login_info():
        url = url_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # Usamos threading para executar a função em uma thread separada
        threading.Thread(target=process_login, args=(url, username, password)).start()
        
    # Adicionando espaçamento entre o botão "Enviar" e a área de texto
    submit_button = tk.Button(root, text="Enviar", command=submit_login_info, padx=10, pady=5)  # Adicionando padding ao botão
    submit_button.pack(pady=10)  # Add vertical spacing after the button
    
    # Adicionando um rodapé com a mesma cor de fundo e texto branco
    footer_label = tk.Label(root, text="Criado por Marlon - Versão 1.5", bg="#0F1120", fg="#FFFFFF")
    footer_label.pack(pady=10)

    root.mainloop()

# Redirecionar a saída do console para o widget 'console_text'
def console_print(text):
    global console_text
    console_text.insert(tk.END, text + '\n')
    console_text.see(tk.END)  # Rolagem automática para a última linha

print = console_print  # Substituímos a função 'print' para que imprima no widget

def process_login(url, username, password):
    # Redirecionar a saída do console para o widget 'console_text'
    def console_print(text):
        console_text.insert(tk.END, text + '\n')
        console_text.see(tk.END)  # Rolagem automática para a última linha

    print = console_print

    # Configurar as opções do Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # Evita problemas de sandbox no ambiente de testes
    chrome_options.add_argument('--headless')  # Enable headless mode
    chrome_options.add_argument('--log-level=3')

    # Passar os cookies da sessão para o WebDriver
    print("Inicializando o Navegador...")
    driver = webdriver.Chrome(options=chrome_options)

    # Fazer login no site
    print("Autenticando...")
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Realizar o login no site
    # print("Adicionando Usuário e Senha no Input...")
    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="ctrl.data.username"]')))
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="ctrl.data.password"]') 

    username_input.send_keys(username)
    password_input.send_keys(password)

    # Clicar no botão de login
    # print("Button Logar...")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    print("LOGADO !")
    
    # Esperar até que o botão "itemModal" seja clicável
    # print("Esperar até que o botão 'itemModal' seja clicável...")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click*='ctrl.itemModal']"))).click()

    # Pasta contendo as fotos a serem enviadas
    pasta_com_fotos = filedialog.askdirectory(title="Selecione a Pasta com as Fotos")

    # Lista todos os arquivos na pasta
    lista_arquivos = os.listdir(pasta_com_fotos)

    # Loop through the files in the folder and upload photos with descriptions
    for arquivo in lista_arquivos:
        caminho_da_imagem = os.path.join(pasta_com_fotos, arquivo)
        descricao = os.path.splitext(arquivo)[0]  # Uses the name of the file (without the extension) as description

        # Upload the photo and add description
        upload_photo_with_description(driver, None, caminho_da_imagem, descricao)
        
    def console_print(text):
        console_text.insert(tk.END, text + '\n')
        console_text.see(tk.END)  # Rolagem automática para a última linha

    print = console_print
        
def upload_photo_with_description(driver, item_name, caminho_da_imagem, descricao):

    # Enviar a foto
    print(f"Enviando a Foto: {caminho_da_imagem}")    
    input_file = driver.find_element(By.CSS_SELECTOR, "input[type='file'][fileread='ctrl.item.imagem_exemplo']")
    input_file.send_keys(caminho_da_imagem)


    # Esperar até que o elemento "loading-overlay-content" desapareça da página
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-overlay-content")))

    # Aguardar mais alguns segundos para o processamento adicional (se houver)

    # Codigo JavaScript para adicionar descricao e tornar foto obrigatoria
    print(f"Adicionando Descricao: {descricao}")
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
    # Envia o formulário da modal usando JavaScript
    # print("Enviando Fotos...")
    script = """
        var modalFooter = document.querySelector('.modal-dialog .modal-footer');
        var salvarButton = modalFooter.querySelector('button[type="submit"]');
        salvarButton.click();
    """
    driver.execute_script(script)

    print("FOTO ENVIADA !")
    time.sleep(5)

    pass

# Inicia a interface gráfica para solicitar informações de login
get_login_info()