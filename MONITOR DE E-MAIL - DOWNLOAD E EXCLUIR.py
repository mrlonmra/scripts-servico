import imapclient
import email.header
import email.charset
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Configurações de conexão IMAP
HOST = 'imap.terra.com.br'
USERNAME = 'email-aqui'
PASSWORD = 'd06m06'
SEARCH_KEYWORDS = ['Sinesp']

# Conexão IMAP
server = imapclient.IMAPClient(HOST)
server.login(USERNAME, PASSWORD)
server.select_folder('INBOX')

# Lista de mensagens de e-mail encontradas
messages = []

# Pesquisa por e-mails que contêm palavras-chave no assunto


def search_emails():
    global messages
    new_messages = server.search(['SUBJECT'] + SEARCH_KEYWORDS)
    if new_messages == messages:
        tk.messagebox.showinfo('Nenhum novo e-mail',
                               'Não foram encontrados novos e-mails.')
    else:
        messages = new_messages
        # Limpa a lista de e-mails anteriores
        listbox.delete(0, tk.END)
        # Adiciona os e-mails encontrados à lista
        for msg_id in messages:
            envelope = server.fetch([msg_id], ['ENVELOPE'])[
                msg_id][b'ENVELOPE']
            subject = envelope.subject or ''
            if isinstance(subject, bytes):
                subject = subject.decode()
            subject_pairs = email.header.decode_header(subject)
            subject = ''
            for decoded_text, charset in subject_pairs:
                if isinstance(decoded_text, bytes):
                    decoded_text = decoded_text.decode(charset or 'utf-8')
                subject += decoded_text
            listbox.insert(tk.END, f'{msg_id} - {subject}')


# Cria interface gráfica
root = tk.Tk()
root.title('E-mails encontrados')
root.geometry('600x400')
root.resizable(False, False)

# Define tema de cores
style = ttk.Style()
style.theme_use('clam')
style.configure('.', background='#1e1e1e', foreground='white')
style.configure('TButton', background='#3d3d3d',
                foreground='white', borderwidth=0, padx=10)
style.map('TButton', background=[('active', '#4f4f4f')])


# Cria lista para exibir e-mails
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)


def download_email():
    # Obtém o ID da mensagem selecionada
    selected_indices = listbox.curselection()
    if len(selected_indices) == 0:
        return
    msg_id = messages[selected_indices[0]]

    # Baixa o e-mail em formato EML
    eml_data = server.fetch([msg_id], ['RFC822']).get(
        msg_id, {}).get(b'RFC822', None)
    if eml_data is None:
        tk.messagebox.showwarning(
            'Erro ao baixar e-mail', 'Não foi possível baixar o e-mail selecionado.')
        return

    # Salva o conteúdo do e-mail em um arquivo
    filename = f'{msg_id}.eml'
    with open(filename, 'wb') as f:
        f.write(eml_data)

    # Apaga a mensagem da caixa de entrada
    server.delete_messages([msg_id])

    messagebox.showinfo('Download concluído',
                        'O e-mail foi baixado em {}.'.format(filename))


def show_menu(event):
    try:
        item = listbox.curselection()
        if item:
            menu = tk.Menu(listbox, tearoff=0)
            menu.add_command(label="Baixar e-mail", command=download_email)
            menu.post(event.x_root, event.y_root)
    finally:
        pass


listbox.bind("<Button-3>", show_menu)

# Cria botão de pesquisa
search_button = ttk.Button(root, text='Pesquisar', command=search_emails)
search_button.pack(side=tk.LEFT, padx=10, pady=10)

# Cria botão de saída
quit_button = ttk.Button(root, text='Sair', command=root.quit)
quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Inicia loop de interface gráfica
root.mainloop()

# Desconexão IMAP
server.logout()
