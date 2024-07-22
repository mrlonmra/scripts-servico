import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define as informações do servidor SMTP e as credenciais de login
smtp_server = 'smtp.terra.com.br'
smtp_port = 587
smtp_username = 'segiocarreiro@terra.com.br'
smtp_password = ''

# Define as informações do remetente e do destinatário do e-mail
remetente = 'segiocarreiro@terra.com.br'
destinatario = 'mrlon.mra@gmail.com'

# URL do site que você deseja monitorar
url = 'https://www.iades.com.br/inscricao/ProcessoSeletivo.aspx?id=df57c0a1'

# Número da última linha verificada
ultimo_numero_linhas = 0

# Inicia o loop de monitoramento
while True:
    # Faz uma solicitação HTTP para a página da web
    response = requests.get(url)

    # Verifica se houve um erro ao acessar a página
    if response.status_code != 200:
        print(f'Erro ao acessar a página: {response.status_code}')
        continue

    # Analisa o HTML da página da web com o BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra a tabela que você deseja monitorar (neste exemplo, a primeira tabela na página)
    tables = soup.find_all('table')
    print('SITE VERIFICADO!')

    # Conta quantas linhas (TRs) estão dentro do tbody
    linhas = soup.find_all('tr')
    print(f'{len(linhas)} LINHAS EXISTENTES!')

    num_linhas = len(linhas)

    # Verifica se o número de linhas mudou desde a última verificação
    if num_linhas != ultimo_numero_linhas:
        print(f'O número de documentos agora é {num_linhas}!')
        # Atualiza o número de linhas da tabela
        ultimo_numero_linhas = num_linhas

    # Cria o corpo do e-mail a ser enviado
        assunto = 'SAIU NOVIDADE NO CONCURSO'
        corpo = f'O número de linhas agora é {num_linhas}! Corre lá.'.encode('utf-8')
        
        # Configura a mensagem de e-mail
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto
        mensagem.attach(MIMEText(corpo, 'plain', 'utf-8'))
        
        # Envia o e-mail
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(remetente, destinatario, mensagem.as_string())
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
    
    # Aguarda 5 minutos antes de verificar a página novamente
    time.sleep(5)
