import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
from datetime import datetime

def iniciar_bd():
    """ Inicializa o banco de dados e cria as tabelas necessárias. """
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            cargo TEXT,
            salario REAL,
            data_admissao DATE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL,
            quantidade INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def verificar_login(usuario, senha):
    """ Verifica as credenciais do usuário. """
    if usuario == "admin" and senha == "1234":
        abrir_dashboard()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

def abrir_dashboard():
    """ Abre a tela principal do dashboard após o login. """
    tela_login.destroy()
    global tela_dashboard, frame_conteudo
    tela_dashboard = tk.Tk()
    tela_dashboard.title("Dashboard")
    tela_dashboard.geometry("1000x600")
    tela_dashboard.configure(bg="#ECF0F1")
    
    frame_sidebar = tk.Frame(tela_dashboard, width=200, bg="#2C3E50", height=600, relief="flat")
    frame_sidebar.pack(side="left", fill="y")
    label_sidebar = tk.Label(frame_sidebar, text="Menu", fg="white", bg="#2C3E50", font=("Arial", 18))
    label_sidebar.pack(pady=20)
    
    buttons = {
        "Dashboard": "dashboard",
        "Cadastrar Produto": "cadastro_produto",
        "Listar Produtos": "listar_produtos",
        "Cadastrar Funcionário": "cadastrar_funcionario",
        "Listar Funcionários": "listar_funcionarios"
    }
    for text, action in buttons.items():
        tk.Button(frame_sidebar, text=text, command=lambda act=action: mostrar_conteudo(act), bg="#3498DB", fg="white", font=("Arial", 14), relief="flat").pack(pady=10, padx=10, fill="x")
    
    frame_conteudo = tk.Frame(tela_dashboard, bg="#ECF0F1")
    frame_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    
    mostrar_conteudo("dashboard")
    tela_dashboard.mainloop()

def mostrar_conteudo(tipo):
    """ Mostra o conteúdo específico no painel direito com base na ação selecionada. """
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    
    if tipo == "dashboard":
        criar_cards()
    elif tipo == "cadastro_produto":
        criar_formulario_produto()
    elif tipo == "listar_produtos":
        listar_produtos()
    elif tipo == "cadastrar_funcionario":
        criar_formulario_funcionario()
    elif tipo == "listar_funcionarios":
        listar_funcionarios()

def criar_cards():
    """ Exibe cards de exemplo no dashboard. """
    for i in range(3):
        frame_card = tk.Frame(frame_conteudo, bg="#FFFFFF", relief="flat", borderwidth=1, padx=10, pady=10)
        frame_card.pack(padx=10, pady=10, side="left", fill="both", expand=True)
        
        label_titulo = tk.Label(frame_card, text=f"Card {i+1}", font=("Arial", 16), bg="#FFFFFF")
        label_titulo.pack(pady=(10, 2))
        
        label_conteudo = tk.Label(frame_card, text="Conteúdo do card", bg="#FFFFFF")
        label_conteudo.pack(pady=2)

def criar_formulario_produto():
    """ Cria o formulário para cadastro de produtos. """
    tk.Label(frame_conteudo, text="Cadastro de Produto", font=("Arial", 24), bg="#ECF0F1", fg="#2C3E50").pack(pady=20)
    
    campos = ["Nome", "Descrição", "Preço", "Quantidade"]
    entries = {}
    
    for campo in campos:
        frame_campo = tk.Frame(frame_conteudo, bg="#ECF0F1")
        frame_campo.pack(pady=5, fill="x", padx=20)
        
        tk.Label(frame_campo, text=campo + ":", bg="#ECF0F1", font=("Arial", 12)).pack(side="left", padx=10)
        entry = tk.Entry(frame_campo, font=("Arial", 12), width=30)
        entry.pack(side="left", padx=10)
        entries[campo] = entry
    
    def salvar_produto():
        conn = sqlite3.connect('empresa.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (?, ?, ?, ?)
        ''', (entries["Nome"].get(), entries["Descrição"].get(), entries["Preço"].get(), entries["Quantidade"].get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
        mostrar_conteudo("listar_produtos")
    
    tk.Button(frame_conteudo, text="Salvar", command=salvar_produto, bg="#3498DB", fg="white", font=("Arial", 12), relief="flat").pack(pady=20)

def listar_produtos():
    """ Lista todos os produtos em uma tabela com opções para editar e deletar. """
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, descricao, preco, quantidade FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    
    tabela = ttk.Treeview(frame_conteudo, columns=("ID", "Nome", "Descrição", "Preço", "Quantidade"), show="headings")
    tabela.pack(expand=True, fill="both", padx=20, pady=20)
    
    for col in tabela["columns"]:
        tabela.heading(col, text=col)
    
    for produto in produtos:
        tabela.insert("", "end", values=produto)
    
    def deletar_produto():
        selected_item = tabela.selection()[0]
        produto_id = tabela.item(selected_item)["values"][0]
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente deletar o produto com ID {produto_id}?")
        if resposta:
            conn = sqlite3.connect('empresa.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            conn.close()
            tabela.delete(selected_item)
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso")
    
    def editar_produto():
        selected_item = tabela.selection()[0]
        produto_id = tabela.item(selected_item)["values"][0]
        # Implemente a edição aqui
        messagebox.showinfo("Editar", f"Editar produto com ID {produto_id}")
    
    tk.Button(frame_conteudo, text="Deletar Produto", command=deletar_produto, bg="#E74C3C", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
    tk.Button(frame_conteudo, text="Editar Produto", command=editar_produto, bg="#3498DB", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)

# Implementação de funções de cadastro e listagem de funcionários omitidas por brevidade

def criar_formulario_funcionario():
    """ Cria o formulário para cadastro de funcionários. """
    tk.Label(frame_conteudo, text="Cadastro de Funcionário", font=("Arial", 24), bg="#ECF0F1", fg="#2C3E50").pack(pady=20)
    campos = ["Nome", "CPF", "Cargo", "Salário", "Data de Admissão"]
    entries = {}
    
    for campo in campos:
        frame_campo = tk.Frame(frame_conteudo, bg="#ECF0F1")
        frame_campo.pack(pady=5, fill="x", padx=20)
        
        tk.Label(frame_campo, text=campo + ":", bg="#ECF0F1", font=("Arial", 12)).pack(side="left", padx=10)
        entry = tk.Entry(frame_campo, font=("Arial", 12), width=30)
        entry.pack(side="left", padx=10)
        entries[campo] = entry
    
    def salvar_funcionario():
        conn = sqlite3.connect('empresa.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funcionarios (nome, cpf, cargo, salario, data_admissao) VALUES (?, ?, ?, ?, ?)
        ''', (entries["Nome"].get(), entries["CPF"].get(), entries["Cargo"].get(), entries["Salário"].get(), entries["Data de Admissão"].get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso")
        mostrar_conteudo("listar_funcionarios")
    
    tk.Button(frame_conteudo, text="Salvar", command=salvar_funcionario, bg="#3498DB", fg="white", font=("Arial", 12), relief="flat").pack(pady=20)

def listar_funcionarios():
    """ Lista todos os funcionários em uma tabela com opções para editar e deletar. """
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, cargo, salario, data_admissao FROM funcionarios")
    funcionarios = cursor.fetchall()
    conn.close()
    
    tabela = ttk.Treeview(frame_conteudo, columns=("ID", "Nome", "CPF", "Cargo", "Salário", "Data de Admissão"), show="headings")
    tabela.pack(expand=True, fill="both", padx=20, pady=20)
    
    for col in tabela["columns"]:
        tabela.heading(col, text=col)
    
    for funcionario in funcionarios:
        tabela.insert("", "end", values=funcionario)
    
    def deletar_funcionario():
        selected_item = tabela.selection()[0]
        funcionario_id = tabela.item(selected_item)["values"][0]
        resposta = messagebox.askyesno("Confirmar", f"Deseja realmente deletar o funcionário com ID {funcionario_id}?")
        if resposta:
            conn = sqlite3.connect('empresa.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM funcionarios WHERE id = ?", (funcionario_id,))
            conn.commit()
            conn.close()
            tabela.delete(selected_item)
            messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso")
    
    def editar_funcionario():
        selected_item = tabela.selection()[0]
        funcionario_id = tabela.item(selected_item)["values"][0]
        # Implemente a edição aqui
        messagebox.showinfo("Editar", f"Editar funcionário com ID {funcionario_id}")
    
    tk.Button(frame_conteudo, text="Deletar Funcionário", command=deletar_funcionario, bg="#E74C3C", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)
    tk.Button(frame_conteudo, text="Editar Funcionário", command=editar_funcionario, bg="#3498DB", fg="white", font=("Arial", 12), relief="flat").pack(pady=10)

# Configuração da tela de login
tela_login = tk.Tk()
tela_login.title("Login")
tela_login.geometry("400x300")
tela_login.configure(bg="#ECF0F1")

tk.Label(tela_login, text="Login", font=("Arial", 24), bg="#ECF0F1", fg="#2C3E50").pack(pady=20)

frame_login = tk.Frame(tela_login, bg="#ECF0F1")
frame_login.pack(pady=10)

tk.Label(frame_login, text="Usuário:", bg="#ECF0F1", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_usuario = tk.Entry(frame_login, font=("Arial", 12))
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_login, text="Senha:", bg="#ECF0F1", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_senha = tk.Entry(frame_login, show="*", font=("Arial", 12))
entry_senha.grid(row=1, column=1, padx=10, pady=5)

tk.Button(frame_login, text="Entrar", command=lambda: verificar_login(entry_usuario.get(), entry_senha.get()), bg="#2C3E50", fg="white", font=("Arial", 12), relief="flat").grid(row=2, columnspan=2, pady=20)

iniciar_bd()  # Inicia o banco de dados ao carregar o programa
tela_login.mainloop()
