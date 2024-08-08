import streamlit as st
import sqlite3

# Função para criar o banco de dados e a tabela
def initialize_db():
    try:
        conn = sqlite3.connect('website_elements.db')
        c = conn.cursor()
        # Criar tabela para armazenar elementos HTML
        c.execute('''
        CREATE TABLE IF NOT EXISTS elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_type TEXT NOT NULL,
            content TEXT NOT NULL,
            meta_tags TEXT
        )
        ''')
        # Inserir dados de exemplo se a tabela estiver vazia
        c.execute("SELECT COUNT(*) FROM elements")
        count = c.fetchone()[0]
        if count == 0:
            c.execute("INSERT INTO elements (element_type, content, meta_tags) VALUES ('header', 'Welcome to My Site', '<meta name=\"description\" content=\"My awesome site\">')")
            c.execute("INSERT INTO elements (element_type, content, meta_tags) VALUES ('paragraph', 'This is a sample paragraph.', '<meta name=\"keywords\" content=\"sample, site\">')")
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao inicializar o banco de dados: {e}")

# Função para conectar ao banco de dados SQLite
def get_elements_from_db():
    try:
        conn = sqlite3.connect('website_elements.db')
        c = conn.cursor()
        c.execute("SELECT id, element_type, content, meta_tags FROM elements")
        elements = c.fetchall()
        conn.close()
        return elements
    except Exception as e:
        st.error(f"Erro ao obter elementos do banco de dados: {e}")
        return []

# Função para atualizar o banco de dados
def update_element(element_id, content, meta_tags):
    try:
        conn = sqlite3.connect('website_elements.db')
        c = conn.cursor()
        c.execute("UPDATE elements SET content = ?, meta_tags = ? WHERE id = ?", (content, meta_tags, element_id))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao atualizar elemento: {e}")

# Função para gerar o HTML
def generate_html(elements):
    html_content = "<!DOCTYPE html><html><head>"
    for element in elements:
        meta_tags = element[3] if element[3] else ""
        html_content += f"{meta_tags}\n"
    html_content += "</head><body>"
    for element in elements:
        html_content += f"<{element[1]}>{element[2]}</{element[1]}>\n"
    html_content += "</body></html>"
    return html_content

def main():
    # Inicializar o banco de dados
    initialize_db()

    st.title('Dashboard de Criação de Sites')

    elements = get_elements_from_db()

    st.sidebar.header('Editar Elementos')
    element_id = st.sidebar.selectbox('Selecione o Elemento', [e[0] for e in elements])

    if element_id:
        element = next(e for e in elements if e[0] == element_id)
        content = st.sidebar.text_area('Conteúdo', value=element[2])
        meta_tags = st.sidebar.text_area('Meta Tags', value=element[3] if element[3] else "")

        if st.sidebar.button('Atualizar'):
            update_element(element_id, content, meta_tags)
            st.sidebar.success('Elemento atualizado com sucesso!')

    if st.button('Gerar e Visualizar HTML'):
        html_content = generate_html(elements)
        st.code(html_content, language='html')
        st.download_button('Download HTML', data=html_content, file_name='index.html', mime='text/html')

if __name__ == '__main__':
    main()
