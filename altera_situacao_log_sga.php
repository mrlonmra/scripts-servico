<?php

// URLs base e token da API
$base_url = "http://209.38.150.208/SGA/LOGS/nova_cliente_solidy/";
$api_associado_url = "https://api.hinova.com.br/api/sga/v2/associado/buscar/";
$api_veiculo_url = "https://api.hinova.com.br/api/sga/v2/veiculo/buscar/";
$api_alterar_situacao_url = "https://api.hinova.com.br/api/sga/v2/veiculo/alterar-situacao-para/";
$api_token = "fa4a5b183c0db0336613a956039b322f4a0d2ce9b4ac73720fd64bf1e67bae92eef4a39bc88a17fa965c0ff5178b44129955141d5efb5ba64dbfe30f9e7eb2befab8eb88c56ef418039084e3f45fae2ce1b101939af47bf9fa309ab97283d2761086a81946eaaf5c7febb8f9532498f7938bb25fc67798a2a23ca0c0e49765e44026d6f8be4eadef8398bca4b872d7e7";
# NOVA $api_token = "b19884f636e2e09259b94c36d9cecdd380e42e1ec0c0b418dfaf06e4f605656c62839174ce1c76f2799c43a0c5bd2a35a16bc828574ba51153e95074b1b85c5269a7ef94e3168cdc2db32e649f993fa4bb874c266abd2ca2c622d4eaa746d8c94905690719b24c0f46c3ef975f401dc797975fac88fa9485229428663f991d198b3105406d0f04ae016641d4daf5549c";

// Código da situação para "INATIVO MIGRADO"
$codigo_situacao_inativo_migrado = 22;

// Código da situação para "INATIVO MIGRADO" NOVA
//$codigo_situacao_inativo_migrado = 18;

// Função para capturar arquivos de log na URL fornecida
function capturaArquivosLog($url)
{
    $log_files = [];
    // Faz a requisição para obter o conteúdo da URL
    $response = file_get_contents($url);
    if ($response === FALSE) {
        echo "Erro ao buscar arquivos de log.\n";
        return $log_files;
    }
    // Carrega o HTML da resposta e busca os links para os arquivos de log
    $doc = new DOMDocument();
    @$doc->loadHTML($response);
    $links = $doc->getElementsByTagName('a');
    foreach ($links as $link) {
        $href = $link->getAttribute('href');
        // Adiciona o link ao array se contiver 'SITUACAO.log'
        if (strpos($href, 'SITUACAO.log') !== FALSE) {
            $log_files[] = $href;
        }
    }
    return $log_files;
}

// Função para verificar se uma linha de log é uma nova entrada de log
function novoLog($line)
{
    return preg_match('/\d{2}\/\d{2}\/\d{4} as \d{2}:\d{2}:\d{2}/', $line);
}

// Função para corrigir JSON truncado
function fecharJsonLogTruncado($json_str)
{
    if (substr($json_str, -3) === '...') {
        $json_str = substr($json_str, 0, -3);
    }
    if (substr($json_str, -1) !== '}') {
        if (strpos($json_str, '"error":[') !== FALSE) {
            $json_str .= '"]}';
        } else {
            $json_str .= '}';
        }
    }
    return $json_str;
}

// Função para extrair erros do conteúdo do log
function extrairErros($log_content)
{
    $errors = [];
    $lines = explode("\n", $log_content);
    $current_log = [];
    foreach ($lines as $line) {
        if (novoLog($line)) {
            if (!empty($current_log)) {
                $combined_log = implode(" ", $current_log);
                $errors = array_merge($errors, analisarEntradaLog($combined_log));
            }
            $current_log = [$line];
        } else {
            $current_log[] = $line;
        }
    }
    if (!empty($current_log)) {
        $combined_log = implode(" ", $current_log);
        $errors = array_merge($errors, analisarEntradaLog($combined_log));
    }
    return $errors;
}

// Função para analisar uma entrada de log específica
function analisarEntradaLog($log_entry)
{
    $errors = [];
    // Verifica se a entrada de log contém um erro
    if (strpos($log_entry, "ERRO") !== FALSE) {
        // Extrai o timestamp do log
        preg_match('/\d{2}\/\d{2}\/\d{4} as \d{2}:\d{2}:\d{2}/', $log_entry, $timestamp_match);
        $timestamp = $timestamp_match[0];
        // Extrai a URL do erro
        preg_match('/https?:\/\/\S+/', $log_entry, $error_url_match);
        if ($error_url_match) {
            $error_url = $error_url_match[0];
            // Extrai o código do associado ou do veículo da URL
            preg_match('/\/(\d+)\/(\d+)/', $error_url, $error_code_match);
            if ($error_code_match) {
                $error_code = $error_code_match[2];
                $entity_type = (strpos($error_url, "/associado/") !== FALSE) ? "associado" : "veiculo";
                // Determina a mensagem de erro com base no conteúdo da entrada de log
                if (strpos($log_entry, "cURL error 28: Operation timed out after") !== FALSE) {
                    $error_message = 'TIMEOUT';
                } elseif (strpos($log_entry, "Login ou senha") !== FALSE) {
                    $error_message = "LOGIN OU SENHA INVALIDOS";
                } elseif (strpos($log_entry, "a mesma que o associado se encontra atualmente") !== FALSE) {
                    $error_message = "O ASSOCIADO JA ESTA NESSA SITUAÇÃO.";
                } elseif (strpos($log_entry, "RECEBER WHATSAPP do objeto ASSOCIADO") !== FALSE) {
                    $error_message = "O CAMPO WHATSAPP NO ASSOCIADO É OBRIGATORIO";
                } elseif (strpos($log_entry, "Cliente n\\u00e3o localizado") !== FALSE) {
                    $error_message = "CLIENTE NÃO LOCALIZADO - ENTREM EM CONTATO COM A HINOVA";
                } elseif (strpos($log_entry, "O campo GERAR COBRANC") !== FALSE) {
                    $error_message = "O CAMPO GERAR COBRANCA RATEIO DO VEICULO É OBRIGATORIO";
                } elseif (strpos($log_entry, "Par\\u00e2metros Inv") !== FALSE) {
                    $error_message = "PARAMETROS INVALIDOS";
                } elseif (strpos($log_entry, "O campo LOGRADOURO do objeto VEICULO") !== FALSE) {
                    $error_message = "O CAMPO LOGRADOURO DO VEÍCULO É OBRIGATORIO";
                } elseif (strpos($log_entry, "Horario inv\\u00e1lido.") !== FALSE) {
                    $error_message = "HORARIO INVALIDO";
                } elseif (strpos($log_entry, "CIADO com este CPF") !== FALSE) {
                    $error_message = "JÁ EXISTE UM ASSOCIADO COM ESSE CPF";
                } elseif (strpos($log_entry, "cURL error 6: Could not resolve host: api.hinova.com.br") !== FALSE || strpos($log_entry, "cURL error 28: Failed to resolve host 'api.hinova.com.br'") !== FALSE) {
                    $error_message = "NÃO RESOLVEU O HOST: api.hinova.com.br";
                } else {
                    preg_match('/\{.*$/', $log_entry, $json_part_match);
                    if ($json_part_match) {
                        $json_part = fecharJsonLogTruncado($json_part_match[0]);
                        $error_message = $json_part;
                    } else {
                        $error_message = 'Erro desconhecido';
                    }
                }
                // Adiciona o erro ao array de erros
                $errors[] = [$timestamp, $error_code, $entity_type, $error_message];
            }
        }
    }
    return $errors;
}

// Função para buscar e analisar os logs
function buscarAnalisarLogs($log_files)
{
    global $base_url;
    $all_errors = [];
    $seen_errors = [];
    foreach ($log_files as $log_file) {
        // Faz a requisição para obter o conteúdo do arquivo de log
        $response = file_get_contents($base_url . $log_file);
        if ($response === FALSE) {
            echo "Erro ao buscar o conteúdo do log $log_file.\n";
            continue;
        }
        $log_content = $response;
        // Extrai os erros do conteúdo do log
        $errors = extrairErros($log_content);
        foreach ($errors as $error) {
            $error_key = $error[1] . $error[2] . $error[3];
            // Evita a duplicação de erros
            if (!in_array($error_key, $seen_errors)) {
                $seen_errors[] = $error_key;
                $all_errors[] = $error;
            }
        }
    }
    return $all_errors;
}

// Função para fazer a requisição à API SGA e obter informações sobre o associado ou veículo
function requisicaoSGA($codigo, $entity_type)
{
    global $api_associado_url, $api_veiculo_url, $api_token;
    $url = ($entity_type === "associado") ? $api_associado_url . $codigo : $api_veiculo_url . $codigo . "/codigo";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json",
        "Authorization: Bearer $api_token"
    ]);
    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Erro ao consultar ' . $entity_type . ' ' . $codigo . ': ' . curl_error($ch) . "\n";
        return NULL;
    }
    curl_close($ch);
    return json_decode($response, true);
}

// Função para alterar a situação de um veículo
function alterarSituacaoVeiculo($codigo_veiculo, $codigo_situacao)
{
    global $api_alterar_situacao_url, $api_token;
    $url = $api_alterar_situacao_url . $codigo_situacao . '/' . $codigo_veiculo;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json",
        "Authorization: Bearer $api_token"
    ]);
    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Erro ao alterar situação do veículo ' . $codigo_veiculo . ': ' . curl_error($ch) . "\n";
        return NULL;
    }
    curl_close($ch);
    return json_decode($response, true);
}

// Função principal
function main()
{
    global $base_url, $codigo_situacao_inativo_migrado;
    $log_files = capturaArquivosLog($base_url);
    if (empty($log_files)) {
        echo "Nenhum arquivo de log encontrado.\n";
        return;
    }

    $errors = buscarAnalisarLogs($log_files);

    $output = "Relação de códigos de associado ou veículo e seus erros:\n";
    $situacao_diferente = false; // Variável para verificar se há situações diferentes
    $situacoes_diferentes = []; // Array para armazenar detalhes das situações diferentes
    $alteracoes_veiculos = []; // Array para armazenar detalhes das alterações realizadas

    foreach ($errors as $error) {
        $output .= "Data: " . $error[0] . ", Código: " . $error[1] . ", Tipo: " . $error[2] . ", Erro: " . $error[3] . "\n";

        $info = requisicaoSGA($error[1], $error[2]);
        if ($info) {
            if ($error[2] === "associado") {
                $situacao_associado = $info["descricao_situacao"] ?? "N/A";
                $situacao_veiculo = isset($info["veiculos"][0]) ? ($info["veiculos"][0]["situacao"] ?? "N/A") : "N/A";
                if (stripos($situacao_associado, "ASSOCIADO_SEM_VEICULO") !== false) {
                    // Ignora associados na situação "ASSOCIADO_SEM_VEICULO"
                    continue;
                }
                $output .= "Situação do Associado: " . $situacao_associado . ", Situação do Veículo: " . $situacao_veiculo . "\n";
                if (stripos($situacao_associado, "inativo migrado") === false || stripos($situacao_veiculo, "inativo migrado") === false) {
                    $situacao_diferente = true;
                    $situacoes_diferentes[] = [
                        'tipo' => 'associado',
                        'codigo' => $error[1],
                        'situacao_associado' => $situacao_associado,
                        'situacao_veiculo' => $situacao_veiculo
                    ];
                }
            } elseif ($error[2] === "veiculo") {
                if (is_array($info) && !empty($info)) {
                    $situacao_veiculo = $info[0]["descricao_situacao"] ?? "N/A";
                } else {
                    $situacao_veiculo = "N/A";
                }
                $output .= "Situação do Veículo: " . $situacao_veiculo . "\n";
                if (stripos($situacao_veiculo, "inativo migrado") === false) {
                    // Altera a situação do veículo para "INATIVO MIGRADO"
                    $alteracao = alterarSituacaoVeiculo($error[1], $codigo_situacao_inativo_migrado);
                    if ($alteracao !== NULL) {
                        $alteracoes_veiculos[] = [
                            'codigo' => $error[1],
                            'situacao_anterior' => $situacao_veiculo,
                            'nova_situacao' => 'INATIVO MIGRADO'
                        ];
                    }

                    $situacao_diferente = true;
                    $situacoes_diferentes[] = [
                        'tipo' => 'veiculo',
                        'codigo' => $error[1],
                        'situacao' => $situacao_veiculo
                    ];
                }
            }
        }

        // Adiciona uma linha em branco para separar as entradas
        $output .= "\n";
    }

    // Adiciona o resumo ao final do output
    if ($situacao_diferente) {
        $output .= "RESUMO: EXISTEM ASSOCIADOS OU VEÍCULOS EM SITUAÇÃO DIFERENTE DE 'INATIVO MIGRADO'.\n";
        foreach ($situacoes_diferentes as $detalhe) {
            if ($detalhe['tipo'] === 'associado') {
                $output .= "Código do Associado: " . $detalhe['codigo'] . ", Situação do Associado: " . $detalhe['situacao_associado'] . ", Situação do Veículo: " . $detalhe['situacao_veiculo'] . "\n";
            } else {
                $output .= "Código do Veículo: " . $detalhe['codigo'] . ", Situação do Veículo: " . $detalhe['situacao'] . "\n";
            }
        }
    } else {
        $output .= "RESUMO: TODOS OS ASSOCIADOS E VEÍCULOS ESTÃO NA SITUAÇÃO 'INATIVO MIGRADO'.\n";
    }

    // Adiciona o log das alterações realizadas
    if (!empty($alteracoes_veiculos)) {
        $output .= "\nVeículos que tiveram a situação alterada:\n";
        foreach ($alteracoes_veiculos as $alteracao) {
            $output .= "Código do Veículo: " . $alteracao['codigo'] . ", Situação Anterior: " . $alteracao['situacao_anterior'] . ", Nova Situação: " . $alteracao['nova_situacao'] . "\n";
        }
    }

    // Salva a saída em um arquivo
    file_put_contents('verificadorLogs.txt', $output);

    // Exibe a saída no console
    echo $output;
}

// Chama a função principal
main();