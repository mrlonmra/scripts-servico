import smtplib
import tkinter as tk
from tkinter import messagebox

# Configurações do servidor SMTP
smtp_server = 'smtp.terra.com.br'
smtp_port = 587
smtp_username = 'email-aqui'
smtp_password = 'd06m06'


class EmailApp:
    def __init__(self, master):
        self.master = master
        master.title("Enviar Email")

        # Campo de entrada do remetente
        tk.Label(master, text="Remetente:").grid(row=0)
        self.sender_entry = tk.Entry(master, width=50)
        self.sender_entry.grid(row=0, column=1)

        # Campo de entrada do destinatário
        tk.Label(master, text="Destinatário:").grid(row=1)
        self.recipient_entry = tk.Entry(master, width=50)
        self.recipient_entry.grid(row=1, column=1)

        # Campo de entrada da mensagem em HTML
        tk.Label(master, text="Mensagem (HTML):").grid(row=2)
        self.message_entry = tk.Text(master, width=50, height=10)
        self.message_entry.grid(row=3, column=1)

        # Botão para enviar o e-mail
        self.send_button = tk.Button(
            master, text="Enviar", command=self.send_email)
        self.send_button.grid(row=4, column=1)

    def send_email(self):
        # Lê os valores dos campos de entrada
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        message = self.message_entry.get("1.0", tk.END)

        # Conecta ao servidor SMTP e faz a autenticação
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Cria a mensagem em formato MIME
        message = f"From: {sender}\nTo: {recipient}\nContent-Type: text/html\n\n{message}"
        message = message.encode('utf-8')

        # Envia a mensagem
        try:
            server.sendmail(sender, recipient, message)
            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar e-mail: {str(e)}")

        # Desconecta do servidor SMTP
        server.quit()


root = tk.Tk()
app = EmailApp(root)
root.mainloop()
