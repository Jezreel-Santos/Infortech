
from flask import Flask, render_template, url_for, redirect
import secrets
import os

# --- Funções de rota e gerenciamento de conexão ---

from cadClienteRota import cadastrar_cliente, close_connection as close_db_connection_g
from pesquisarClienteRota import buscar_cliente 
from atualizarClienteRota import atualizar_cadastro 
from cadastrarManutencaoRota import cadastrar_manutencao
from pesquisarManutencaoRota import pesquisar_manutencao
from atualizarStatusRota import atualizar_status
from contatoRota import contato

# --- Instância Principal do App ---
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# --- Registrar Função Teardown ---
@app.teardown_appcontext
def teardown_db_g(exception=None):
    close_db_connection_g(exception) # Fecha conexões de cadClienteRota



# --- Registro das Rotas ---

# Rotas de Cliente
app.add_url_rule('/cadastrar_cliente', view_func=cadastrar_cliente, methods=['GET', 'POST'])
app.add_url_rule('/buscar_cliente/<int:cliente_id>', view_func=buscar_cliente, methods=['GET'])
app.add_url_rule('/atualizar_cadastro', view_func=atualizar_cadastro, methods=['GET', 'POST'])


# Rotas de Manutenção
app.add_url_rule('/cadastrar_manutencao', view_func=cadastrar_manutencao, methods=['GET', 'POST'])
app.add_url_rule('/pesquisar_manutencao', view_func=pesquisar_manutencao, methods=['GET', 'POST'])
app.add_url_rule('/atualizar_status', view_func=atualizar_status, methods=['GET', 'POST'])

# Rota de Contato
app.add_url_rule('/contato', view_func=contato, methods=['GET'])



# --- Rotas Definidas Diretamente Aqui ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pesquisar_cliente')
def pesquisar_cliente_page():
    return render_template('pesquisar-cliente.html')


# --- Execução Principal ---
if __name__ == '__main__':
    db_path_check = os.path.join(os.path.dirname(__file__), 'infotech.db')
    if not os.path.exists(db_path_check):
        print(f"\nAVISO: Banco de dados '{db_path_check}' não encontrado.")
        print(f"Execute o script 'python criar_tab_manutencao.py' (e outros) para inicializar.\n")
    else:
        print(f"\nINFO: Banco de dados '{db_path_check}' encontrado.")

    print("INFO: Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0')