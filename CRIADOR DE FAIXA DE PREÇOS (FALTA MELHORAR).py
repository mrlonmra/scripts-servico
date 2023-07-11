import openpyxl
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, simpledialog

def gerar_tabela_faixas_preco():
    inicio = float(inicio_entry.get())
    fim = float(fim_entry.get())
    incremento = float(incremento_entry.get())

    result = selecionado.get()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet["A1"] = "Valor Inicial"
    sheet["B1"] = "Valor Final"

    valor_inicial = inicio
    row = 2
    while valor_inicial <= fim:
        valor_final = valor_inicial + incremento
        if result == 1:
            valor_final += 0.01
        sheet["A{}".format(row)] = valor_inicial
        sheet["B{}".format(row)] = valor_final
        valor_inicial += incremento
        row += 1

    filename = simpledialog.askstring("Salvar tabela", "Digite o nome do arquivo:")
    if filename:
        workbook.save(f"{filename}.xlsx")
        result_label.config(text="Tabela de faixas de preço gerada e salva com sucesso!")
    else:
        result_label.config(text="Falha ao salvar a tabela. Nome do arquivo não fornecido.")

# Criação da janela principal
window = Tk()
window.title("Gerador de Tabela de Faixas de Preço")

# Rótulos e campos de entrada
inicio_label = Label(window, text="Valor Inicial:")
inicio_label.pack()
inicio_entry = Entry(window)
inicio_entry.pack()

fim_label = Label(window, text="Valor Final:")
fim_label.pack()
fim_entry = Entry(window)
fim_entry.pack()

incremento_label = Label(window, text="Incremento:")
incremento_label.pack()
incremento_entry = Entry(window)
incremento_entry.pack()

# Seleção para adição de 0.01
select_label = Label(window, text="Adicionar 0.01?")
select_label.pack()

selecionado = IntVar()
check_button = Checkbutton(window, text="Sim", variable=selecionado)
check_button.pack()

# Botão para gerar a tabela
gerar_button = Button(window, text="Gerar Tabela", command=gerar_tabela_faixas_preco)
gerar_button.pack()

# Rótulo para exibir o resultado
result_label = Label(window, text="")
result_label.pack()

# Iniciar a janela
window.mainloop()