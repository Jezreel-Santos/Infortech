
from flask import redirect, render_template, request, url_for, flash 
import sqlite3
import os


def get_db_connection():
    ### Cria e retorna uma conexão com o banco de dados SQLite. ###
    db_path = os.path.join(os.path.dirname(__file__), 'infotech.db')
    try:
        if not os.path.exists(db_path):
            raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERRO [atualizarClienteRota]: Falha ao conectar ao banco: {e}")
        flash(f"Erro ao conectar ao banco ({e})", "error")
        return None

# --- Função Principal da Rota ---
def atualizar_cadastro():

    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
             # Flash já emitido por get_db_connection
             return redirect(url_for('atualizar_cadastro'))

        try:
            cliente_id = request.form['id_cliente']
            nome = request.form.get('nome', '').strip()
            cpf = request.form.get('cpf', '').strip()
            telefone = request.form.get('telefone', '').strip()
            email = request.form.get('email', '').strip()
            endereco = request.form.get('endereco', '').strip()

            if not all([cliente_id, nome, cpf, telefone, email, endereco]):
                 flash("Erro: Preencha todos os campos para atualizar.", "error")
                 return redirect(url_for('atualizar_cadastro'))

            # Verificar se o novo CPF já existe para OUTRO cliente
            cur = conn.cursor()
            cur.execute("SELECT id_cliente FROM clientes WHERE cpf = ? AND id_cliente != ?", (cpf, cliente_id))
            existing_cpf = cur.fetchone()
            if existing_cpf:
                flash(f"Erro: O CPF {cpf} já pertence a outro cliente (ID: {existing_cpf['id_cliente']}).", "error")
                return redirect(url_for('atualizar_cadastro'))

            # Executa a atualização
            cur.execute(
                'UPDATE clientes SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ? WHERE id_cliente = ?',
                (nome, cpf, telefone, email, endereco, cliente_id)
            )
            conn.commit()

            if cur.rowcount > 0:
                flash("Cadastro do cliente atualizado com sucesso!", "success")
            else:
                flash("Nenhuma alteração realizada (cliente não encontrado ou dados idênticos).", "warning")

        except KeyError as e:
            flash(f"Erro no formulário: campo '{e}' ausente.", "error")
        except sqlite3.Error as e:
            conn.rollback()
            flash(f"Erro ao atualizar cliente no banco: {e}", "error")
        except Exception as ex:
            conn.rollback()
            flash(f"Erro inesperado ao atualizar cliente: {ex}", "error")
        finally:
             if conn:
                conn.close() 

        return redirect(url_for('atualizar_cadastro'))

    return render_template('atualizar-cliente.html')


