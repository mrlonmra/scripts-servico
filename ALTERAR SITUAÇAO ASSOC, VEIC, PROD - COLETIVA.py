import json
import logging
import requests
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurando o logger
logging.basicConfig(
    filename='inativacao_veiculos.log',  # Nome do arquivo de log
    level=logging.DEBUG,                 # Nível de log: DEBUG para ser mais verbose
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato do log
    datefmt='%Y-%m-%d %H:%M:%S'          # Formato da data
)

# Função para ler o JSON a partir de um arquivo
def ler_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            logging.info(f"Lendo arquivo JSON: {caminho_arquivo}")
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar JSON: {caminho_arquivo}")
        return None

# Função para transformar o JSON de entrada, garantindo que todos os veículos e produtos ativos sejam inativados
def transformar_json(json_entrada):
    logging.info("Iniciando a transformação do JSON de entrada.")
    resultado = []

    # Itera sobre os associados
    for associado in json_entrada:
        novo_associado = {
            "nome_associado": "",  # Placeholder
            "cpf": associado["cpf_cnpj"],
            "data_contrato": "",  # Placeholder
            "hora_cadastro": "",  # Placeholder
            "codigo_associado": associado["codigo_associado"],
            "rg": "",  # Placeholder
            "data_nascimento": "",  # Placeholder
            "cep": "",  # Placeholder
            "logradouro": "",  # Placeholder
            "numero": "",  # Placeholder
            "complemento": "",  # Placeholder
            "bairro": "",  # Placeholder
            "cidade": "",  # Placeholder
            "estado": "",  # Placeholder
            "ddd": "",  # Placeholder
            "telefone": "",  # Placeholder
            "ddd_celular": "",  # Placeholder
            "telefone_celular": "",  # Placeholder
            "email": "",  # Placeholder
            "status": "INATIVO",  # Definindo o status do associado como INATIVO
            "veiculos": []
        }

        # Itera sobre os veículos do associado
        veiculos_inativos = False
        for veiculo in associado.get("veiculos", []):
            veiculo_inativado = False
            if veiculo['status'] == 'ATIVO':  # Verifica se o veículo está ativo
                veiculo_inativado = True
            novo_veiculo = {
                "codigo_veiculo": veiculo["codigo_veiculo"],
                "placa": veiculo["placa"],
                "chassi": "",  # Placeholder
                "renavam": "",  # Placeholder
                "ano_fabricacao": "",  # Placeholder
                "ano_modelo": "",  # Placeholder
                "valor_fipe": "",  # Placeholder
                "codigo_fipe": "",  # Placeholder
                "descricao_modelo": "",  # Placeholder
                "status": "INATIVO",  # Força o status do veículo para INATIVO
                "descricao_cor": "",  # Placeholder
                "descricao_combustivel": "",  # Placeholder
                "descricao_tipoveiculo": "",  # Placeholder
                "descricao_marca": "",  # Placeholder
                "produtos": []
            }

            # Itera sobre os produtos do veículo
            for produto in veiculo.get("produtos", []):
                if produto['status'] == 'ATIVO':  # Verifica se o produto está ativo
                    veiculo_inativado = True
                    logging.debug(f"Produto {produto['codigo_produto']} (Status: ATIVO) encontrado no veículo {veiculo['codigo_veiculo']}.")
                novo_produto = {
                    "codigo_produto": produto["codigo_produto"],
                    "descricao_produto": "",  # Placeholder
                    "status": "INATIVO"  # Define o status do produto como INATIVO
                }
                novo_veiculo["produtos"].append(novo_produto)

            # Se o veículo tem algum produto ativo ou está ativo, ele será inativado
            if veiculo_inativado:
                novo_associado["veiculos"].append(novo_veiculo)
                veiculos_inativos = True

        # Se houver veículos ativos ou produtos ativos, o associado será processado
        if veiculos_inativos:
            resultado.append(novo_associado)
            logging.debug(f"Associado {associado['codigo_associado']} processado com veículos ativos/inativados.")

    logging.info("Transformação do JSON de entrada concluída.")
    return resultado

# Função para dividir a lista em lotes de no máximo 10 itens
def dividir_em_lotes(dados, tamanho_lote=10):
    it = iter(dados)
    for i in range(0, len(dados), tamanho_lote):
        yield list(islice(it, tamanho_lote))

# Função para consumir a API
def consumir_api(lote, token, lote_num):
    url = "https://sistema.accenda.com.br/api/v2/sincronizar"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=lote)
        response.raise_for_status()  # Levanta uma exceção se o código de status não for 200
        
        logging.info(f"Resposta da API (Lote {lote_num}): {response.json()}")
        return {"status": "SUCESSO", "lote": lote_num, "resposta": response.json()}
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consumir a API no lote {lote_num}: {e}")
        return {"status": "ERRO", "lote": lote_num, "mensagem": str(e)}

# Função principal para executar o processo
def inativar_veiculos():
    caminho_arquivo = input("Digite o caminho completo do arquivo JSON: ")
    token = input("Digite o token de acesso: ")

    # Lê o arquivo JSON
    json_entrada = ler_json(caminho_arquivo)
    if json_entrada is None:
        logging.error("Erro ao ler o JSON de entrada. Encerrando o processo.")
        return

    # Transforma o JSON para o formato correto, garantindo que veículos e produtos ativos sejam inativados
    json_saida = transformar_json(json_entrada)

    # Se houver dados para processar
    if json_saida:
        lotes = list(dividir_em_lotes(json_saida, tamanho_lote=10))
        lotes_com_erro = []
        limite_tentativas = 3

        # Usando ThreadPoolExecutor para processar os lotes em paralelo
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(consumir_api, lote, token, index + 1): lote for index, lote in enumerate(lotes)}

            for future in as_completed(futures):
                resultado = future.result()
                lote_num = resultado["lote"]

                if resultado["status"] == "ERRO":
                    lotes_com_erro.append(futures[future])
                    logging.warning(f"Lote {lote_num} falhou. Adicionando para reprocessamento.")
                    print(f"Lote {lote_num} falhou. Adicionando para reprocessamento.")
                else:
                    print(f"Resposta da API (Lote {lote_num}):", resultado["resposta"])

        # Tentativa de reprocessar lotes que deram erro
        tentativas = 0
        while lotes_com_erro and tentativas < limite_tentativas:
            logging.info(f"Reprocessando lotes com erro. Tentativa {tentativas + 1} de {limite_tentativas}")
            print(f"Reprocessando lotes com erro. Tentativa {tentativas + 1} de {limite_tentativas}...")

            lotes_com_erro_novos = []

            # Reprocessando lotes com erro em paralelo
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(consumir_api, lote, token, index + 1): lote for index, lote in enumerate(lotes_com_erro)}

                for future in as_completed(futures):
                    resultado = future.result()
                    lote_num = resultado["lote"]

                    if resultado["status"] == "ERRO":
                        lotes_com_erro_novos.append(futures[future])
                        logging.warning(f"Lote {lote_num} falhou novamente. Tentativa {tentativas + 1}.")
                        print(f"Lote {lote_num} falhou novamente. Tentativa {tentativas + 1}.")
                    else:
                        print(f"Resposta da API (Lote {lote_num} - Reprocessado):", resultado["resposta"])

            lotes_com_erro = lotes_com_erro_novos
            tentativas += 1

        if not lotes_com_erro:
            logging.info("Todos os lotes foram processados com sucesso.")
            print("Todos os lotes foram processados com sucesso.")
        else:
            logging.error(f"Alguns lotes falharam após {limite_tentativas} tentativas.")
            print(f"Alguns lotes falharam após {limite_tentativas} tentativas.")

    else:
        logging.info("Nenhum veículo ou produto ativo encontrado para inativar.")
        print("Nenhum veículo ou produto ativo encontrado para inativar.")

# Executa o processo de inativação
inativar_veiculos()
