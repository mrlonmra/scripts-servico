import imaplib
import email
import os
import time
from email import message_from_bytes
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Defina as credenciais do seu e-mail
email_usuario = 'segiocarreiro@terra.com.br'
senha = 'd06m06'

# Conecte-se ao servidor IMAP
servidor_imap = 'imap.terra.com.br'  # exemplo para Gmail
conexao = imaplib.IMAP4_SSL(servidor_imap)
conexao.login(email_usuario, senha)

# Defina a caixa de entrada para o upload
caixa_entrada = 'INBOX'

# Crie a janela
janela = tk.Tk()
janela.title('Enviar e-mail')
janela.geometry('600x400')

# Defina a função para selecionar o arquivo .eml


def selecionar_arquivo():
    arquivo_eml = filedialog.askopenfilename(
        filetypes=[('Arquivo .eml', '*.eml')])
    if arquivo_eml:
        enviar_email(arquivo_eml)

# Defina a função para enviar o e-mail


def enviar_email(caminho_arquivo_eml):
    # Leia o conteúdo do arquivo .eml e armazene em uma variável
    with open(caminho_arquivo_eml, 'rb') as arquivo_eml:
        conteudo_eml = arquivo_eml.read()

    # Analise o conteúdo do arquivo .eml
    mensagem = message_from_bytes(conteudo_eml)

    # Defina os cabeçalhos da mensagem
    mensagem['From'] = mensagem['From']  # Defina o remetente da mensagem
    mensagem['To'] = email_usuario  # Defina o destinatário da mensagem
    mensagem['Date'] = datetime.now().strftime(
        "%d-%b-%Y %H:%M:%S")  # Defina a data da mensagem

    # Solicite acesso de gravação à caixa de entrada
    conexao.select(caixa_entrada, readonly=False)

    # Faça o upload da mensagem na caixa de entrada
    conexao.append(caixa_entrada, '', imaplib.Time2Internaldate(
        time.time()), conteudo_eml)

    # Desconecte-se do servidor IMAP
    conexao.close()
    conexao.logout()

    print('Arquivo .eml enviado com sucesso para a caixa de entrada.')


# Crie o botão para selecionar o arquivo .eml
botao_selecionar_arquivo = tk.Button(
    janela, text='ENVIAR ARQUIVO .eml', command=selecionar_arquivo)
botao_selecionar_arquivo.pack(pady=20)

# Inicie o loop principal da janela
janela.mainloop()
