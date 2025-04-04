

from flask import jsonify, flash
import sqlite3
import os
import datetime

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    db_path = os.path.join(os.path.dirname(__file__), 'infotech.db')
    # print(f"INFO [pesquisarClienteRota]: Conectando a: {db_path}")
    try:
        if not os.path.exists(db_path):
            raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERRO [pesquisarClienteRota]: Falha ao conectar ao banco: {e}")
        return None

# Função para o endpoint da API /buscar_cliente/<id>
def buscar_cliente(cliente_id):
    """Busca um cliente pelo ID e retorna JSON (ou erro)."""
    conn = get_db_connection()
    if not conn:
         
         # Retorna erro 500 se não puder conectar
         return jsonify({'erro': 'Falha ao conectar ao banco de dados'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (cliente_id,))
        cliente = cursor.fetchone()

        if cliente:
            
            cliente_dict = dict(cliente)

            try:
                if cliente_dict.get('data_cadastro'):
                    cliente_dict['data_cadastro'] = datetime.datetime.strptime(cliente_dict['data_cadastro'], '%Y-%m-%d').strftime('%d/%m/%Y')
                if cliente_dict.get('hora_cadastro'):
                    cliente_dict['hora_cadastro'] = datetime.datetime.strptime(cliente_dict['hora_cadastro'], '%H:%M:%S').strftime('%H:%M:%S')
            except (ValueError, TypeError) as format_error:
                 print(f"AVISO [pesquisarClienteRota]: Erro ao formatar data/hora para cliente {cliente_id}: {format_error}")
                 # Mantém os valores originais se a formatação falhar

            return jsonify(cliente_dict), 200  # Retorna 200 OK com os dados
        else:
            return jsonify({'erro': 'Cliente não encontrado'}), 404  # Retorna 404 Not Found

    except sqlite3.Error as e:
        print(f"ERRO DB [pesquisarClienteRota]: {e}")
        return jsonify({'erro': f'Erro no banco ao buscar cliente: {e}'}), 500 # Erro interno do servidor
    except Exception as ex: # Outros erros
        print(f"ERRO App [pesquisarClienteRota]: {ex}")
        return jsonify({'erro': f'Erro inesperado: {ex}'}), 500
    finally:
        if conn:
            conn.close() 