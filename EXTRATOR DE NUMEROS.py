import re
import tkinter as tk
from tkinter import filedialog

def extract_phone_numbers():
    raw_text = text_area.get("1.0", "end-1c")
    phone_numbers = set(re.findall(r"\(\d{2}\) \d{5}-\d{4}", raw_text))

    if phone_numbers:
        phone_numbers = sorted(phone_numbers, key=lambda x: x[1:3])  # Ordena pelo DDD
        result_label.config(text=f"Encontrados {len(phone_numbers)} números de telefone únicos.")
        save_to_file(phone_numbers)
    else:
        result_label.config(text="Nenhum número de telefone encontrado.")

def save_to_file(phone_numbers):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Arquivo de texto", "*.txt")],
                                             title="Salvar resultado como")

    if file_path:
        with open(file_path, "w") as file:
            for phone_number in phone_numbers:
                file.write(phone_number)
                file.write("\n")
        result_label.config(text=f"Números de telefone únicos salvos em {file_path}")

# Criação da janela
window = tk.Tk()
window.title("Extrator de Número de Telefone")

# Área de texto
text_area = tk.Text(window, wrap="word", width=60, height=10)
text_area.pack(padx=10, pady=10)

# Botão para extrair número de telefone
extract_button = tk.Button(window, text="Extrair Número", command=extract_phone_numbers)
extract_button.pack()

# Label para exibir o resultado
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=5)

# Inicia a interface gráfica
window.mainloop()
