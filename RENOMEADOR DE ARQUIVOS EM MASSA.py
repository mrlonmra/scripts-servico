import os

# substitua pelo caminho do diretório onde estão os arquivos
diretorio = r"C:/Users/Híbrida/Desktop/1"
prefixo = 'manual'  # prefixo para o novo nome
extensao = '.jpg'  # extensão dos arquivos originais
contador = 0  # contador para os novos nomes

# percorre todos os arquivos no diretório
for arquivo in os.listdir(diretorio):
    # verifica se é um arquivo com a extensão desejada
    if arquivo.endswith(extensao):
        # constrói o novo nome com o prefixo e o número
        novo_nome = f'{prefixo}-{contador:02}{extensao}'
        # renomeia o arquivo
        os.rename(os.path.join(diretorio, arquivo),
                  os.path.join(diretorio, novo_nome))
        # incrementa o contador
        contador += 1
