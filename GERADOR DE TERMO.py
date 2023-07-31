from io import BytesIO
import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def fazer_requisicao():
    subdominio = subdominio_entry.get()
    id = id_entry.get()
    url = f"https://{subdominio}.ileva.com.br/api/indicacao/gerarProposta/{id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            resultado_label.config(text=response.text)
            resultado_label.config(text="Termo gerado com sucesso!", foreground="white")  # Set the text color to white
            clear_input_fields()  # Call the function to clear the input fields
        else:
            resultado_label.config(text="Erro: Código de status HTTP inválido.", foreground="white")  # Set the text color to white
    except requests.exceptions.RequestException as e:
        resultado_label.config(text=f"Erro: {e}", foreground="white")  # Set the text color to white

def clear_input_fields():
    subdominio_entry.delete(0, END)
    id_entry.delete(0, END)

root = Tk()
root.title("Gerador de Termos - Marlon (Ver. 1.2)")

# Definindo estilo personalizado
style = ttk.Style(root)
style.theme_create("meu_estilo", parent="alt", settings={
    "TLabel": {"configure": {"background": "#0F1120", "foreground": "white", "font": ("Arial", 16)}},  # Set the background color to "#0F1120" and text color to white
    "TEntry": {"configure": {"font": ("Arial", 16)}},
    "TButton": {"configure": {"font": ("Arial", 16), "borderwidth": 2, "relief": "raised"}},
    "TFrame": {"configure": {"background": "#0F1120"}},  # Set the background color to "#0F1120" for all frames
})
style.theme_use("meu_estilo")

# Definindo tamanho e posição da janela
root.geometry("600x450")
root.eval('tk::PlaceWindow . center')

# Definindo cores de background
background = ttk.Frame(root, style="TLabel")
background.place(relwidth=1, relheight=1)

# Redimensionando a imagem da logo
logo_path = "logo.png"  # Substitua pelo caminho da sua logo
logo_image = tk.PhotoImage(file=logo_path)  # Redimensiona a imagem para 200x200
logo_label = tk.Label(root, image=logo_image, bg="#0F1120")  # Definindo a cor de fundo do label da logo
logo_label.pack(pady=10)  # Adicionando espaçamento no topo

logo_label = ttk.Label(background, image=logo_image)
logo_label.pack(side=TOP, padx=10, pady=10)

subdominio_label = ttk.Label(background, text="Associação:")
subdominio_label.pack(pady=10)
subdominio_entry = ttk.Entry(background)
subdominio_entry.pack(pady=10)

id_label = ttk.Label(background, text="ID do Termo:")
id_label.pack(pady=10)
id_entry = ttk.Entry(background)
id_entry.pack(pady=10)

botao = ttk.Button(background, text="Gerar Novo Termo", command=fazer_requisicao)
botao.pack(pady=10)

resultado_label = ttk.Label(background, text="", foreground="white")  # Set the text color to white
resultado_label.pack(pady=10)

# Criando o rodapé
rodape = ttk.Frame(root, style="TFrame", borderwidth=1, relief="solid")  # Set the background color to "#0F1120" for the footer frame
rodape.place(relwidth=1, relheight=0.1, rely=0.9)

# Adicionando a mensagem de versão no rodapé
versao_label = ttk.Label(
    rodape, text="Criado por Marlon - Versão 1.2", font=("Arial", 10), foreground="white", anchor="center")  # Set the text color to white and anchor the text to the center
versao_label.pack(side=LEFT, fill="both", expand=True, padx=20, pady=10)  # Use fill="both" and expand=True to center the label text

root.mainloop()