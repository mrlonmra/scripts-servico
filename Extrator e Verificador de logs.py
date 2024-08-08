import requests
from bs4 import BeautifulSoup
import re
import json

# URL base
base_url = "http://209.38.150.208/SGA/LOGS/nova_cliente_nova/"
api_associado_url = "https://api.hinova.com.br/api/sga/v2/associado/buscar/"
api_veiculo_url = "https://api.hinova.com.br/api/sga/v2/veiculo/buscar/"
api_token = "c619644cf96399a1fbeeb8221a8ca4072cab2f23d7d21aee362c52d3fd1724574948ded2741ecbf2fccbc2fb763a170d9d751a6ad2614b650ad3a3f1701449ef961b07f85a964d7d8aa3830a09f067798f37e1054a1f06dbb97df0831d650aa228b040cd4ff55aba8846cee535a6d91b9803a8f6bbe4b33f561732997d33994bb33f79b3672beff13c2b4697ca9d8899"

def fetch_log_files(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao buscar arquivos de log: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    log_files = [a['href'] for a in soup.find_all('a') if 'SITUACAO.log' in a['href']]
    return log_files

def is_new_log_entry(line):
    return bool(re.match(r"\d{2}/\d{2}/\d{4} as \d{2}:\d{2}:\d{2}", line))

def fix_incomplete_json(json_str):
    if json_str.endswith('...'):
        json_str = json_str[:-3]
    if not json_str.endswith('}'):
        if '"error":[' in json_str:
            json_str += '"]}'
        else:
            json_str += '}'
    return json_str

def extract_errors(log_content):
    errors = []
    lines = log_content.split('\n')
    current_log = []
    for line in lines:
        if is_new_log_entry(line):
            if current_log:
                combined_log = " ".join(current_log)
                errors.extend(parse_log_entry(combined_log))
            current_log = [line]
        else:
            current_log.append(line)
    if current_log:
        combined_log = " ".join(current_log)
        errors.extend(parse_log_entry(combined_log))
    return errors

def parse_log_entry(log_entry):
    errors = []
    if "ERRO" in log_entry:
        timestamp = re.match(r"\d{2}/\d{2}/\d{4} as \d{2}:\d{2}:\d{2}", log_entry).group()
        error_url_match = re.search(r"https?://\S+", log_entry)
        if error_url_match:
            error_url = error_url_match.group()
            error_code_match = re.search(r'/(\d+)/(\d+)', error_url)
            if error_code_match:
                error_code = error_code_match.group(2)
                entity_type = "associado" if "/associado/" in error_url else "veiculo"
                if "cURL error 28: Operation timed out after" in log_entry:
                    error_message = 'TIMEOUT'
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "Login ou senha" in log_entry:
                    error_message = "LOGIN OU SENHA INVALIDOS"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "a mesma que o associado se encontra atualmente" in log_entry:
                    error_message = "O ASSOCIADO JA ESTA NESSA SITUAÇÃO."
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "RECEBER WHATSAPP do objeto ASSOCIADO" in log_entry:
                    error_message = "O CAMPO WHATSAPP NO ASSOCIADO É OBRIGATORIO"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "Cliente n\\u00e3o localizado" in log_entry:
                    error_message = "CLIENTE NÃO LOCALIZADO - ENTREM EM CONTATO COM A HINOVA"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "O campo GERAR COBRANC" in log_entry:
                    error_message = "O CAMPO GERAR COBRANCA RATEIO DO VEICULO É OBRIGATORIO"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "Par\\u00e2metros Inv" in log_entry:
                    error_message = "PARAMETROS INVALIDOS"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "O campo LOGRADOURO do objeto VEICULO" in log_entry:
                    error_message = "O CAMPO LOGRADOURO DO VEÍCULO É OBRIGATORIO"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "Horario inv\\u00e1lido." in log_entry:
                    error_message = "HORARIO INVALIDO"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "CIADO com este CPF" in log_entry:
                    error_message = "JÁ EXISTE UM ASSOCIADO COM ESSE CPF"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                if "cURL error 6: Could not resolve host: api.hinova.com.br" or "cURL error 28: Failed to resolve host 'api.hinova.com.br'" in log_entry:
                    error_message = "NÃO RESOLVEU O HOST: api.hinova.com.br"
                    errors.append((timestamp, error_code, entity_type, error_message))
                    return errors
                else:
                    json_part_match = re.search(r'\{.*', log_entry)
                    if json_part_match:
                        json_part = fix_incomplete_json(json_part_match.group(0))
                        if json_part is None:
                            return errors  # Ignorar este log
                        error_message = json_part
                    else:
                        error_message = 'Erro desconhecido'
                errors.append((timestamp, error_code, entity_type, error_message))
    return errors

def fetch_and_parse_logs(log_files):
    all_errors = []
    seen_errors = set()
    for log_file in log_files:
        try:
            response = requests.get(base_url + log_file)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao buscar o conteúdo do log {log_file}: {e}")
            continue
        log_content = response.text
        errors = extract_errors(log_content)
        for error in errors:
            error_key = (error[1], error[2], error[3])
            if error_key not in seen_errors:
                seen_errors.add(error_key)
                all_errors.append(error)
    return all_errors

def fetch_info(codigo, entity_type):
    """
    Consulta a API para obter a situação do associado ou do veículo.
    """
    url = f"{api_associado_url}{codigo}" if entity_type == "associado" else f"{api_veiculo_url}{codigo}/codigo"
    try:
        response = requests.get(url, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        })
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao consultar {entity_type} {codigo}: {e}")
        return None
    
    return response.json()

def main():
    log_files = fetch_log_files(base_url)
    if not log_files:
        print("Nenhum arquivo de log encontrado.")
        return

    errors = fetch_and_parse_logs(log_files)

    print("Relação de códigos de associado ou veículo e seus erros:")
    for error in errors:
        print(f"Data: {error[0]}, Código: {error[1]}, Tipo: {error[2]}, Erro: {error[3]}")
        info = fetch_info(error[1], error[2])
        if info:
            if error[2] == "associado":
                situacao_associado = info.get("descricao_situacao", "N/A")
                situacao_veiculo = info["veiculos"][0].get("situacao", "N/A") if info.get("veiculos") else "N/A"
                print(f"Situação do Associado: {situacao_associado}, Situação do Veículo: {situacao_veiculo}")
            elif error[2] == "veiculo":
                # Se a resposta for uma lista, pegue o primeiro item
                if isinstance(info, list) and len(info) > 0:
                    situacao_veiculo = info[0].get("descricao_situacao", "N/A")
                else:
                    situacao_veiculo = "N/A"
                print(f"Situação do Veículo: {situacao_veiculo}")

if __name__ == "__main__":
    main()
