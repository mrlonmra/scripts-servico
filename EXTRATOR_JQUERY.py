import tkinter as tk
from tkinter import filedialog
import pandas as pd
import json
from tkinter import messagebox

# Função para lidar com a seleção de arquivo
def selecionar_arquivo():
    # Abrir o diálogo de seleção de arquivo
    file_path = filedialog.askopenfilename()

    # Verificar se um arquivo foi selecionado
    if file_path:
        # Carregar o arquivo do Excel
        df = pd.read_excel(file_path)

        # Colunas para converter em JSON
        colunas = ['de_val', 'ate_val', 'cota', 'adesao', 'val_mensal']

        # Lista para armazenar os objetos JSON
        lista_json = []

        # Iterar sobre as linhas da planilha
        for _, row in df.iterrows():
            # Criar um dicionário com os valores das colunas selecionadas para a linha atual
            data = {col: str(row[col]) for col in colunas}

            # Converter o dicionário para formato JSON
            json_data = json.dumps(data)

            # Adicionar o JSON à lista
            lista_json.append(json_data)

        # Exportar os dados para um arquivo de texto
        exportar_para_txt(lista_json)

# Função para exportar os dados para um arquivo de texto
def exportar_para_txt(lista_json):
    # Abrir o diálogo de salvamento de arquivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Arquivos de Texto", "*.txt"),))

    # Verificar se um arquivo foi selecionado
    if file_path:
        try:
            # Criar o arquivo de texto
            with open(file_path, 'w') as file:
                # Escrever os dados no arquivo
                for json_data in lista_json:
                    file.write(json_data + '\n')

            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", "A conversão para JSON foi realizada com sucesso.")
        except Exception as e:
            # Exibir mensagem de erro
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")

# Criar a janela principal
root = tk.Tk()
root.title("Extrator Json")
root.geometry("400x400")
root.configure(background="#441155")

# Adicionar o logotipo
logo_label = tk.Label(root, background="#441155")
logo_label.pack(pady=20)

# Adicionar o texto
texto = tk.Label(root, text="Extrator Execel - JSON", font=("Arial", 16), fg="white", background="#441155")
texto.pack(pady=50)

# Adicionar o botão para selecionar o arquivo
button = tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo)
button.pack(pady=25)

# Adicionar o rodapé
rodape = tk.Label(root, text="Desenvolvido por Marlon - Suporte Ileva", font=("Arial", 10), fg="white", background="#441155")
rodape.pack(side=tk.BOTTOM, pady=10)

# Executar a interface gráfica
root.mainloop()
