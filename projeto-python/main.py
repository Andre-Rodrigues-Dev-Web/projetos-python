import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import locale

# Configurar a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para obter dados de câmbio
def get_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data["rates"]

# Função para obter dados de criptomoedas
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data

# Função para criar gráfico de câmbio
def plot_exchange_rates():
    rates = get_exchange_rates()
    currencies = ["BRL", "EUR", "USD"]
    values = [rates[cur] for cur in currencies]

    fig, ax = plt.subplots()
    ax.bar(currencies, values, color=['#4CAF50', '#2196f3', '#FF9800'])
    ax.set_title('Câmbio de Moedas')
    ax.set_ylabel('Valor em USD')

    return fig

# Função para criar gráfico de criptomoedas
def plot_crypto_prices():
    prices = get_crypto_prices()
    cryptos = ["bitcoin", "ethereum", "ripple"]
    values = [prices[crypto]["usd"] for crypto in cryptos]

    fig, ax = plt.subplots()
    ax.bar(cryptos, values, color=['#9C27B0', '#FFEB3B', '#03A9F4'])
    ax.set_title('Preços de Criptomoedas')
    ax.set_ylabel('Valor em USD')

    return fig

# Função para mostrar o gráfico de câmbio
def show_exchange_graph():
    exchange_fig = plot_exchange_rates()

    for widget in content_frame.winfo_children():
        widget.destroy()

    exchange_canvas = FigureCanvasTkAgg(exchange_fig, master=content_frame)
    exchange_canvas.draw()
    exchange_canvas.get_tk_widget().pack(expand=True)

# Função para mostrar o gráfico de criptomoedas
def show_crypto_graph():
    crypto_fig = plot_crypto_prices()

    for widget in content_frame.winfo_children():
        widget.destroy()

    crypto_canvas = FigureCanvasTkAgg(crypto_fig, master=content_frame)
    crypto_canvas.draw()
    crypto_canvas.get_tk_widget().pack(expand=True)

# Função para gerar dados de transações PIX (para exemplo)
def generate_pix_data():
    data = []
    current_date = datetime.now()
    owners = ['João', 'Maria', 'Carlos', 'Ana', 'Pedro']
    receivers = ['Empresa A', 'Loja B', 'Serviço C', 'Instituição D', 'Fulano']
    banks = ['Itaú', 'Bradesco', 'Caixa', 'Banco do Brasil', 'Santander']
    
    for i in range(50):
        date = current_date - timedelta(days=i)
        owner = owners[i % len(owners)]
        receiver = receivers[i % len(receivers)]
        bank = banks[i % len(banks)]
        num_transactions = abs(100 + 30 * (i % 7) - i)
        data.append((date.strftime('%d/%m/%Y'), owner, receiver, bank, num_transactions))
        
    return pd.DataFrame(data, columns=['Date', 'Account Owner', 'Receiver', 'Bank', 'Transactions'])

# Função para exibir a tabela de transações PIX
def show_pix_transactions():
    data = generate_pix_data()

    for widget in content_frame.winfo_children():
        widget.destroy()

    # Filtro de data
    def filter_data():
        start_date = start_entry.get()
        end_date = end_entry.get()
        if start_date and end_date:
            filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
        else:
            filtered_data = data
        update_table(filtered_data)

    # Atualiza a tabela com os dados filtrados
    def update_table(filtered_data):
        for row in tree.get_children():
            tree.delete(row)
        for index, row in filtered_data.iterrows():
            transactions_formatted = locale.currency(row['Transactions'], grouping=True)
            tree.insert("", tk.END, values=(row['Date'], row['Account Owner'], row['Receiver'], row['Bank'], transactions_formatted))

    # Layout da tela de transações PIX
    filter_frame = ttk.Frame(content_frame, padding="10 10 10 10")
    filter_frame.pack(fill=tk.X)

    ttk.Label(filter_frame, text="Data Início (dd/mm/yyyy):").grid(column=0, row=0, sticky=tk.W)
    start_entry = ttk.Entry(filter_frame)
    start_entry.grid(column=1, row=0, sticky=tk.W)

    ttk.Label(filter_frame, text="Data Fim (dd/mm/yyyy):").grid(column=2, row=0, sticky=tk.W)
    end_entry = ttk.Entry(filter_frame)
    end_entry.grid(column=3, row=0, sticky=tk.W)

    filter_button = ttk.Button(filter_frame, text="Filtrar", command=filter_data, style="TButton")
    filter_button.grid(column=4, row=0, sticky=tk.W)

    tree_frame = ttk.Frame(content_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('Date', 'Account Owner', 'Receiver', 'Bank', 'Transactions')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    tree.heading('Date', text='Data')
    tree.heading('Account Owner', text='Dono da Conta')
    tree.heading('Receiver', text='Recebedor')
    tree.heading('Bank', text='Banco')
    tree.heading('Transactions', text='Transações')

    tree.pack(fill=tk.BOTH, expand=True)

    update_table(data)

# Criação da janela principal
root = tk.Tk()
root.title("Valores de Moedas e Criptomoedas")
root.geometry("800x600")

# Estilo flat
style = ttk.Style()
style.theme_use("clam")

# Configuração de estilos
style.configure("TFrame", background="white")
style.configure("Sidebar.TFrame", background="#2196f3")
style.configure("TButton",
                background="#2196f3",
                foreground="#fff",
                borderwidth=0,
                focuscolor="none")
style.map("TButton",
          background=[('active', '#1976D2')],
          foreground=[('active', '#fff')])

# Frame principal
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Sidebar para navegação
sidebar_frame = ttk.Frame(main_frame, width=200, style="Sidebar.TFrame")
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Botões de navegação na sidebar
ttk.Button(sidebar_frame, text="Câmbio de Moedas", command=show_exchange_graph, style="TButton").pack(fill=tk.X, padx=5, pady=5)
ttk.Button(sidebar_frame, text="Preços de Criptomoedas", command=show_crypto_graph, style="TButton").pack(fill=tk.X, padx=5, pady=5)
ttk.Button(sidebar_frame, text="Transações PIX", command=show_pix_transactions, style="TButton").pack(fill=tk.X, padx=5, pady=5)

# Frame para conteúdo dos gráficos
content_frame = ttk.Frame(main_frame, style="TFrame")
content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Inicializa com o gráfico de câmbio
show_exchange_graph()

# Executa a aplicação
root.mainloop()
