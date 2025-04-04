
from flask import render_template, request, redirect, url_for, abort, flash
import sqlite3
import os


def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    db_path = os.path.join(os.path.dirname(__file__), 'infotech.db')
    # print(f"INFO [cadManutRota]: Conectando a: {db_path}")
    try:
        if not os.path.exists(db_path):
            raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERRO [cadManutRota]: Falha ao conectar ao banco: {e}")
        flash(f"Erro ao conectar ao banco ({e})", "error")
        return None

def cadastrar_manutencao():
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
             
             return redirect(url_for('cadastrar_manutencao'))

        try:
    
            codigo_cliente = request.form['codigoCliente'].strip()
            data_entrada = request.form['dataEntrada'].strip()
            tipo_equipamento = request.form['tipoEquipamento'].strip() 
            marca = request.form['marca'].strip()
            modelo = request.form.get('modelo', '').strip() 
            numero_serie = request.form['numeroSerie'].strip()
            descricao_problema = request.form['descricaoProblema'].strip()
            valor_orcamento = request.form['valorOrcamento'].strip()
            status_manutencao = request.form['statusManutencao'].strip() 

            
            if not all([codigo_cliente, data_entrada, tipo_equipamento, marca, numero_serie, descricao_problema, valor_orcamento, status_manutencao]):
                 flash("Erro: Preencha todos os campos obrigatórios da manutenção.", "error")
                 return redirect(url_for('cadastrar_manutencao'))


            if not codigo_cliente.isdigit():
                 flash("Erro: Código do Cliente deve ser um número.", "error")
                 return redirect(url_for('cadastrar_manutencao'))

            # Tenta converter valor para float
            try:
                valor_orcamento_float = float(valor_orcamento)
            except ValueError:
                 flash("Erro: Valor do orçamento inválido.", "error")
                 return redirect(url_for('cadastrar_manutencao'))

            # Verifica se o cliente existe
            cur = conn.cursor()
            cur.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (int(codigo_cliente),))
            cliente_existe = cur.fetchone()
            if not cliente_existe:
                 flash(f"Erro: Cliente com ID {codigo_cliente} não encontrado.", "error")
                 conn.close() 
                 return redirect(url_for('cadastrar_manutencao'))


            conn.execute(
                """INSERT INTO manutencao
                   (codigo_cliente, data_entrada, tipo_equipamento, marca, modelo,
                    numero_serie, descricao_problema, valor_orcamento, status_manutencao, data_status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, DATE('now', 'localtime'))""", 
                (int(codigo_cliente), data_entrada, tipo_equipamento, marca, modelo,
                 numero_serie, descricao_problema, valor_orcamento_float, status_manutencao)
            )
            conn.commit()
            flash("Manutenção cadastrada com sucesso!", "success")
            print(f"INFO [cadManutRota]: Manutenção cadastrada para cliente ID {codigo_cliente}.")

        except KeyError as e:
            # Erro se um campo OBRIGATÓRIO (sem .get()) não for encontrado
            print(f"ERRO [cadManutRota]: Campo '{e}' não encontrado no form.")
            flash(f"Erro no formulário: campo '{e}' ausente.", "error")
            
            return redirect(url_for('cadastrar_manutencao'))
        except sqlite3.Error as e:
            conn.rollback() # Desfaz em caso de erro de banco
            print(f"ERRO DB [cadManutRota]: {e}")
            flash(f"Erro ao cadastrar manutenção no banco: {e}", "error")
            
            return redirect(url_for('cadastrar_manutencao'))
        except Exception as ex:
             conn.rollback()
             print(f"ERRO App [cadManutRota]: {ex}")
             flash(f"Erro inesperado ao cadastrar manutenção: {ex}", "error")
            
             return redirect(url_for('cadastrar_manutencao'))

        finally:
             if conn:
                 conn.close() 

        return redirect(url_for('cadastrar_manutencao')) 

    return render_template('cadastrar-manutencao.html')