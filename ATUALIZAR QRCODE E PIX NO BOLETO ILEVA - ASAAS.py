import requests
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Função para processar cada ID e fazer a requisição ao endpoint
def verificar_boleto(id_boleto, headers):
    url = f'https://solidy.ileva.com.br/sistema/financeiro/boleto/verificaCobAsaas/id/{id_boleto}'
    try:
        response = requests.get(url, headers=headers)
        
        # Logar o status e o conteúdo da resposta
        print(f"ID {id_boleto} - Status Code: {response.status_code}")
        # Conteúdo da resposta, descomente a linha abaixo se quiser exibir no terminal
        # print(f"Conteúdo da resposta: {response.text}")

        # Verificar se a resposta está vazia ou não é JSON
        if response.status_code == 200:
            try:
                response_data = response.json()
            except ValueError:
                print(f"Erro: A resposta não está no formato JSON esperado para o ID {id_boleto}.")
                return
            
            # Verificar se o objeto retornado é "payment"
            if response_data.get('object') == 'payment':
                print(f"Sucesso: ID {id_boleto} processado com sucesso.")
            else:
                print(f"Erro: ID {id_boleto} não retornou um objeto de pagamento válido.")
        else:
            print(f"Erro: ID {id_boleto} retornou o status {response.status_code}.")

    except Exception as e:
        print(f"Erro ao processar o ID {id_boleto}: {e}")

# Função principal para ler o CSV e processar todos os IDs
def processar_boletos(caminho_csv):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        # Adicione os cabeçalhos necessários conforme o seu exemplo de curl
        'Cookie': '_ga_BL70T1HXSC=GS1.1.1726751411.1.0.1726751704.0.0.0; _gcl_au=1.1.372818866.1727102653; _fbp=fb.2.1727102653744.707277317593146368; _ga_8HWNEDYH2T=GS1.1.1727102649.1.0.1727102675.0.0.0; _ga_DV8WBLP23W=GS1.3.1727177058.2.1.1727177058.60.0.0; _ga=GA1.1.489049116.1725911949; session_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbl9jbGllbnRlIjoic29saWR5IiwiYWRtaW5fbG9nYWRvIjp0cnVlLCJhZG1pbl9pZCI6MSwiYWRtaW5fc2FsdCI6IjE3NDc3ODAyOTIiLCJleHBpcmVkIjoiMjAyNC0wOS0yNyAwMzowMTo1NSJ9.n15ClQ4wDXvoEMWh_vg_bvUC4JkXnVqQbhCXsuzgRC4; _ga_1ZHF37XPWK=GS1.1.1727367934.46.1.1727371106.0.0.0',  # Complete com os cookies
        'Referer': 'https://solidy.ileva.com.br/sistema/financeiro/boleto/visualizar/id/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Abrir o CSV e ler os IDs
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        ids = [row[0] for row in reader]  # Supondo que cada linha tem um ID em sua primeira coluna
    
    # Usar tqdm para mostrar a barra de progresso
    with ThreadPoolExecutor(max_workers=10) as executor:  # Utilizar 10 threads
        list(tqdm(executor.map(lambda id_boleto: verificar_boleto(id_boleto, headers), ids), 
                  total=len(ids), desc="Verificando boletos"))

# Executar o script com o caminho do CSV
if __name__ == "__main__":
    caminho_csv = input("Digite o caminho completo para o arquivo CSV com os IDs: ")
    processar_boletos(caminho_csv)
