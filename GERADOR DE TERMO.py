from io import BytesIO
import requests
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
            resultado_label.config(text="Termo gerado com sucesso!")
        else:
            resultado_label.config(
                text="Erro: Código de status HTTP inválido.")
    except requests.exceptions.RequestException as e:
        resultado_label.config(text=f"Erro: {e}")


root = Tk()
root.title("Gerador de Termo - API")

# Definindo estilo personalizado
style = ttk.Style(root)
style.theme_create("meu_estilo", parent="alt", settings={
    "TLabel": {"configure": {"background": "white", "foreground": "black", "font": ("Arial", 16)}},
    "TEntry": {"configure": {"font": ("Arial", 16)}},
    "TButton": {"configure": {"font": ("Arial", 16), "borderwidth": 2, "relief": "raised"}},
})
style.theme_use("meu_estilo")

# Definindo tamanho e posição da janela
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

# Definindo cores de background
background = ttk.Frame(root, style="TLabel")
background.place(relwidth=1, relheight=1)

# Adicionando widgets
# Substitua o URL pelo seu logotipo
logo_url = "https://cdn-fra1.ileva.com.br/hibrida/sistema/7b2c7cec6cf2aebb59b66e727cf8d278.jpeg"
logo_response = requests.get(logo_url)
logo_image = Image.open(BytesIO(logo_response.content))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttk.Label(background, image=logo_photo)
logo_label.pack(side=TOP, padx=10, pady=10)

subdominio_label = ttk.Label(background, text="Associação:")
subdominio_label.pack(pady=10)
subdominio_entry = ttk.Entry(background)
subdominio_entry.pack(pady=10)

id_label = ttk.Label(background, text="ID do Termo:")
id_label.pack(pady=10)
id_entry = ttk.Entry(background)
id_entry.pack(pady=10)

botao = ttk.Button(background, text="Gerar Novo Termo",
                   command=fazer_requisicao)
botao.pack(pady=10)

resultado_label = ttk.Label(background, text="")
resultado_label.pack(pady=10)

# Criando o rodapé
rodape = ttk.Frame(root, borderwidth=1, relief="solid")
rodape.place(relwidth=1, relheight=0.1, rely=0.9)

# Adicionando a mensagem de versão no rodapé
versao_label = ttk.Label(
    rodape, text="Criado por Marlon - Suporte Ileva - Versão 1.0", font=("Arial", 10))
versao_label.pack(side=LEFT, padx=20, pady=10)

root.mainloop()
