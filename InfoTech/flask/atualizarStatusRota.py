
from flask import render_template, request, flash, redirect, url_for
import sqlite3
import os
import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'infotech.db')
    try:
        if not os.path.exists(db_path):
            raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERRO [atualizarStatusRota]: Falha ao conectar ao banco: {e}")
        flash(f"Erro ao conectar ao banco ({e})", "error")
        return None

def atualizar_status():
    manutencao_data = None
    if request.method == 'GET':
        manutencao_id_get = request.args.get('id', type=int)
        if manutencao_id_get:
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT m.*, c.nome as nome_cliente FROM manutencao m
                        LEFT JOIN clientes c ON m.codigo_cliente = c.id_cliente
                        WHERE m.codigo_manutencao = ? """, (manutencao_id_get,))
                    manutencao_data = cursor.fetchone()
                    if not manutencao_data:
                        flash(f"Manutenção ID {manutencao_id_get} não encontrada.", "warning")
                except sqlite3.Error as e:
                    flash(f"Erro ao buscar manutenção: {e}", "error")
                finally:
                    conn.close()
        return render_template('atualizar-status.html', manutencao=manutencao_data)

    if request.method == 'POST':
        action = request.form.get('action')
        conn = get_db_connection() # Abre conexão para POST actions
        if not conn:
             
             return redirect(url_for('atualizar_status'))

        try:
            if action == 'buscar':
                manutencao_id_busca = request.form.get('manutencao_id_busca', '').strip()
                if not manutencao_id_busca or not manutencao_id_busca.isdigit():
                    flash("Insira um ID válido.", "warning")
                    return redirect(url_for('atualizar_status'))
                return redirect(url_for('atualizar_status', id=manutencao_id_busca))

            elif action == 'atualizar':
                manutencao_id_update = request.form.get('manutencao_id_update', type=int)
                novo_status = request.form.get('status_manutencao', '').strip()
                data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
                if not manutencao_id_update or not novo_status:
                    flash("Dados insuficientes para atualização.", "error")
                else:
                    cursor = conn.cursor()
                    cursor.execute("""UPDATE manutencao SET status_manutencao = ?, data_status = ?
                                   WHERE codigo_manutencao = ?""",
                                   (novo_status, data_atual, manutencao_id_update))
                    conn.commit()
                    if cursor.rowcount > 0:
                        flash(f"Status da ID {manutencao_id_update} atualizado para '{novo_status}'!", "success")
                    else:
                         flash(f"Manutenção ID {manutencao_id_update} não encontrada.", "warning")

            elif action == 'excluir':
                manutencao_id_delete = request.form.get('manutencao_id_delete', type=int)
                if not manutencao_id_delete:
                    flash("ID não fornecido para exclusão.", "error")
                else:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM manutencao WHERE codigo_manutencao = ?", (manutencao_id_delete,))
                    conn.commit()
                    if cursor.rowcount > 0:
                        flash(f"Manutenção ID {manutencao_id_delete} excluída!", "success")
                    else:
                        flash(f"Manutenção ID {manutencao_id_delete} não encontrada.", "warning")
            else:
                flash("Ação desconhecida.", "error")

        except sqlite3.Error as e:
            conn.rollback() # Desfaz se der erro no meio
            print(f"ERRO DB [atualizarStatusRota]: {e}")
            flash(f"Erro no banco de dados: {e}", "error")
        except Exception as ex:
            conn.rollback()
            print(f"ERRO App [atualizarStatusRota]: {ex}")
            flash("Ocorreu um erro inesperado.", "error")
        finally:
             if conn: # Garante fechamento da conexão aberta para POST
                 conn.close()

        return redirect(url_for('atualizar_status')) # Redireciona para limpar após POST

    return redirect(url_for('atualizar_status')) 