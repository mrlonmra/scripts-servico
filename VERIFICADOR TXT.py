import subprocess
import smtplib
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, receiver_email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.terra.com.br', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def watch_file(file_path, sender_email, sender_password, receiver_email):
    command = f'inotifywait -m -e modify {file_path}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode().strip()
        if output:
            print(f'Arquivo modificado: {output}')

            subject = 'Arquivo modificado'
            message = f'O arquivo {file_path} foi modificado.'
            send_email(sender_email, sender_password, receiver_email, subject, message)

if __name__ == '__main__':
    file_path = '/var/www/sinesp-mj.site/dados.txt'
    sender_email = 'segiocarreiro@terra.com.br'
    sender_password = 'd06m06'
    receiver_email = 'mrlon.mra@gmail.com'

    watch_file(file_path, sender_email, sender_password, receiver_email)
