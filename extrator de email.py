import re
import tkinter as tk
from tkinter import filedialog

def extrair_emails(texto):
    padrao_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails_encontrados = re.findall(padrao_email, texto)
    emails_unicos = list(set(emails_encontrados))
    return emails_unicos

def extrair_e_salvar():
    texto = texto_input.get("1.0", tk.END)
    emails = extrair_emails(texto)
    
    if not emails:
        resultado_label.config(text="Nenhum e-mail encontrado.")
        return
    
    arquivo_salvar = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
    if arquivo_salvar:
        with open(arquivo_salvar, 'w') as file:
            for email in emails:
                file.write(email + "\n")
        resultado_label.config(text=f"E-mails extraídos e salvos em {arquivo_salvar}.")
    else:
        resultado_label.config(text="Operação cancelada.")

# Configuração da GUI
janela = tk.Tk()
janela.title("Extrator de E-mails")

texto_label = tk.Label(janela, text="Cole o texto abaixo:")
texto_label.pack()

texto_input = tk.Text(janela, height=10, width=40)
texto_input.pack()

extrair_button = tk.Button(janela, text="Extrair e-mails", command=extrair_e_salvar)
extrair_button.pack()

resultado_label = tk.Label(janela, text="")
resultado_label.pack()

janela.mainloop()
